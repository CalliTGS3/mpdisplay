""" QTPy ESP32 Pico with EyeSPI and ILI9341 2.8" display """

from displayio import release_displays
release_displays()

from fourwire import FourWire
from ili9341 import ILI9341
from adafruit_focaltouch import Adafruit_FocalTouch
from mpdisplay import Devices
import board


display_bus = FourWire(
    board.SPI(),
    command=board.RX,
    chip_select=board.TX,
    baudrate=30_000_000,
#     reset=None,
#     polarity=0,
#     phase=0,
)

display_drv = ILI9341(
    display_bus,
    width=240,
    height=320,
    colstart=0,
    rowstart=0,
    rotation=0,
    mirrored=False,
    color_depth=16,
    bgr=True,
    reverse_bytes_in_word=True,
    invert=False,
    brightness=1.0,
    backlight_pin=None,
    backlight_on_high=True,
    reset_pin=None,
    reset_high=True,
    power_pin=None,
    power_on_high=True,
)

i2c = board.I2C()
touch_drv = Adafruit_FocalTouch(i2c)
touch_rotation_table=(6, 3, 0, 5)

def touch_read_func():
    touches = touch_drv.touches
    if len(touches):
        return touches[0]['x'], touches[0]['y']
    return None

touch_dev = display_drv.create_device(
    type=Devices.TOUCH,
    read=touch_read_func,
    data=touch_rotation_table,
)
