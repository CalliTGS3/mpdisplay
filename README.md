# MPDisplay
Display, touch and encoder drivers for [MicroPython](https://github.com/micropython/micropython), [LV_MicroPython](https://github.com/lvgl/lv_micropython) and [LVGL_MicroPython](https://github.com/kdschlosser/lvgl_micropython)

MPDisplay supports SPIBus displays using the included [lcd_bus.py](bus_drivers/lcd_bus.py).  There is also an implementation of I80Bus written in MicroPython in the [bus_drivers](bus_drivers) directory, but it has limitations and is meant for reference rather than production use.  See the notes in bus_drivers for more details about the I80 implementation.  MPDisplay provides touch and encoder drivers, as well as `lv_driver_framework.py` and `lv_config.py` files for use in LV_MicroPython and LVGL_MicroPython.

# Supported platforms
## MicroPython
[MicroPython](https://github.com/micropython/micropython) doesn't include drivers for color displays nor display buses.  The files in [bus_drivers](bus_drivers) provide SPI and I8080 bus drivers written in MicroPython.  The drivers will work with MicroPython's native `framebuf.FrameBuffer` and other methods of creating buffer objects before they are sent to the display.  If you have an ESP32 and are comfortable compiling MicroPython, you may want to use Kevin Schlosser's [lcd_bus](https://github.com/kdschlosser/lcd_bus) C bus drivers with the display drivers in MPDisplay.

## LV_MicroPython
[LV_MicroPython](https://github.com/lvgl/lv_micropython) is the official repository of LVGL integrated into MicroPython.  It does not include bus drivers separated from display drivers and are more difficult to use if your exact display isn't already supported.  The bus and display drivers in MPDisplay work with LV_MicroPython.

## LVGL_MicroPython
[LVGL_MicroPython](https://github.com/kdschlosser/lvgl_micropython) is created by community member Kevin Schlosser.  It has several improvements over the official repo.  Most significant as far as drivers are concerned, it includes very fast SPI, i80 and RGB bus drivers written in C for ESP32 platforms.  You won't need the files in [bus_drivers](bus_drivers) in this case, but it doesn't hurt to have them on your board.  The compiled-in drivers take precedence over the drivers in the filesystem.  The display drivers in MPDisplay will work with the bus drivers from LVGL_MicroPython.

## Micro-GUI on MicroPython
[Micro-GUI](https://github.com/peterhinch/micropython-micro-gui) is a graphics platform written in MicroPython for MicroPython.  It provides its own drivers, but it is modular and may use the drivers provided by MPDisplay.  I have not added support for Micro-GUI yet, but I plan to in the next few weeks.

# Quickstart
Flash your board with your preferred version of MicroPython listed above.

Download the following files and upload them to the /lib folder on your board:
- The [lib](lib) folder, which includes these files:
  	- `busdisplay.py` (required)
  	- `display_simpletest.py` (optional)
  	- `lv_config.py` (required for LVGL targets)
  	- `lv_driver_framework` (required for LVGL targets only)
  	- `lv_touch_test.py` (optional for LVGL targets)
- The `lcd_bus.py` file from [bus_drivers](bus_drivers).  (Not required if you have [lcd_bus](https://github.com/kdschlosser/lcd_bus) or [LVGL_MicroPython](https://github.com/kdschlosser/lvgl_micropython) on ESP32, but it won't hurt to have this file in your /lib folder anyway, so you may as well grab it.)
  	- If your board has an I80 bus, you will also need `i80bus.py` from [bus_drivers](bus_drivers).
- An appropriate `board_config.py` from [board_configs](board_configs).  If you don't find one that matches your hardware, try to find one with the same bus, display controller and MCU as yours.
- The driver for your display controller from [display_drivers](display_drivers)
- The driver for your touchscreen controller (if applicable) from [touch_drivers](touch_drivers)
- If your board uses an IO expander to communicate with the display, for example RGB displays like the ST7701 on the T-RGB board, get the driver from [io_expander_drivers](io_expander_drivers)
- If your board has an encoder, or if you want to add one, get the driver from [encoder_drivers](encoder_drivers).  See [t-embed](board_configs/t-embed) for an example.

You MAY want to edit the `board_config.py` to:
- Adjust the bus frequency for possible higher throughput
- Set the initial brightness of the backlight if backlight_pin is set
- Set the rotation of the display
- Correct any settings that may be necessary for your setup
- Enable an encoder if you add one.  See [t-embed](board_configs/t-embed) for an example.
- Add other non-display related drivers, such as SD card reader or real time clock (not provided)

For use in LVGL, you MAY want to edit the `lv_config.py` to:
- Adjust the buffer size, type and quantity to match your needs
- Set your color format if "lv.COLOR_FORMAT.NATIVE" doesn't work
- Change from blocking mode to non-blocking mode (currently has issues in the C lcd_bus bus drivers)
- Enable encoder(s) if you are using them.  Simply uncomment the last line.

Note, if you have LVGL_MicroPython with lcd_bus compiled in and also have lcd_bus.py in your /lib folder,
the former takes precedence.  In this case, if you want to force MicroPython to use lcd_bus.py, change the include line in your board_config.py from
```
from lcd_bus include ...
```
to
```
from lib.lcd_bus include ...
```

# Usage
No matter which graphics platform you plan to use, it is recommended that you first try the [display_simpletest.py](lib/display_simpletest.py) program.  See the code from that program and [testris](https://github.com/bdbarnett/testris) for non-LVGL usage examples.

If you have LVGL compiled into your MicroPython binary, try [lv_touch_test.py](lib/lv_touch_test.py).  The color of the buttons should be blue when not selected, green when pressed and red when focused.  If the touch points don't line up with the buttons, it provides directions in the REPL on how to find the correct touch rotation masks.  From the REPL type:
```
from lv_touch_test import mask, rotation
```

After getting everything working with the above tests, you're ready to start writing your own code.  Here is an LVGL usage example:
```
import lv_config
import lvgl as lv

scr = lv.screen_active()
button = lv.button(scr)
button.center()
label = lv.label(button)
label.set_text("Test")
```

# Throughput comparison

Running display_simpletest.py, which allocates ten 64x64 blocks and writes them to the screen at random.								
There are 18.75 blocks per screen on the ILI9341 with 320x240 resolution.
Test boards:
- ESP32 without PSRAM (BOARD=ESP32_GENERIC_S3), freq=80,000,000											
- RP2040 (BOARD=ADAFRUIT_QTPY_RP2040), freq=62,500,000											
				
											
Board	|	Bus Driver	|	Byte Swap	|	Alloc	        |	Block/sec	|	FPS	    |
----	|	--------	|	---	        |	---     	|	---	        |	---	    |
ESP32	|	C	        |	false           |	heap_caps	|	825	        |	44.0        |
ESP32	|	C	        |	false	        |	bytearray	|	783	        |	41.8	    |
ESP32	|	C	        |	true	        |	heap_caps	|	495	        |	26.4	    |
ESP32	|	C        	|	true	        |	bytearray	|	487	        |	26.0	    |
ESP32	|	Python	        |	false	        |	heap_caps	|	578	        |	30.8	    |
ESP32	|	Python	        |	false	        |	bytearray	|	549	        |	29.3	    |
ESP32	|	Python	        |	true	        |	heap_caps	|	24	        |	1.3	    |
ESP32	|	Python	        |	true	        |	bytearray	|	24	        |	1.3	    |
RP2040	|	Python	        |	false	        |	bytearray	|	402	        |	21.4	    |
rp2040	|	Python	        |	true	        |	bytearray	|	13	        |	0.7	    |

# My board isn't listed
Please note, I am only providing configs for boards that have an integrated display or, on occasion, boards and displays that may be directly plugged into one another, such as Feather, EYE-SPI, Qualia or QT-Py.  I will not create configs for any setup that requires wiring.  Those setups are generally custom built, but you may use the board configs here as an example.  I am considering creating board configs by request IF you provide a gift certificate to pay for the board from Adafruit, DigiKey, Amazon, Pimoroni or wherever your board is stocked.  I'll post that here if I decide to do that.
