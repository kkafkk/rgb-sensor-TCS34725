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

## 🧪 Project Feature: Software Spectrum Calibration

During development and testing, a hardware characteristic of the "silicon photodiode + white LED illumination" combination was identified. The TCS34725 sensor exhibits varying sensitivity to different spectrums, and the blue channel often gets "lost" in noise or is overpowered by other channels, even when scanning blue objects.

**Solution:** 
To ensure stable color classification, a **weighting coefficient block (white balance)** was implemented in the code. Raw data is normalized before comparison according to the specific testing environment:
* The blue channel is artificially amplified (`x1.45` multiplier).
* The green channel is amplified (`x1.2` multiplier).
* The red channel remains the baseline (`x1.0`).

```python
# Channel balancing (White Balance)
r = r_raw * 1.0
g = g_raw * 1.2   
b = b_raw * 1.45
```
This approach achieved high accuracy in recognizing objects without the need to alter the hardware circuit.

## 🛠 Setup and Run
1.Assemble the circuit on a breadboard according to the pinout table.

2.Connect the Raspberry Pi Pico to your computer.

3. Copy the contents of the **main.py** file from this repository. (*The driver for interacting with TCS34725 registers is already integrated into the main script for a quick start*).

4.Run the script on the microcontroller and place colored objects ~5–10 mm away from the sensor.
