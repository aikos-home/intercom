set(board_sources "board_support.c")
if(CONFIG_P4_BOARD_FUNCTION_EV_V152)
    list(APPEND board_sources "boards/function_ev_v152.c")
else()
    message(FATAL_ERROR "No implemented P4 board profile selected")
endif()

idf_component_register(SRCS ${board_sources} INCLUDE_DIRS "include"
                       PRIV_REQUIRES spi_flash heap esp_system log)
