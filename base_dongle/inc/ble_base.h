/*******************************************************************************
 Module Name: USB BLE Dongle Bluetooth

 Made for CSSE 4011 Semester 1 2022

 First written on 10/05/2022 by Blake Rowden s4427634

 Module Description:
*******************************************************************************/

#ifndef BLE_BASE_H
#define BLE_BASE_H

/* Includes *******************************************************************/
#include <bluetooth/bluetooth.h>
#include <bluetooth/conn.h>
#include <bluetooth/gatt.h>
#include <bluetooth/hci.h>
#include <bluetooth/uuid.h>
#include <drivers/gpio.h>
#include <drivers/uart.h>
#include <errno.h>
#include <logging/log.h>
#include <stddef.h>
#include <sys/byteorder.h>
#include <sys/printk.h>
#include <usb/usb_device.h>
#include <zephyr.h>
#include <zephyr/types.h>

#include "led_driver.h"

/* Defines ********************************************************************/
#define SLEEP_TIME_MS     1000
#define BLE_DISC_SLEEP_MS 250
#define BLE_CONN_SLEEP_MS 2000

/* Function Prototypes ********************************************************/

/**
 * @brief Runs the LED to show the connection status of the BLE device
 *
 */
extern void thread_ble_led(void *, void *, void *);

/**
 * @brief Base thread to start the BLE stack
 *
 */
extern void thread_ble_base(void *, void *, void *);

/**
 * @brief Thread to print the BLE data to the terminal
 *
 */
extern void thread_ble_terminal_print(void *, void *, void *);

#endif  // BLE_BASE_H