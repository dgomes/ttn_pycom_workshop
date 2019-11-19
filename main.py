import pycom
from network import LoRa
import time
import binascii
import socket

from machine import Pin
from onewire import DS18X20
from onewire import OneWire


print("TTN Example v0")
# DS18B20 data line connected to pin P10
ow = OneWire(Pin('G16'))
d = DS18X20(ow)

pycom.heartbeat(False)
pycom.rgbled(0x00ff00)

lora = LoRa(mode=LoRa.LORAWAN)

app_eui = binascii.unhexlify('70B3D57EF0003CDF')
app_key = binascii.unhexlify('221D0C89D6393F66C01EFE5588E99D65')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet... Have you registered device ID? Mine is:')
    print(binascii.hexlify(lora.mac()).upper().decode('utf-8'))



print('Network joined!')

# setup a socket to transmit data
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)


while True:
    #create message
    d.start_conversion()
    time.sleep(1)
    temperature=d.read_temp_async()
    print(temperature)
    msg = (int(temperature*100)).to_bytes(4, 'little')
    print(msg)
    
    pycom.rgbled(0x0000ff)
    s.send(msg)
    time.sleep(1)
    pycom.rgbled(0x000000)

    #rest for a while
    time.sleep(30)