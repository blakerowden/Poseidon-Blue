/*******************************************************************************
 Module Name:

 Made for CSSE 4011 Semester 1 2022

 First written on 10/05/2022 by Blake Rowden s4427634

 Module Description:
*******************************************************************************/

/* Includes *******************************************************************/
#include "main.h"

#include "stdint.h"

/* Defines ********************************************************************/
LOG_MODULE_REGISTER(main, LOG_LEVEL_INF);

/* Function Prototypes ********************************************************/
int enable_terminal(void);

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
    if (usb_enable(NULL)) return -1;

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
