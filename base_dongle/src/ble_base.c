/**
 * @file ble_base.c
 * @author Blake Rowden (b.rowden@uqconnect.edu.au)
 * @brief
 * @version 0.1
 * @date 2022-03-23
 *
 * @copyright Copyright (c) 2022
 *
 */

#include "ble_base.h"

static void start_scan(void);

static struct bt_conn *default_conn;
bool ble_connected;

// Logging Module
LOG_MODULE_REGISTER(BLE, LOG_LEVEL_INF);

/* Custom UUIDs For Mobile and it's GATT Attributes */
#define UUID_BUFFER_SIZE 16
// Used to as a key to test against scanned UUIDs
uint16_t mobile_uuid[] = {0xd5, 0x92, 0x67, 0x35, 0x78, 0x16, 0x21, 0x91,
                          0x26, 0x49, 0x60, 0xeb, 0x06, 0xa7, 0xca, 0xcb};

static struct bt_uuid_128 gatt_uuid_radar =
    BT_UUID_INIT_128(0xd1, 0x92, 0x67, 0x35, 0x78, 0x16, 0x21, 0x91, 0x26, 0x49,
                     0x60, 0xeb, 0x06, 0xa7, 0xca, 0xcb);
;

// Radar RX BUFFER
int rx_buff[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

/**
 * @brief Used to parse the advertisement data
 *        in order to find the UUID of the service we are looking for.
 *
 */
static bool parse_device(struct bt_data *data, void *user_data) {
    bt_addr_le_t *addr = user_data;
    int i;
    int matchedCount = 0;

    LOG_DBG("[AD]: %u data_len %u", data->type, data->data_len);

    if (data->type == BT_DATA_UUID128_ALL) {
        uint16_t temp = 0;
        for (i = 0; i < data->data_len; i++) {
            temp = data->data[i];
            if (temp == mobile_uuid[i]) {
                matchedCount++;
            }
        }

        if (matchedCount == UUID_BUFFER_SIZE) {
            // MOBILE UUID MATCHED
            LOG_INF("Mobile UUID Found, attempting to connect");

            int err = bt_le_scan_stop();
            k_msleep(10);

            if (err) {
                LOG_ERR("Stop LE scan failed (err %d)", err);
                return true;
            }

            struct bt_le_conn_param *param = BT_LE_CONN_PARAM_DEFAULT;

            err = bt_conn_le_create(addr, BT_CONN_LE_CREATE_CONN, param,
                                    &default_conn);
            if (err) {
                LOG_ERR("Create conn failed (err %d)", err);
                start_scan();
            }

            return false;
        }
    }
    return true;
}

/**
 * @brief Callback function for when scan detects device, scanned devices
 *          are filtered by their connectibilty and scan data is parsed.
 *
 * @param addr Device Address
 * @param rssi RSSI
 * @param type Device Type
 * @param ad Adv Data
 */
static void device_found(const bt_addr_le_t *addr, int8_t rssi, uint8_t type,
                         struct net_buf_simple *ad) {
    if (default_conn) {
        return;
    }

    /* We're only interested in connectable events */
    if (type == BT_GAP_ADV_TYPE_ADV_IND ||
        type == BT_GAP_ADV_TYPE_ADV_DIRECT_IND) {
        bt_data_parse(ad, parse_device, (void *)addr);
    }
}

/**
 * @brief Starts passive BLE scanning for nearby
 *          devices.
 */
static void start_scan(void) {
    int err;

    err = bt_le_scan_start(BT_LE_SCAN_PASSIVE, device_found);
    if (err) {
        LOG_ERR("Scanning failed to start (err %d)", err);
        return;
    }

    LOG_INF("Scanning successfully started");
}

/**
 * @brief Callback for when reading RSSI Gatt atrribute data
 *          from the mobile device. The data read is saved into
 *          and internal rx buffer.
 *
 * @param conn ble connection handler
 * @param err  ble ATT error val
 * @param params Read params
 * @param data Data read from GATT attribute
 * @param length Len of Data
 * @return uint8_t retVal (custom)
 */
uint8_t read_radar_from_mobile(struct bt_conn *conn, uint8_t err,
                               struct bt_gatt_read_params *params,
                               const void *data, uint16_t length) {
    memcpy(&rx_buff, data, sizeof(rx_buff));
    return 0;
}

/**
 * @brief BLE Device connected callback function. If an error is detected
 *          scan is restarted. Else, the app can establish that the
 *          devices are now conneted using flag ble_connected;
 *
 * @param conn Connection handler
 * @param err BLE ERR
 */
static void connected(struct bt_conn *conn, uint8_t err) {
    char addr[BT_ADDR_LE_STR_LEN];

    bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));

    if (err) {
        LOG_ERR("Failed to connect to %s (%u)", addr, err);

        bt_conn_unref(default_conn);
        default_conn = NULL;

        start_scan();
        return;
    }

    if (conn != default_conn) {
        return;
    }
    ble_connected = true;
    LOG_INF("Connected: %s", addr);
}

/**
 * @brief BLE Disconnected callback, when disconnected, restarts BLE scanning
 *          and the app can detect that BLE has been disconnected by referring
 * to ble_connected flag.
 *
 * @param conn Connection handler.
 * @param reason Disconnect reason (ERR VAL).
 */
static void disconnected(struct bt_conn *conn, uint8_t reason) {
    char addr[BT_ADDR_LE_STR_LEN];

    if (conn != default_conn) {
        return;
    }

    bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));

    LOG_WRN("Disconnected: %s (reason 0x%02x)", addr, reason);

    bt_conn_unref(default_conn);
    default_conn = NULL;
    ble_connected = false;
    start_scan();
}

/**
 * @brief Connection callback struct, required to set conn/disconn
 *          function pointers.
 */
static struct bt_conn_cb conn_callbacks = {
    .connected = connected,
    .disconnected = disconnected,
};

/**
 * @brief BLE Base entry thread, starts initial ble scanning.
 *          When a valid mobile device is connected.
 */
void thread_ble_base(void *p1, void *p2, void *p3) {
    int err;

    err = bt_enable(NULL);
    default_conn = NULL;

    if (err) {
        LOG_ERR("Bluetooth init failed (err %d)", err);
        return;
    }

    LOG_INF("Bluetooth initialized");

    bt_conn_cb_register(&conn_callbacks);

    start_scan();
}

/**
 * @brief Prints data to the terminal in JSON format
 *
 */
void thread_ble_terminal_print(void *p1, void *p2, void *p3) {
    static struct bt_gatt_read_params read_params_radar = {
        .func = read_radar_from_mobile,
        .handle_count = 0,
        .by_uuid.uuid = &gatt_uuid_radar.uuid,
        .by_uuid.start_handle = BT_ATT_FIRST_ATTRIBUTE_HANDLE,
        .by_uuid.end_handle = BT_ATT_LAST_ATTRIBUTE_HANDLE,
    };

    int timeStamp = 0;

    while (1) {
        if (ble_connected) {
            timeStamp = k_cyc_to_ms_floor64(k_cycle_get_32());
            // Read Radar data from mobile
            bt_gatt_read(default_conn, &read_params_radar);

            led0_toggle();
            // Print data to terminal in JSON
        }

        k_usleep(200);
    }
}

/**
 * @brief Blink LED when BLE connected
 *
 */
void thread_ble_led(void *p1, void *p2, void *p3) {
    ble_connected = false;
    bool red_led_is_on = false;
    bool green_led_is_on = false;
    init_leds();

    while (1) {
        if (ble_connected) {
            if (red_led_is_on) {
                led1_off();
            }
            red_led_is_on = false;
            if (!green_led_is_on) {
                led2_on();
            }
            green_led_is_on = true;
            k_msleep(BLE_CONN_SLEEP_MS);
        } else {
            if (green_led_is_on) {
                led2_off();
            }
            green_led_is_on = false;
            red_led_is_on ? led1_off() : led1_on();
            k_msleep(BLE_DISC_SLEEP_MS);
            red_led_is_on = !red_led_is_on;
        }
    }
}