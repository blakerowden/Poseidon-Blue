/**
 * @file main.c
 * @author Blake Rowden (b.rowden@uqconnect.edu.au) - s4427634
 * @brief Mobile/Static Node
 * @version 0.2
 * @date 2022-03-15
 *
 * @copyright Copyright (c) 2022
 *
 */

#include "main.h"

LOG_MODULE_REGISTER(log_main);  // Logging Module

K_THREAD_DEFINE(ble_mobile, BLE_CONNECT_THREAD_STACK, thread_ble_connect, NULL,
                NULL, NULL, BLE_CONNECT_THREAD_PRIORITY, 0, 0);


