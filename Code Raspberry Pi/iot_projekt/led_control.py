import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup_pins(red_pin, green_pin):
    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.setup(green_pin, GPIO.OUT)

def led_off(red_pin, green_pin):
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.LOW)

def led_red(red_pin, green_pin):
    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.LOW)

def led_green(red_pin, green_pin):
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.HIGH)

def set_led_status(gpio_red, gpio_green, status):
    setup_pins(gpio_red, gpio_green)

    if status == "frei":
        led_green(gpio_red, gpio_green)
    elif status == "belegt":
        led_red(gpio_red, gpio_green)
    else:
        led_off(gpio_red, gpio_green)


