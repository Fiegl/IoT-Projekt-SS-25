Import RPi.GPIO as GPIO

RED_PIN = 17
GREEN_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.seup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

def led_off():
	GPIO.output(RED_PIN, GPIO.LOW)
	GPIO.output(GREEN_PIN, GPIO.LOW)

def led_red():
	GPIO.output(RED_PIN, GPIO.HIGH)
	GPIO.output(GREEN_PIN, GPIO.LOW)

def led_green():
	GPIO.output(RED_PIN, GPIO.LOW)
	GPIO.output(GREEN_PIN, GPIO.High)

def cleanup_gpio():
	led_off()
	GPIO.cleanup()