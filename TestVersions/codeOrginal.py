import board
import neopixel
import time
import digitalio
import busio
import supervisor


def rgbFill():
    for i in range(1,num_pixels):
        pixels[i] = colors[i % len(colors)]
    pixels.show()


def update(switch):
    if switch:
        pixels[0] = RED
    else:
        pixels[0] = 0
    pixels.show()


def fill(color):
    for i in range(1, num_pixels):
        pixels[i] = color
    pixels.show()


print("Start")
# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
colors = [GREEN, YELLOW, RED, BLUE, WHITE]
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = 0.3
button = digitalio.DigitalInOut(board.GP1)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
lastButton = False
rgbFill()
while True:
    switch = not button.value
    update(switch)
    if switch and not lastButton:
        print("disable")
        time.sleep(.1)
    lastButton = switch
    if supervisor.runtime.serial_bytes_available:
        try:
            value = int(input().strip())
        except:
            continue
        if value == -1:  # Connected to getBattery.py
            rgbFill()
        if value == -2:  # Connected to Robot
            fillBlue()
        if value >= 0 and value < len(colors):
            fill(colors[int(value)])
       
