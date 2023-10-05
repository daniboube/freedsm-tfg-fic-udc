# FreeDSM Firmware for Raspberry Pi

[![Licence](https://img.shields.io/badge/license-GPLv3-green?style=for-the-badge)](./LICENSE)
[![Official Website](https://img.shields.io/badge/website-Gaia4Sustainability-orange?style=for-the-badge)](http://gaia4sustainability.eu)

The FreeDSM photometer is an open hardware and open software solution for citizen light pollution monitoring based on IoT technologies. It has been created under the idea of being a low-cost (around 20-30 euros), easy-to-build and easy-to-use device, so everyone with minimum knowledge about soldering or electronics can make their own. In this repository you will find the source code necessary to make the different sensors work when connected to a Raspberry Pi Zero. It should be noted that this is an early prototype, and not a finished version, since only the work presented as my Final Degree Project in Computer Engineering is included here. Below is a list of the components needed to build it.

## Table of contents

- [Requirements](#requirements)
    - [Software](#software)
    - [Hardware](#hardware)
- [Software setup](#software-setup)
    - [Flash device](#flash-device)
    - [Set Raspberry workspace](#set-raspberry-workspace)
    - [Create a service](#create-a-service)
    - [Add Wifi Network](#add-wifi-network)
- [Hardware-setup](#hardware-setup)
- [Final notes](#final-notes)

## Requirements

### Software

- [Raspberry Pi Imager Tool](https://www.raspberrypi.com/software/)

### Hardware

| Component | Description | Units | Online link | Documentation |
| --- | --- | --- | --- | --- |
| Raspberry PI Zero W | Raspberry PI computer model Zero Wireless (Wifi and Bluetooth communication) | 1 | [Link](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) | [Link](https://www.raspberrypi.com/documentation/computers/getting-started.html) |
| TSL2591 | Optical light I2C sensor | 1 | [Link](https://es.aliexpress.com/item/1005003630281406.html) | [Link](https://learn.adafruit.com/adafruit-tsl2591/assembly) |
| AHT10 | Temperature and Humidity I2C sensor | 1 | [Link](https://es.aliexpress.com/item/1005001621672964.html) |  |
| MPU6050 | Gyroscope and acelerometer I2C sensor | 1 | [Link](https://es.aliexpress.com/item/32346328217.html) | [Link](https://learn.adafruit.com/mpu6050-6-dof-accelerometer-and-gyro/python-and-circuitpython) |
| GPS Neo6mV2 | GPS module with anthena | 1 | [Link](https://es.aliexpress.com/item/1005001635722164.html) | [Link](https://github.com/FranzTscharf/Python-NEO-6M-GPS-Raspberry-Pi) |
| Lenses | 60 degrees PMMA lenses to put on top of the light sensor, ensuring that most of the photons are caught by the photodiodes in extremely low light conditions | 1 | [Link](https://www.aliexpress.us/item/1005003717171920.html?gatewayAdapt=4itemAdapt) |  |
| Screws | M.2 screws x6mm tall | 14 | [Link](https://es.aliexpress.com/item/1005003898938876.html) |  |
| Jumping wires | Female-Female jumping wires (short) | 20 | [Link](https://es.aliexpress.com/item/1005005616699410.html) |  |
| SD Card | at least 32 GB SD Card | 1 | [Link](https://es.aliexpress.com/item/1005004094130339.html) |  |
| SD Card reader | USB reader for SD Cards | 1 | [Link](https://es.aliexpress.com/item/1005005903040090.html) |  |

## Software setup

### Flash device

Connect the card reader with the micro SD to the computer and open the Raspberry Pi Imager tool. Select the following settings:

- **Operating System**: Raspberry Pi OS Lite (32-bit)
- **Storage**: The SD Card connected to the computer

Before flashing your device, click on the gear icon to access advanced options. Use the following configuration:

- **Set hostname**: No
- **Enable SSH**: Yes
    - *Use password authentication*
- **Set username and password**: Yes
    - *Username*: pi
    - *Password*: raspfreedsm
- **Configure wireless LAN**: Yes
    - *SSID*: (your domestic Wifi ssid)
    - *Password*: (your domestic Wifi password)
    - *Wireless LAN country*: (your country code)
- **Set locale settings**: Yes
    - *Time zone*: (your local timezone)
    - *Keyboard layout*: (your keyboard settings)
 
Be sure to check the *to always use* option in the drop-down menu at the top of the advanced options screen. Leave the *Persistent settings* as default. Save the settings and start the flashing process.

### Set Raspberry workspace

Now, clone this repository into your Raspberry using the following commands:

```bash
git clone https://github.com/daniboube/freedsm-tfg-fic-udc

cd freedsm-tfg-fic-udc
```

You will need to install the Python libreries now. Using the default Python environment, type the following command to achieve this:

```bash
sudo apt-get install pip
sudo pip install -r ./requirements.txt
```

### Create a service

The next step will be to create a service in the OS that is responsible for running this application at startup. For this, we will use systemd.

```bash
# Create the unit file
sudo nano /lib/systemd/system/freedsm.service

# Add this content inside it
[Unit]
Description=Freedsm-Firmware Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/freedsm-tfg-fic-udc/main.py

[Install]
WantedBy=multi-user.target
```

Next, configure the files to have the correct permissions and add the file to systemd:

```bash
# Change the default permisions
sudo chmod 644 /lib/systemd/system/freedsm.service

# Add the service to Systemd
sudo systemctl daemon-reload
sudo systemctl enable freedsm.service
```

### Add Wifi network

Finally, add the Wi-Fi network to which the machine will connect once it is deployed. This step is optional, only in case the Raspberry does not have Ethernet connectivity.

```bash
# Open the following file
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# Add these lines to the end of it
network={
    ssid="Your other SSID Name"
    psk="Your other WiFI Password"
    key_mgmt=WPA-PSK
}
```

After this, restart the device and make sure everything is working correctly. You chan check the status of your FreeDSM with the command:

```bash
systemctl status freedsm
```

## Hardware setup

Although there is no complete diagram on how to assemble the components in the case, below are the wiring diagrams for the different modules and sensors with respect to the Raspberry Pi.

- [TSL2591](https://github.com/daniboube/freedsm-tfg-fic-udc/assets/50242249/a952c098-11e5-414b-87b5-9d07e4f2f252)
- [AHT10](https://github.com/daniboube/freedsm-tfg-fic-udc/assets/50242249/b9b49af8-2dc8-4a0f-9fa1-b462a3c23307)
- [MPU6050](https://github.com/daniboube/freedsm-tfg-fic-udc/assets/50242249/9fb60c81-5de3-48f8-a797-fd76370a446b)
- [GPS NEO6mV2](https://github.com/daniboube/freedsm-tfg-fic-udc/assets/50242249/16060026-2da3-473f-970a-5de3fc8a9dca)

## Final notes

If you want to know more about the context of the project or the device (how it is built, how it is used, results obtained, etc.), you can review the complete report of the work published in the [institutional repository](https://ruc.udc.es/dspace/handle/2183/32824) of the University of A Coruña. To find out more about the current status of the project, carried out by researchers from the Universities of A Coruña, Vigo and Barcelona, visit the [official website](http://gaia4sustainability.eu) of the Gaia4Sustainability project.

As a reminder, this work is licensed under a [GNU General Public License V.3](https://www.gnu.org/licenses/gpl-3.0.html), so you are free to use it as you want.
