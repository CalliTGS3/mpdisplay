# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Tyler Crumpton
#
# SPDX-License-Identifier: MIT
"""
`gc9a01`
================================================================================

displayio driver for GC9A01 TFT LCD displays


* Author(s): Tyler Crumpton

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tylercrumpton/CircuitPython_GC9A01.git"

from busdisplay import BusDisplay

_INIT_SEQUENCE = bytearray(
    b"\x28\x80\x78" # Display OFF (28h) and delay(20)
    b"\xEF\x00" # Inter Register Enable2 (EFh)
    b"\xEB\x01\x14"
    b"\xFE\x00" # Inter Register Enable1 (FEh)
    b"\xEF\x00" # Inter Register Enable2 (EFh)
    b"\xEB\x01\x14"
    b"\x84\x01\x40"
    b"\x85\x01\xFF"
    b"\x86\x01\xFF"
    b"\x87\x01\xFF"
    b"\x88\x01\x0A"
    b"\x89\x01\x21"
    b"\x8A\x01\x00"
    b"\x8B\x01\x80"
    b"\x8C\x01\x01"
    b"\x8D\x01\x01"
    b"\x8E\x01\xFF"
    b"\x8F\x01\xFF"
    b"\xB6\x02\x00\x00" # Display Function Control (B6h) [S1→S360 source, G1→G32 gate]
    b"\x3A\x01\x05" # 05 COLMOD: Pixel Format Set (3Ah) [16 bits / pixel]
    b"\x90\x04\x08\x08\x08\x08"
    b"\xBD\x01\x06"
    b"\xBC\x01\x00"
    b"\xFF\x03\x60\x01\x04"
    b"\xC3\x01\x13" # Power Control 2 (C3h) [VREG1A = 5.06, VREG1B = 0.68]
    b"\xC4\x01\x13" # Power Control 3 (C4h) [VREG2A = -3.7, VREG2B = 0.68]
    b"\xC9\x01\x22" # Power Control 4 (C9h)
    b"\xBE\x01\x11"
    b"\xE1\x02\x10\x0E"
    b"\xDF\x03\x21\x0c\x02"
    b"\xF0\x06\x45\x09\x08\x08\x26\x2A" # SET_GAMMA1 (F0h)
    b"\xF1\x06\x43\x70\x72\x36\x37\x6F" # SET_GAMMA1 (F1h)
    b"\xF2\x06\x45\x09\x08\x08\x26\x2A" # SET_GAMMA1 (F2h)
    b"\xF3\x06\x43\x70\x72\x36\x37\x6F" # SET_GAMMA1 (F3h)
    b"\xED\x02\x1B\x0B"
    b"\xAE\x01\x77"
    b"\xCD\x01\x63"
    b"\x70\x09\x07\x07\x04\x0E\x0F\x09\x07\x08\x03"
    b"\xE8\x01\x34"
    b"\x62\x0C\x18\x0D\x71\xED\x70\x70\x18\x0F\x71\xEF\x70\x70"
    b"\x63\x0C\x18\x11\x71\xF1\x70\x70\x18\x13\x71\xF3\x70\x70"
    b"\x64\x07\x28\x29\xF1\x01\xF1\x00\x07"
    b"\x66\x0A\x3C\x00\xCD\x67\x45\x45\x10\x00\x00\x00"
    b"\x67\x0A\x00\x3C\x00\x00\x00\x01\x54\x10\x32\x98"
    b"\x74\x07\x10\x85\x80\x00\x00\x4E\x00"
    b"\x98\x02\x3e\x07"
    b"\x35\x00" # Tearing Effect Line ON (35h) [both V-blanking and H-blanking]
    b"\x21\x00" # Display Inversion ON (21h)
    b"\x11\x80\x78" # Sleep Out Mode (11h) and delay(120)
    b"\x29\x80\x14" # Display ON (29h) and delay(20)
    b"\x2A\x04\x00\x00\x00\xEF"  # Column Address Set (2Ah) [Start col = 0, end col = 239]
    b"\x2B\x04\x00\x00\x00\xEF"  # Row Address Set (2Bh) [Start row = 0, end row = 239]
)
# pylint: disable=too-few-public-methods
class GC9A01(BusDisplay):
    """GC9A01 display driver"""

    def __init__(self, bus, **kwargs):
        super().__init__(bus, _INIT_SEQUENCE, **kwargs)
