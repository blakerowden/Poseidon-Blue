/**
 ******************************************************************************
 * @file           : led_driver.c
 * @brief          : The LED Driver provides functionality to control onboard
 * LEDs in a Zepher environment.
 ******************************************************************************
 * @attention Built for CSSE4011 Semester 1 2022
 *
 * @author: Blake Rowden
 * @date: 12/03/2022
 * ***************************************************************************
 */

#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <logging/log.h>
#include <zephyr.h>

/* Local Includes ------------------------------------------------------------*/

#include "led_driver.h"

/* Local Defines -------------------------------------------------------------*/

#define ON  1
#define OFF 0

/* Logging Module ------------------------------------------------------------*/

LOG_MODULE_REGISTER(led_module);

bool led_status(int led_no);

/* Public Function Definitions -----------------------------------------------*/

/* LED0 Functions */

int led0_init(void) {
    const struct device *dev = device_get_binding(LED0);
    if (dev == NULL) {
        return DEV_NOT_FOUND;
    }

    LOG_DBG("LED0 Initialized");

    return gpio_pin_configure(dev, LED0_PIN, GPIO_OUTPUT_INACTIVE | LED0_FLAGS);
}

int led0_on(void) {
    const struct device *dev = device_get_binding(LED0);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(0)) {
        LOG_WRN("LED0 Already ON");
    } else {
        LOG_INF("LED0 is ON");
    }
    return gpio_pin_set(dev, LED0_PIN, ON);
}

int led0_off(void) {
    const struct device *dev = device_get_binding(LED0);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(0)) {
        LOG_INF("LED0 is OFF");
    } else {
        LOG_WRN("LED0 is Already OFF");
    }

    return gpio_pin_set(dev, LED0_PIN, OFF);
}

int led0_toggle(void) {
    const struct device *dev = device_get_binding(LED0);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(0)) {
        LOG_INF("LED0 is OFF");
    } else {
        LOG_INF("LED0 is ON");
    }

    return gpio_pin_toggle(dev, LED0_PIN);
}

int led0_deinit(void) {
    const struct device *dev = device_get_binding(LED0);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    LOG_DBG("LED0 Deinitialized OK");

    return gpio_pin_configure(dev, LED0_PIN, GPIO_DISCONNECTED | LED0_FLAGS);
}

/* LED1 Functions */

int led1_init(void) {
    const struct device *dev = device_get_binding(LED1);
    if (dev == NULL) {
        return DEV_NOT_FOUND;
    }

    LOG_DBG("LED1 Initialized");

    return gpio_pin_configure(dev, LED1_PIN, GPIO_OUTPUT_INACTIVE | LED1_FLAGS);
}

int led1_on(void) {
    const struct device *dev = device_get_binding(LED1);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(1)) {
        LOG_WRN("LED1 Already ON");
    } else {
        LOG_INF("LED1 is ON");
    }

    return gpio_pin_set(dev, LED1_PIN, ON);
}

int led1_off(void) {
    const struct device *dev = device_get_binding(LED1);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(1)) {
        LOG_INF("LED1 is OFF");
    } else {
        LOG_WRN("LED1 is Already OFF");
    }

    return gpio_pin_set(dev, LED1_PIN, OFF);
}

int led1_toggle(void) {
    const struct device *dev = device_get_binding(LED1);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(1)) {
        LOG_INF("LED1 is OFF");
    } else {
        LOG_INF("LED1 is ON");
    }

    return gpio_pin_toggle(dev, LED1_PIN);
}

int led1_deinit(void) {
    const struct device *dev = device_get_binding(LED1);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    LOG_DBG("LED0 Deinitialized OK");

    return gpio_pin_configure(dev, LED1_PIN, GPIO_DISCONNECTED | LED1_FLAGS);
}

/* LED2 Functions */

int led2_init(void) {
    const struct device *dev = device_get_binding(LED2);
    if (dev == NULL) {
        return DEV_NOT_FOUND;
    }

    LOG_DBG("LED2 Initialized");

    return gpio_pin_configure(dev, LED2_PIN, GPIO_OUTPUT_INACTIVE | LED2_FLAGS);
}

int led2_on(void) {
    const struct device *dev = device_get_binding(LED2);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(2)) {
        LOG_WRN("LED2 Already ON");
    } else {
        LOG_INF("LED2 is ON");
    }

    return gpio_pin_set(dev, LED2_PIN, ON);
}

int led2_off(void) {
    const struct device *dev = device_get_binding(LED2);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(2)) {
        LOG_INF("LED2 is OFF");
    } else {
        LOG_WRN("LED2 is Already OFF");
    }

    return gpio_pin_set(dev, LED2_PIN, OFF);
}

int led2_toggle(void) {
    const struct device *dev = device_get_binding(LED2);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(2)) {
        LOG_INF("LED2 is OFF");
    } else {
        LOG_INF("LED2 is ON");
    }

    return gpio_pin_toggle(dev, LED2_PIN);
}

int led2_deinit(void) {
    const struct device *dev = device_get_binding(LED2);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    LOG_DBG("LED2 Deinitialized OK");

    return gpio_pin_configure(dev, LED2_PIN, GPIO_DISCONNECTED | LED2_FLAGS);
}

/* LED3 Functions */

int led3_init(void) {
    const struct device *dev = device_get_binding(LED3);
    if (dev == NULL) {
        return DEV_NOT_FOUND;
    }

    LOG_DBG("LED3 Initialized");

    return gpio_pin_configure(dev, LED3_PIN, GPIO_OUTPUT_INACTIVE | LED3_FLAGS);
}

int led3_on(void) {
    const struct device *dev = device_get_binding(LED3);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(3)) {
        LOG_WRN("LED3 Already ON");
    } else {
        LOG_INF("LED3 is ON");
    }

    return gpio_pin_set(dev, LED3_PIN, ON);
}

int led3_off(void) {
    const struct device *dev = device_get_binding(LED3);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(3)) {
        LOG_INF("LED3 is OFF");
    } else {
        LOG_WRN("LED3 is Already OFF");
    }

    return gpio_pin_set(dev, LED3_PIN, OFF);
}

int led3_toggle(void) {
    const struct device *dev = device_get_binding(LED3);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    if (led_status(3)) {
        LOG_INF("LED3 is OFF");
    } else {
        LOG_INF("LED3 is ON");
    }

    return gpio_pin_toggle(dev, LED3_PIN);
}

int led3_deinit(void) {
    const struct device *dev = device_get_binding(LED3);
    if (dev == NULL) {
        return DEV_NOT_INIT;
    }

    LOG_DBG("LED3 Deinitialized OK");

    return gpio_pin_configure(dev, LED3_PIN, GPIO_DISCONNECTED | LED3_FLAGS);
}

bool led_status(int led_no) {
    gpio_port_value_t value = 0;
    const struct device *dev;

    switch (led_no) {
        case 0:
            dev = device_get_binding(LED0);
            gpio_pin_configure(dev, LED0_PIN, GPIO_INPUT | LED0_FLAGS);
            gpio_port_get_raw(dev, &value);
            if (!(value & (1 << LED0_PIN))) {
                gpio_pin_configure(dev, LED0_PIN,
                                   GPIO_OUTPUT_ACTIVE | LED0_FLAGS);
                return true;
            } else {
                gpio_pin_configure(dev, LED0_PIN,
                                   GPIO_OUTPUT_INACTIVE | LED0_FLAGS);
                return false;
            }

            break;
        case 1:
            dev = device_get_binding(LED1);
            gpio_pin_configure(dev, LED1_PIN, GPIO_INPUT | LED1_FLAGS);
            gpio_port_get_raw(dev, &value);
            if (!(value & (1 << LED1_PIN))) {
                gpio_pin_configure(dev, LED1_PIN,
                                   GPIO_OUTPUT_ACTIVE | LED1_FLAGS);
                return true;
            } else {
                gpio_pin_configure(dev, LED1_PIN,
                                   GPIO_OUTPUT_INACTIVE | LED1_FLAGS);
                return false;
            }
            break;
        case 2:
            dev = device_get_binding(LED2);
            gpio_pin_configure(dev, LED2_PIN, GPIO_INPUT | LED2_FLAGS);
            gpio_port_get_raw(dev, &value);
            if (!(value & (1 << LED2_PIN))) {
                gpio_pin_configure(dev, LED2_PIN,
                                   GPIO_OUTPUT_ACTIVE | LED2_FLAGS);
                return true;
            } else {
                gpio_pin_configure(dev, LED2_PIN,
                                   GPIO_OUTPUT_INACTIVE | LED2_FLAGS);
                return false;
            }
            break;
        case 3:
            dev = device_get_binding(LED3);
            gpio_pin_configure(dev, LED3_PIN, GPIO_INPUT | LED3_FLAGS);
            gpio_port_get_raw(dev, &value);
            if (!(value & (1 << LED3_PIN))) {
                gpio_pin_configure(dev, LED3_PIN,
                                   GPIO_OUTPUT_ACTIVE | LED3_FLAGS);
                return true;
            } else {
                gpio_pin_configure(dev, LED3_PIN,
                                   GPIO_OUTPUT_INACTIVE | LED3_FLAGS);
                return false;
            }
            break;
        default:
            return false;
            break;
    }
}

void no_command(void) { LOG_ERR("invalid command"); }

void init_leds(void) {
    led0_init();
    led1_init();
    led2_init();
    led3_init();
}