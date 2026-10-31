// aikos_firmware: normal firmware <-> the device's own safe firmware in the factory partition (see __init__.py).
#include "aikos_firmware.h"

#include <esp_ota_ops.h>
#include <esp_partition.h>
#include <nvs.h>
#include "esphome/core/application.h"
#include "esphome/core/hal.h"
#include "esphome/core/log.h"

namespace esphome::aikos_firmware {

static const char *const TAG = "aikos_firmware";
static const char *const NVS_NS = "aikos_fw";
static const char *const NVS_KEY = "normal_slot";  // subtype of the OTA slot that ran before the safe firmware

static const esp_partition_t *factory_partition() {
  return esp_partition_find_first(ESP_PARTITION_TYPE_APP, ESP_PARTITION_SUBTYPE_APP_FACTORY, nullptr);
}

static bool has_valid_app(const esp_partition_t *p) {
  esp_app_desc_t desc;
  return p != nullptr && esp_ota_get_partition_description(p, &desc) == ESP_OK;
}

bool running_safe_firmware() {
  const esp_partition_t *factory = factory_partition();
  return factory != nullptr && esp_ota_get_running_partition() == factory;
}

bool boot_safe_firmware() {
  const esp_partition_t *factory = factory_partition();
  if (!has_valid_app(factory)) {
    ESP_LOGE(TAG, "no safe firmware in a factory partition: staying (ESPHome safe mode)");
    return false;
  }
  const esp_partition_t *running = esp_ota_get_running_partition();
  if (running == factory)
    return false;  // already the safe firmware: ESPHome's own safe mode takes over
  nvs_handle_t h;
  if (nvs_open(NVS_NS, NVS_READWRITE, &h) == ESP_OK) {
    nvs_set_u8(h, NVS_KEY, static_cast<uint8_t>(running->subtype));
    nvs_commit(h);
    nvs_close(h);
  }
  const esp_err_t err = esp_ota_set_boot_partition(factory);
  if (err != ESP_OK) {
    ESP_LOGE(TAG, "cannot select the safe firmware: %s", esp_err_to_name(err));
    return false;
  }
  ESP_LOGE(TAG, "boot loop of the normal firmware ('%s'): starting the SAFE firmware", running->label);
  delay(200);  // let the log line out
  App.reboot();
  return true;
}

bool boot_normal_firmware() {
  uint8_t subtype = ESP_PARTITION_SUBTYPE_APP_OTA_0;
  nvs_handle_t h;
  if (nvs_open(NVS_NS, NVS_READONLY, &h) == ESP_OK) {
    nvs_get_u8(h, NVS_KEY, &subtype);
    nvs_close(h);
  }
  const esp_partition_t *p =
      esp_partition_find_first(ESP_PARTITION_TYPE_APP, static_cast<esp_partition_subtype_t>(subtype), nullptr);
  if (!has_valid_app(p)) {  // the remembered slot is empty: try the other one
    const esp_partition_subtype_t other = subtype == ESP_PARTITION_SUBTYPE_APP_OTA_0 ? ESP_PARTITION_SUBTYPE_APP_OTA_1
                                                                                      : ESP_PARTITION_SUBTYPE_APP_OTA_0;
    p = esp_partition_find_first(ESP_PARTITION_TYPE_APP, other, nullptr);
  }
  if (!has_valid_app(p)) {
    ESP_LOGW(TAG, "no normal firmware to go back to: staying on the safe firmware");
    return false;
  }
  const esp_err_t err = esp_ota_set_boot_partition(p);
  if (err != ESP_OK) {
    ESP_LOGE(TAG, "cannot select the normal firmware '%s': %s", p->label, esp_err_to_name(err));
    return false;
  }
  ESP_LOGW(TAG, "trying the normal firmware again ('%s')", p->label);
  delay(200);
  App.reboot();
  return true;
}

void AikosFirmware::setup() {
  const esp_partition_t *running = esp_ota_get_running_partition();
  if (running_safe_firmware())
    ESP_LOGW(TAG, "SAFE firmware running (partition '%s')", running->label);
}

void AikosFirmware::loop() {
  if (!this->safe_role_ || !running_safe_firmware()) {
    this->disable_loop();
    return;
  }
  if (millis() > this->retry_ms_) {
    this->disable_loop();
    boot_normal_firmware();  // returns only if there is no normal firmware to try
  }
}

void AikosFirmware::dump_config() {
  const esp_partition_t *running = esp_ota_get_running_partition();
  const esp_partition_t *factory = factory_partition();
  ESP_LOGCONFIG(TAG,
                "aikos firmware:\n"
                "  Role: %s, running partition '%s'\n"
                "  Safe firmware in the factory partition: %s",
                this->safe_role_ ? "safe" : "normal", running != nullptr ? running->label : "?",
                has_valid_app(factory) ? "yes" : "NO");
  if (this->safe_role_)
    ESP_LOGCONFIG(TAG, "  Tries the normal firmware again after %u min", (unsigned) (this->retry_ms_ / 60000));
}

}  // namespace esphome::aikos_firmware
