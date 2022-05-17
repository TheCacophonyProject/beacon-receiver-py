# Programmed onto an ESP32 using Thonny

import bluetooth
import ubinascii
import sys
import time
import machine

devices = {}
pin = machine.Pin(2, machine.Pin.OUT)

recording_type = 2
classification_type = 3

labels = {
    0: "bird",
    1: "cat",
    2: "false-positive",
    3: "hedgehog",
    4: "human",
    5: "leporidae",
    6: "mustelid",
    7: "possum",
    8: "rodent",
    9: "vehicle",
    10: "wallaby",
}

dev = {"scanning": False, "last_received_time": 0}


def bt_irq(event, data):
    if event == 5:
        addr_type, addr, adv_type, rssi, adv_data = data
        # Check that data is long enough
        l = adv_data[0]
        if l < 9 or l != len(adv_data) - 1:
            return
        ad_type = adv_data[1]
        man_id = int.from_bytes(adv_data[2:4], "big")
        version = adv_data[4]
        # Check that data is from one of our cameras and a version that
        if ad_type != 0xFF or man_id != 0x1212 or version != 0x01:
            return
        # print("======")
        # print(ubinascii.hexlify(adv_data))

        # Check the CRC of the data
        crc = int.from_bytes(adv_data[-4:], "big")
        crc_data = ubinascii.crc32(adv_data[4:-4])
        if crc != crc_data:
            print("CRC did not match")

        device_id = int.from_bytes(adv_data[5:7], "big")
        data_type = adv_data[7]
        data = adv_data[8:-4]

        process_data(device_id, data_type, data)

    elif event == 6:
        dev["scanning"] = False


def process_data(device_id, data_type, data):
    print("New beacon call!")
    print("Device ID:", device_id)
    dev["last_received_time"] = time.ticks_ms()
    if data_type == recording_type:
        print("Recording started")
    elif data_type == classification_type:
        handle_classification(data)

def handle_classification(classifications):
    class_len=int(classifications[0])
    print("No of classifications: ",class_len)
    top_pick = labels[int(classifications[1])]
    top_confidence = int(classifications[2])
    print("1:", top_pick, " ", top_confidence, "%")
    if class_len>1:
        second_pick = labels[int(classifications[3])]
        second_confidence = int(classifications[4])
        print("2:", second_pick, " ", second_confidence, "%")

print("starting")
ble = bluetooth.BLE()
while True:
    ble.active(True)
    ble.irq(bt_irq)
    dev["scanning"] = True
    ble.gap_scan(3000, 30000, 30000)
    while dev["scanning"]:
        pin.value(dev["last_received_time"] > time.ticks_ms() - 5000)
        time.sleep(0.2)
