# Programmed onto an ESP32 using Thonny

import bluetooth
import ubinascii
import sys
import time
import machine

devices = {}
pin = machine.Pin(2, machine.Pin.OUT)

dev={
    "scanning":False,
    "last": 0,
    }

def bt_irq(event, data):
    if event == 5:
        addr_type, addr, adv_type, rssi, adv_data = data
        # Check that data is long enough
        l = adv_data[0]
        if l < 9 or l != len(adv_data)-1:
            return
        ad_type = adv_data[1]
        man_id = int.from_bytes(adv_data[2:4], 'big')
        version = adv_data[4]
        # Check that data is from one of our cameras and a version that 
        if ad_type != 0xFF or man_id != 0x1212 or version != 0x01:
            return
        print("======")
        print(ubinascii.hexlify(adv_data))
        
        # Check the CRC of the data
        crc = int.from_bytes(adv_data[-4:], 'big')
        crc_data = ubinascii.crc32(adv_data[4:-4])
        if crc != crc_data:
            print("CRC did not match")
            
        device_id = int.from_bytes(adv_data[5:7], 'big')
        data_type = adv_data[7]
        data = adv_data[8:-4]
        
        process_data(device_id, data_type, data)
        
    elif event == 6:
        dev["scanning"] = False

def process_data(device_id, data_type, data):
    #TODO
    print("New beacon call!")
    print("Device ID:", device_id)
    print("Data type:", data_type)
    print("Data:", ubinascii.hexlify(data))

ble = bluetooth.BLE()
while True:
    ble.active(True)
    ble.irq(bt_irq)
    dev["scanning"] = True
    ble.gap_scan(3000, 30000, 30000)
    while dev["scanning"]:
        #if dev["last"] > time.ticks_ms():
        pin.value(dev["last"] > time.ticks_ms())
        time.sleep(0.2)
