import time
import ustruct
from machine import Pin, I2C

# ================= ДРАЙВЕР TCS34725 =================
_TCS34725_ADDRESS = 0x29
_COMMAND_BIT = 0x80
_ENABLE = 0x00
_ENABLE_AEN = 0x02
_ENABLE_PON = 0x01
_ATIME = 0x01
_CONTROL = 0x0F
_CDATAL = 0x14
_RDATAL = 0x16
_GDATAL = 0x18
_BDATAL = 0x1A

_INTEGRATION_TIME_50MS = 0xEB
_GAIN_4X = 0x01

class TCS34725:
    def __init__(self, i2c, address=_TCS34725_ADDRESS):
        self.i2c = i2c
        self.address = address
        self._write_byte(_ENABLE, _ENABLE_PON)
        time.sleep(0.01)
        self._write_byte(_ENABLE, _ENABLE_PON | _ENABLE_AEN)
        self._write_byte(_ATIME, _INTEGRATION_TIME_50MS)
        self._write_byte(_CONTROL, _GAIN_4X)

    def _write_byte(self, reg, value):
        self.i2c.writeto_mem(self.address, reg | _COMMAND_BIT, bytearray([value]))

    def _read_word(self, reg):
        data = self.i2c.readfrom_mem(self.address, reg | _COMMAND_BIT, 2)
        return ustruct.unpack('<H', data)[0]

    def read(self):
        c = self._read_word(_CDATAL)
        r = self._read_word(_RDATAL)
        g = self._read_word(_GDATAL)
        b = self._read_word(_BDATAL)
        return r, g, b, c

# ================= НАСТРОЙКА СВЕТОДИОДОВ =================
led_red = Pin(13, Pin.OUT)
led_green = Pin(14, Pin.OUT)
led_blue = Pin(15, Pin.OUT)
led_white = Pin(16, Pin.OUT)

def turn_off_all():
    led_red.value(0)
    led_green.value(0)
    led_blue.value(0)
    led_white.value(0)

# Инициализация I2C на GP4 (SDA) и GP5 (SCL)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
sensor = TCS34725(i2c)

print("--- Индикатор цвета активен ---")

while True:
    r_raw, g_raw, b_raw, c = sensor.read()
    turn_off_all()
    
    # --- Балансировка каналов (весовые коэффициенты) ---
    r = r_raw * 1.0
    g = g_raw * 1.2   
    b = b_raw * 1.45   
    
    # 1. Проверка условия на белый/темный (по сырым данным)
    if 0 < r_raw < 60 and 0 < g_raw < 60 and 0 < b_raw < 60:
        led_white.value(1)
        print("WHITE / BLACK (R:", r_raw, "G:", g_raw, "B:", b_raw, ")")
        
    # 2. Определение ярких цветов с учетом коэффициентов
    elif c > 20:
        if r > g and r > b:
            led_red.value(1)
            print("RED -> R:", int(r), "G:", int(g), "B:", int(b))
        elif g > r and g > b:
            led_green.value(1)
            print("GREEN -> R:", int(r), "G:", int(g), "B:", int(b))
        elif b > r and b > g:
            led_blue.value(1)
            print("BLUE -> R:", int(r), "G:", int(g), "B:", int(b))
            
    time.sleep(0.4)