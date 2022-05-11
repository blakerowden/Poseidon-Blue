/*******************************************************************************
 Module Name: USB BLE Dongle

 Made for CSSE 4011 Semester 1 2022

 First written on 10/05/2022 by Blake Rowden s4427634

 Module Description:
*******************************************************************************/

#ifndef MAIN_H
#define MAIN_H

/* Includes *******************************************************************/
#include <device.h>
#include <devicetree.h>
#include <drivers/uart.h>
#include <stddef.h>
#include <sys/printk.h>
#include <usb/usb_device.h>
#include <zephyr.h>
#include <zephyr/types.h>

#include "ble_base.h"

/* Defines ********************************************************************/
#define THREAD_STACK_BLE      4094
#define THREAD_STACK_TERMINAL 4094
#define THREAD_STACK_LED      512

#define THREAD_PRIORITY_BLE      1
#define THREAD_PRIORITY_TERMINAL 1
#define THREAD_PRIORITY_LED      2

#endif  // MAIN_H
