from i2c.device import SHT20
from i2c.device import TCA9548A
from i2c.device import I2CMuxDevice
from i2c.bus import SimpleSMBus

import time

def get_temp_hum(dev:SHT20):
    humidity = -1
    cTemp = -1
    fTemp = -1
    with SimpleSMBus(dev) as bus:
        bus.wb(SHT20.TEMPERATURE_NO_HOLD)
        time.sleep(0.5)
        data0 = bus.rb()
        data1 = bus.rb()

        temp = data0 * 256 + data1
        cTemp = -46.85 + ((temp * 175.72) / 65536.0)
        fTemp = cTemp * 1.8 + 32

        bus.wb(SHT20.HUMIDITY_NO_HOLD)
        time.sleep(0.5)

        data0 = bus.rb()
        data1 = bus.rb()

        humidity = data0 * 256 + data1
        humidity = -6 + ((humidity * 125.0) / 65536.0)

    return [humidity, cTemp, fTemp]

def change_mux_channel(mux:TCA9548A, dev:I2CMuxDevice):
    with SimpleSMBus(mux) as bus:
        bus.wb(dev.get_mux_channel())