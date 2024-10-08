""" Waveshare Round Display for XIAO GC9A01 240x240 display on ESP32-S3-LCD-1.28"""

from spibus import SPIBus
from gc9a01 import GC9A01
from machine import Pin, I2C
from eventsys.devices import Devices, Broker

display_bus = SPIBus(
    dc=8,
    cs=9,
    mosi=11,
    miso=None,
    sclk=10,
    host=1,
    tx_only=True,
    freq=60_000_000,
    spi_mode=0,
    cmd_bits=8,
    param_bits=8,
    lsb_first=False,
    dc_low_on_data=False,
    cs_high_active=False,
)

display_drv = GC9A01(
    display_bus,
    width=240,
    height=240,
    colstart=0,
    rowstart=0,
    rotation=0,
    mirrored=False,
    color_depth=16,
    bgr=True,
    reverse_bytes_in_word=True,
    invert=True,
    brightness=1.0,
    backlight_pin=40,
    backlight_on_high=True,
    reset_pin=12,
    reset_high=False,
    power_pin=None,
    power_on_high=True,
)
