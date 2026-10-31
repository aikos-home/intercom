"""Privacy scan: run before every push.

    python tools/privacy_scan.py --denylist PATH
    (or set KLINGELBOX_DENYLIST=PATH)

The denylist is a private text file that is never committed. One term per line:
  - plain words match case-insensitively as whole words ("anna" does not hit "Johanna");
  - terms with punctuation (".lan", "10.0.") match as plain substrings;
  - lines starting with "!" are allowed phrases that are blanked out before matching
    (e.g. a public repository URL that contains a name);
  - "#" starts a comment.

Built-in checks, no denylist needed: private IPv4 addresses, MAC addresses, e-mail
addresses and Home Assistant entity ids. Binary files are scanned as Latin-1 text, so
names inside STL/STEP headers or PNG metadata are found too. ZIP containers (FCStd, 3MF,
anything starting with "PK") are unpacked and every member is scanned the same way, nested
ones too; compressed PNG text chunks (zTXt, iTXt) are unpacked as well. A Latin-1 read of
the packed bytes would not see a name in there.

Exit code 1 if anything is found.
"""
import argparse
import io
import os
import re
import struct
import subprocess
import sys
import zipfile
import zlib

MAX_MEMBER = 64 * 1024 * 1024  # a member bigger than this is reported, not read

BUILTIN = {
    "private IPv4": re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
    "MAC address": re.compile(r"\b[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}\b"),
    "e-mail address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "HA entity id": re.compile(r"\b(?:binary_sensor|input_boolean|input_text|input_number|input_select|"
                               r"automation|device_tracker|person|zone|notify)\.[a-z0-9_]{3,}\b"),
}
ALLOWED_EMAILS = {"noreply@anthropic.com"}


def repo_files(root):
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=root, capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines() if f]


def decode(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def png_texts(raw):
    """The compressed text chunks of a PNG (zTXt, compressed iTXt), unpacked."""
    out, pos = [], 8
    while pos + 8 <= len(raw):
        size = struct.unpack(">I", raw[pos:pos + 4])[0]
        kind, data = raw[pos + 4:pos + 8], raw[pos + 8:pos + 8 + size]
        pos += 12 + size
        try:
            if kind == b"zTXt":
                key, rest = data.split(b"\0", 1)
                out.append(key + b": " + zlib.decompress(rest[1:]))
            elif kind == b"iTXt":
                key, rest = data.split(b"\0", 1)
                compressed, body = rest[0], rest[2:]
                _lang, body = body.split(b"\0", 1)
                translated, text = body.split(b"\0", 1)
                out.append(key + b" " + translated + b": " + (zlib.decompress(text) if compressed else text))
        except (ValueError, IndexError, zlib.error):
            out.append(b"(unreadable " + kind + b" chunk)")
    return out


def texts(label, raw, depth=0):
    """(label, text) of a file and of whatever is packed inside it."""
    yield label, decode(raw)
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        for i, t in enumerate(png_texts(raw)):
            yield f"{label}[text chunk {i}]", decode(t)
    if raw[:4] == b"PK\x03\x04" and depth < 4:
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    if info.file_size > MAX_MEMBER:
                        yield f"{label}!{info.filename}", "(member too big to scan)"
                        continue
                    yield from texts(f"{label}!{info.filename}", z.read(info), depth + 1)
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as e:
            yield f"{label}", f"(zip not readable: {e})"


def load_denylist(path):
    terms, allowed = [], []
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("!"):
            allowed.append(line[1:].strip().lower())
        else:
            terms.append(line.lower())
    return terms, allowed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--denylist", default=os.environ.get("KLINGELBOX_DENYLIST"))
    args = ap.parse_args()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    terms, allowed = ([], [])
    if args.denylist:
        terms, allowed = load_denylist(args.denylist)
    else:
        print("warning: no denylist given, running the built-in checks only")
    patterns = []
    for t in terms:
        if re.fullmatch(r"[\wÀ-ɏ]+", t):
            patterns.append((t, re.compile(r"(?<![\wÀ-ɏ])" + re.escape(t) + r"(?![\wÀ-ɏ])")))
        else:
            patterns.append((t, re.compile(re.escape(t))))
    hits = 0
    for rel in repo_files(root):
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        raw = open(path, "rb").read()
        for label, text in texts(rel, raw):
            low = text.lower()
            for a in allowed:
                low = low.replace(a, " " * len(a))
            # the built-in checks see the same blanks (keeps the original case elsewhere): an allowed phrase like a
            # SoftAP default address or a product entity id is allowed everywhere
            blank = text
            for a in allowed:
                blank = re.sub(re.escape(a), lambda m: " " * len(m.group(0)), blank, flags=re.IGNORECASE)
            for t, rx in patterns:
                for m in rx.finditer(low):
                    line = low.count("\n", 0, m.start()) + 1
                    print(f"{label}:{line}: denylisted term '{t}'")
                    hits += 1
            for name, rx in BUILTIN.items():
                for m in rx.finditer(blank):
                    if name == "e-mail address" and m.group(0).lower() in ALLOWED_EMAILS:
                        continue
                    line = text.count("\n", 0, m.start()) + 1
                    print(f"{label}:{line}: {name}: {m.group(0)}")
                    hits += 1
    print(f"{hits} finding(s)" if hits else "clean")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
