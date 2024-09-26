"""
Reset SPI bus.
"""

def spi_init():
    
    from machine import Pin, SPI
    
    spi: SPI = SPI(1,baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=None, mosi=None, miso=None)
    spi.deinit()
    print('SPI reset done.')

spi_init()
