# Audio player
Plays different audio clips depending on the beacon.

Currently have to copy audio files onto the ESP32 flash using `ampy` instead of playing from SD card.

## Setup
- Download latest micropython firmware for esp32 from https://micropython.org/download/esp32/
- Install firmware using thonny `run` -> `Select interpreter..` -> `install or update firmware`
- Disconnect from esp32 on thonny `run` -> `Disconnect`
- Copy files onto esp32 `ampy -p <port fo esp32> put .*`
