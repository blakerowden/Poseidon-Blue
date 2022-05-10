/**
 * @file main.c
 * @author Blake Rowden (b.rowden@uqconnect.edu.au) - s4427634
 * @brief USB BLE Base Dongle
 * @version 1
 * @date 2022-05-10
 *
 * @copyright Copyright (c) 2022
 *
 */

#include "main.h"

LOG_MODULE_REGISTER(main, LOG_LEVEL_INF);

/**
 * @brief Main entry point
 *
 */
void main(void) { enable_terminal(); }

/**
 * @brief Enable the USB Driver and start the terminal
 *
 * @return int: error value
 */
int enable_terminal(void) {
    /* Enable the USB Driver */
    if (usb_enable(NULL)) return;

    /* Setup DTR - 'Data Terminal Ready' */
    const struct device *console_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));
    uint32_t dtr = 0;

    /* Wait on DTR - Ensure startup logs are visible*/
    while (!dtr) {
        uart_line_ctrl_get(console_dev, UART_LINE_CTRL_DTR, &dtr);
        k_sleep(K_MSEC(50));
    }

    LOG_INF("Terminal Successfully Connected");

    return 0;
}
