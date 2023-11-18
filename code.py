import time
import board
import digitalio
#import analogio

import adafruit_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService

btn = digitalio.DigitalInOut(board.D4)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#vbatt = analogio.AnalogIn(board.VBATT)

#def get_voltage(pin):
#    return (pin.value * 5.0) / 65536

ble = adafruit_ble.BLERadio()
ble.name = "Big-Snooze"
# Using default HID Descriptor.
hid = HIDService()
device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                 manufacturer="Tea and Tech Time")
advertisement = ProvideServicesAdvertisement(hid)
cc = ConsumerControl(hid.devices)

muted = False
command = None
advertising = False
connection_made = False
#print("let's go!")

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
    #print(get_voltage(vbatt))
    
    if not ble.connected:
        connection_made = False
        if not advertising:
            ble.start_advertising(advertisement)
            advertising = True
        continue
    else:
        if connection_made:
            pass
        else:
            connection_made = True

    advertising = False

    if not btn.value:
    	#print("Snoozing")
    	command = ConsumerControlCode.VOLUME_INCREMENT
    	cc.send(command)
    	time.sleep(0.1)
    	command = ConsumerControlCode.VOLUME_DECREMENT
    	cc.send(command)
    	
        while not btn.value:  # debounce
            time.sleep(0.1)

