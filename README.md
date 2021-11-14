# beacon-receiver-py
This is a WIP

## Setup
- Install Thonny (https://thonny.org/)
- Plug in ESP32 and press "stop/restart backend"
- After a few seconds enter a new line in the shell and if you see `>>>` you should be able to now run commands on the ESP32.
- Open `main.py` and press the "Run current script" (green button)
- Install https://github.com/TheCacophonyProject/beacon on your RPi.
- Run `dbus-send --system --type=method_call --print-reply --dest=org.cacophony.beacon /org/cacophony/beacon org.cacophony.beacon.Ping` on your RPi and you should see the beacon calls in the shell output on Thonny, and the LED will light up.
- For now to stop sending the beacon from the RPi restart the beacon service with `sudo systemctl restart beacon.service`