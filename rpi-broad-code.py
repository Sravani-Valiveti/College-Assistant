## sudo apt-get install python-rpi.gpio

## GPIO 23 = 16 for input 
##GPIO 24 = 18 for output
## pin 14 and 20 ground
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.OUT)

start = GPIO.input(23)
if (start):
    #go to main screen from exit screen (do in global things)
    pass

## in exxit function after screen transition
GPIO.output(24, GPIO.HIGH)
#GPIO.output(24, True) Alternate method
time.sleep(3)
GPIO.output(24, GPIO.LOW)

GPIO.cleanup()
