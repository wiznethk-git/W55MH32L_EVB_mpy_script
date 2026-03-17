import machine, time
import st7789py as st7789
import vga2_16x32

# Setup SPI
spi = machine.SPI(1, baudrate=30_000_000, polarity=0, phase=0)

# Initialize display
display = st7789.ST7789(
    spi, 240, 240,
    reset=machine.Pin("PD6", machine.Pin.OUT),
    dc=machine.Pin("PD5", machine.Pin.OUT),
    cs=machine.Pin("PA4", machine.Pin.OUT),
    rotation=0
)

# Big smiley
def smile_face(x, y, color):
    display.fill_rect(30+x, 30+y, 50, 50, color)
    display.fill_rect(40+x, 45+y, 5, 5, st7789.BLACK)
    display.fill_rect(65+x, 45+y, 5, 5, st7789.BLACK)
    display.fill_rect(45+x, 65+y, 20, 5, st7789.BLACK)

# Clear screen and show text
display.fill(st7789.BLACK)
display.text(vga2_16x32, "Hello!", 10, 10, st7789.WHITE)
time.sleep(1)
display.text(vga2_16x32, "SPI DEMO", 10, 40, st7789.WHITE)
time.sleep(2)

# show smile face
smile_face(0, 80, st7789.YELLOW)
smile_face(60, 80, st7789.BLUE)
smile_face(120, 80, st7789.GREEN)

