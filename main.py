import RPi.GPIO as GPIO
from i2c.device import TCA9548A
from i2c.device import SHT20
from i2c.com import *

muxer = TCA9548A(0x70, "Muxer")

def main():
    air = SHT20(TCA9548A.CHANNEL_4, muxer.get_address(), "Air sensor")

    change_mux_channel(muxer, air)
    humidity, cTemp, fTemp = get_temp_hum(air)

    print("Relative Humidity is : %.2f %%" % humidity)
    print("Temperature in Celsius is : %.2f C" % cTemp)
    print("Temperature in Fahrenheit is : %.2f F" % fTemp)


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    gpio = muxer.get_address_gpio()
    for pin in gpio:
        state = gpio[pin]
        print("Setting pin " + str(pin) + " to " + str(state))
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, state)
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()