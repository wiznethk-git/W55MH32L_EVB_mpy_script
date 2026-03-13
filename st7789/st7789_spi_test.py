import machine
import st7789py as st7789
import vga2_8x8

spi = machine.SPI(1, baudrate=30_000_000, polarity=0, phase=0)
display = st7789.ST7789(spi, 240, 240,
                        reset=machine.Pin("PD6", machine.Pin.OUT),
                        dc=machine.Pin("PD5", machine.Pin.OUT),
                        cs=machine.Pin("PA4", machine.Pin.OUT),   # set to None if your board has no CS pin
#                         backlight=machine.Pin(15, machine.Pin.OUT),
                        rotation=0)   # 0,1,2,3

display.fill(st7789.BLACK)
display.text(vga2_8x8, "Hello W55MH32", 10, 10, st7789.WHITE)
