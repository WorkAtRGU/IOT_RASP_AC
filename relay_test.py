import RPi.GPIO as GPIO
import time

fan_channel_1 = 5
fan_channel_2 = 6
gas_sensor_channel = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_channel_1, GPIO.OUT)
GPIO.setup(fan_channel_2, GPIO.OUT)
GPIO.setup(gas_sensor_channel, GPIO.IN)

def fan_on(pin):
    GPIO.output(pin, GPIO.LOW)
    print("setting GPIO.BCM pin: {} high".format(pin))

def fan_off(pin):
    GPIO.output(pin, GPIO.HIGH)
    print("setting GPIO.BCM pin: {} low".format(pin))
    
def check_pin_input(pin):
    status = GPIO.input(pin)
    print("pin: {}, is: {}".format(pin, status))
    return status

if __name__ == '__main__':
    try:
        fan_on(fan_channel_1)
        time.sleep(1)
        fan_on(fan_channel_2)
        time.sleep(1)
        check_pin_input(gas_sensor_channel)
        time.sleep(3)
        fan_off(fan_channel_1)
        time.sleep(1)
        fan_off(fan_channel_2)
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()