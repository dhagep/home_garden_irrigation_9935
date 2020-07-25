import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
print "LED ON"
GPIO.output(21,GPIO.HIGH)
GPIO.output(20,GPIO.HIGH)
time.sleep(10)
print "LED OFF"
GPIO.output(21,GPIO.LOW)
GPIO.output(20,GPIO.LOW)
