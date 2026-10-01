#include <stdint.h>
#include "esp_flash.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "esp_system.h"
#include "sdkconfig.h"
#include "board_support.h"

static const char *TAG = "board_support";

#if CONFIG_P4_BOARD_FUNCTION_EV_V152
extern const struct p4_board_config p4_function_ev_v152;
#else
#error "Select and implement a P4 board profile before building"
#endif

const struct p4_board_config *p4_board_get(void)
{
    return &p4_function_ev_v152;
}

void p4_board_report_memory(void)
{
    esp_chip_info_t chip = {0};
    esp_chip_info(&chip);
    ESP_LOGI(TAG, "detected chip revision: %d", chip.revision);
    uint32_t flash_bytes = 0;
    esp_err_t err = esp_flash_get_size(NULL, &flash_bytes);
    if (err == ESP_OK) {
        ESP_LOGI(TAG, "detected NOR flash: %lu bytes", (unsigned long)flash_bytes);
    } else {
        ESP_LOGE(TAG, "NOR flash size query failed: %s", esp_err_to_name(err));
    }
    ESP_LOGI(TAG, "ESP-IDF available PSRAM heap: %lu bytes",
             (unsigned long)heap_caps_get_total_size(MALLOC_CAP_SPIRAM));
    ESP_LOGI(TAG, "PSRAM heap size is a boot diagnostic, not a memory stress test");
}
