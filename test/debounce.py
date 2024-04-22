import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

s = ""
t = time.time()
while time.time() - t < 0.5:
	s += str(GPIO.input(26))

print(s)
