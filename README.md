# 🎨 Optical Color Indicator on Raspberry Pi Pico (TCS34725)

This project is a compact device based on the **Raspberry Pi Pico** microcontroller that detects the dominant color of an object (e.g., colored clay) and lights up the corresponding LED. The project is built on a breadboard and utilizes the **TCS34725** I2C color sensor.

## 🚀 How it Works

The algorithm continuously reads the RGB channels and the overall illuminance (Clear) level from the sensor.
* If an object with a distinct color (Red, Green, or Blue) is detected, the corresponding colored LED lights up.
* If all channel values fall within a low range (1 to 59), indicating a white/dark background or low reflectivity, the white LED turns on.
* If the illuminance drops below the noise threshold (meaning nothing is in front of the sensor), all LEDs turn off.

## ⚙️ Hardware

* **Microcontroller:** Raspberry Pi Pico (RP2040)
* **Sensor:** TCS34725 RGB Color Sensor
* **Indicators:** 4 LEDs (Red, Green, Blue, White) + 4 current-limiting resistors (220–330 Ohm)
* **Assembly:** Breadboard

### 🔌 Pinout

| Component | Pico Pin | Note |
| :--- | :--- | :--- |
| **TCS34725 SDA** | `GP4` | I2C0 Bus |
| **TCS34725 SCL** | `GP5` | I2C0 Bus |
| **TCS34725 VIN** | `3V3 (OUT)` | 3.3V Power |
| **TCS34725 GND** | `GND` | Common Ground |
| **LED Red** | `GP13` | Anode (connect to GND via resistor) |
| **LED Green** | `GP14` | Anode (connect to GND via resistor) |
| **LED Blue** | `GP15` | Anode (connect to GND via resistor) |
| **LED White** | `GP16` | Anode (connect to GND via resistor) |

## 🏗️ System Architecture
```text
[ TCS34725 Sensor ] --(I2C0 / GP4, GP5)--> [ RP2040 Pico ] --(GPIO GP13-GP16)--> [ 4-LED Status Array ]
                                           (MicroPython)                          [ Red/Green/Blue/White ]
```
## 📸 Showcase

https://github.com/user-attachments/assets/14d08c5f-961d-4658-bcd3-8cda4e6854aa

<img width="800" height="480" alt="image" src="https://github.com/user-attachments/assets/91f8ff44-b2d2-4c2a-a60c-2fc2c99d7290" />

<img width="960" height="1280" alt="image" src="https://github.com/user-attachments/assets/023d823e-90ac-4706-bb9b-688fba644925" />

Hardware Assembly & Wiring

## 🛠️ Development Log & Engineering Challenges
Spectral Sensitivity Imbalance (The Blue Wavelength Attenuation)
*The Problem*: When scanning blue test materials, the sensor's raw green and red readings routinely overwhelmed the blue channel. This occurred because silicon photodiodes are inherently more responsive to longer wavelengths, and standard on-board white LEDs have heavy green/yellow spectral peaks.

*Solution*: Implemented software-side digital balancing inside the main processing loop. Applying scaling coefficients (b_raw * 1.45, g_raw * 1.2, r_raw * 1.0) normalized the channels, allowing unambiguous detection of blue targets.
* The blue channel is artificially amplified (`x1.45` multiplier).
* The green channel is amplified (`x1.2` multiplier).
* The red channel remains the baseline (`x1.0`).

```python
# Channel balancing (White Balance)
r = r_raw * 1.0
g = g_raw * 1.2   
b = b_raw * 1.45
```
### Driver Decoupling & Deployment Optimization
*Initial Plan*: Rely on an external multi-file tcs34725.py module loaded alongside main.py.

*The Problem*: In pure embedded environments and lightweight IDEs, multi-file imports often create path resolution overhead and upload fragmentation.

*Solution*: Refactored the core I2C register interface directly into a compact class within main.py, reducing upload complexity and eliminating import errors.

### Ambiguity in Neutral / Low-Reflectance States
*The Problem*: White and matte black surfaces reflect light uniformly across all channels at low-to-medium amplitudes, causing erratic bouncing between chromatic flags.

*Solution*: Implemented a dedicated lower-bound boundary condition (0 < raw < 60 across all channels simultaneously) routed directly to a designated neutral white LED indicator.

## 🛠 Setup and Run
1.Assemble the circuit on a breadboard according to the pinout table.

2.Connect the Raspberry Pi Pico to your computer.

3. Copy the contents of the **main.py** file from this repository. (*The driver for interacting with TCS34725 registers is already integrated into the main script for a quick start*).

4.Run the script on the microcontroller and place colored objects ~5–10 mm away from the sensor.

## 👤 Author
Katya — @kkafkk

## 📝 License
This project is open-source and available under the MIT License.
