/**
 ******************************************************************************
 * @file           : led_driver.h
 * @brief          : The LED Driver provides functionality to control onboard
 * LEDs in a Zepher environment.
 ******************************************************************************
 * @attention Built for CSSE4011 Semester 1 2022
 *
 * @author: Blake Rowden
 * @date: 12/03/2022
 * ***************************************************************************
 */

#ifndef LED_DRIVER_H
#define LED_DRIVER_H

/* Public Error Defines ------------------------------------------------------*/
#define DEV_NOT_FOUND -1
#define DEV_NOT_INIT -2

/* Device Tree Macros --------------------------------------------------------*/

#define LED0_NODE DT_ALIAS(led0)
#define LED1_NODE DT_ALIAS(led1)
#define LED2_NODE DT_ALIAS(led2)
#define LED3_NODE DT_ALIAS(led3)

/* LED0 */

#if DT_NODE_HAS_STATUS(LED0_NODE, okay)
#define LED0 DT_GPIO_LABEL(LED0_NODE, gpios)
#define LED0_PIN DT_GPIO_PIN(LED0_NODE, gpios)
#define LED0_FLAGS DT_GPIO_FLAGS(LED0_NODE, gpios)
#else
/* A build error here means your board isn't set up to blink an LED. */
#error "Unsupported board: led0 devicetree alias is not defined"
#define LED0 ""
#define LED0_PIN 0
#define LED0_FLAGS 0
#endif

/* LED1 */

#if DT_NODE_HAS_STATUS(LED1_NODE, okay)
#define LED1 DT_GPIO_LABEL(LED1_NODE, gpios)
#define LED1_PIN DT_GPIO_PIN(LED1_NODE, gpios)
#define LED1_FLAGS DT_GPIO_FLAGS(LED1_NODE, gpios)
#else
/* A build error here means your board isn't set up to blink an LED. */
#error "Unsupported board: led1 devicetree alias is not defined"
#define LED1 ""
#define LED1_PIN 0
#define LED1_FLAGS 0
#endif

/* LED2 */

#if DT_NODE_HAS_STATUS(LED2_NODE, okay)
#define LED2 DT_GPIO_LABEL(LED2_NODE, gpios)
#define LED2_PIN DT_GPIO_PIN(LED2_NODE, gpios)
#define LED2_FLAGS DT_GPIO_FLAGS(LED2_NODE, gpios)
#else
/* A build error here means your board isn't set up to blink an LED. */
#error "Unsupported board: led2 devicetree alias is not defined"
#define LED2 ""
#define LED2_PIN 0
#define LED2_FLAGS 0
#endif

/* LED3 */

#if DT_NODE_HAS_STATUS(LED3_NODE, okay)
#define LED3 DT_GPIO_LABEL(LED3_NODE, gpios)
#define LED3_PIN DT_GPIO_PIN(LED3_NODE, gpios)
#define LED3_FLAGS DT_GPIO_FLAGS(LED3_NODE, gpios)
#else
/* A build error here means your board isn't set up to blink an LED. */
#error "Unsupported board: led3 devicetree alias is not defined"
#define LED3 ""
#define LED3_PIN 0
#define LED3_FLAGS 0
#endif

/* Public Enums --------------------------------------------------------------*/

/**
 * @brief Describes the possible states of the LED, used to create logs
 *
 */
typedef enum
{
  LED_INIT,
  LED_ON,
  LED_OFF,
  LED_DEINIT,
  LED_ALREADY_ON
} led_state_t;

/* Public Function Declarations ----------------------------------------------*/

/**
 * @brief Initialises LED0 to be used as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led0_init(void);

/**
 * @brief Turns LED0 on
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led0_on(void);

/**
 * @brief Turns LED0 off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led0_off(void);

/**
 * @brief Toggles LED0 on/off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led0_toggle(void);

/**
 * @brief Deitialises LED0 as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led0_deinit(void);

/**
 * @brief Initialises LED1 to be used as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led1_init(void);

/**
 * @brief Turns LED1 on
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led1_on(void);

/**
 * @brief Turns LED1 off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led1_off(void);

/**
 * @brief Toggles LED1 on/off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led1_toggle(void);

/**
 * @brief Deitialises LED1 as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led1_deinit(void);

/**
 * @brief Initialises LED2 to be used as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led2_init(void);

/**
 * @brief Turns LED2 on
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led2_on(void);

/**
 * @brief Turns LED2 off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led2_off(void);

/**
 * @brief Toggles LED2 on/off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led2_toggle(void);

/**
 * @brief Deitialises LED2 as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */

int led2_deinit(void);

/**
 * @brief Initialises LED2 to be used as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led3_init(void);

/**
 * @brief Turns LED2 on
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led3_on(void);

/**
 * @brief Turns LED2 off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led3_off(void);

/**
 * @brief Toggles LED2 on/off
 *
 * @return int 0 on success, negative errno code on failure.
 */
int led3_toggle(void);

/**
 * @brief Deitialises LED2 as an output
 *
 * @return int 0 on success, negative errno code on failure.
 */

int led3_deinit(void);

/**
 * @brief Used to log an invalid LED command
 *
 */
void no_command(void);

/**
 * @brief Initialises all LEDs to be used as outputs
 *
 */
void init_leds(void);

#endif // LED_DRIVER_H