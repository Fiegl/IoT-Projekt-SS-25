import RPi.GPIO as GPIO

RED_PIN = 17
GREEN_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pins nur EINMAL als Output setzen
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

def set_led_status(status):
    if status == "frei":
        GPIO.output(RED_PIN, GPIO.LOW)     # Rot aus
        GPIO.output(GREEN_PIN, GPIO.HIGH)  # Grün an
    elif status == "belegt":
        GPIO.output(RED_PIN, GPIO.HIGH)    # Rot an
        GPIO.output(GREEN_PIN, GPIO.LOW)   # Grün aus
    else:
        GPIO.output(RED_PIN, GPIO.LOW)     # Beide aus
        GPIO.output(GREEN_PIN, GPIO.LOW)

