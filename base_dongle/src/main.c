/*******************************************************************************
 Module Name: USB BLE Dongle

 Made for CSSE 4011 Semester 1 2022

 First written on 10/05/2022 by Blake Rowden s4427634

 Module Description:
*******************************************************************************/

/* Includes *******************************************************************/
#include "main.h"

int errno;

/* Defines ********************************************************************/
LOG_MODULE_REGISTER(MAIN, LOG_LEVEL_DBG);

K_THREAD_STACK_DEFINE(thread_stack_ble, THREAD_STACK_BLE);
K_THREAD_STACK_DEFINE(thread_stack_terminal, THREAD_STACK_TERMINAL);
K_THREAD_STACK_DEFINE(thread_stack_led, THREAD_STACK_LED);

/* Function Prototypes ********************************************************/
int enable_terminal(void);

/**
 * @brief Main entry point
 *
 */
void main(void) {
    init_leds();

    led3_on();  // Blue LED to show terminal is yet to be connected

    errno = enable_terminal();
    if (errno) {
        LOG_ERR("Recieved Error: %d", errno);
        return;
    }

    struct k_thread thread_ble;
    struct k_thread thread_terminal;
    struct k_thread thread_led;

    LOG_DBG("Starting LED Thread");

    k_thread_create(&thread_led, thread_stack_led,
                    K_THREAD_STACK_SIZEOF(thread_stack_led), thread_ble_led,
                    NULL, NULL, NULL, THREAD_PRIORITY_LED, 0, K_NO_WAIT);

    LOG_DBG("Starting BLE Thread");

    k_thread_create(&thread_ble, thread_stack_ble,
                    K_THREAD_STACK_SIZEOF(thread_stack_ble), thread_ble_base,
                    NULL, NULL, NULL, THREAD_PRIORITY_BLE, 0, K_MSEC(50));

    LOG_DBG("Starting PRINT Thread");

    k_thread_create(&thread_terminal, thread_stack_terminal,
                    K_THREAD_STACK_SIZEOF(thread_stack_terminal),
                    thread_ble_terminal_print, NULL, NULL, NULL,
                    THREAD_PRIORITY_TERMINAL, 0, K_NO_WAIT);

    LOG_DBG("All Threads Started");
}

/**
 * @brief Enable the USB Driver and start the terminal
 *
 * @return int: error value
 */
int enable_terminal(void) {
    /* Enable the USB Driver */
    errno = usb_enable(NULL);
    if (errno) return errno;

    /* Setup DTR - 'Data Terminal Ready' */
    const struct device *console_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));
    uint32_t dtr = 0;

    /* Wait on DTR - Ensure startup logs are visible*/
    while (!dtr) {
        errno = uart_line_ctrl_get(console_dev, UART_LINE_CTRL_DTR, &dtr);
        if (errno) return errno;
        k_sleep(K_MSEC(50));
    }

    LOG_INF("Terminal Successfully Connected");

    led3_off();  // Turn off blue LED to show terminal is connected

    return 0;
}