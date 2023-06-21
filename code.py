import time
import usb_hid
import board
import digitalio
import adafruit_ssd1306
import busio

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


# Init Display SSD1306 128x64
i2c = busio.I2C(board.GP17, board.GP16)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)
display.show()

# Init Keyboard
kbd = Keyboard(usb_hid.devices)

# Init led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Init Main Button (push button)
mainBtn = digitalio.DigitalInOut(board.GP4)
mainBtn.switch_to_input(pull=digitalio.Pull.DOWN)
mainBtn.pull = digitalio.Pull.DOWN

#Led Status Blink Def
WAITING = 0.3
RUNING = 0.05
ERROR = 3.0
OTHER = 0.02

#Define Device Status for control stages
DEVICE_STATUS = 1

#Global time
#global_time = 0.0
global_timer = 5.0

def AutoWalk():
    kbd.press(Keycode.W)
    while DEVICE_STATUS is 2:
        if mainBtn.value:
            break
        led.value = not led.value
        time.sleep(RUNING)
    kbd.release(Keycode.W)

def 4CodeLockBF():
    tcode = 0000
    while tcode < 10000:
        kbd.write(tcode)
        time.sleep(0.3)
        tcode = tcode + 1

def 3CodeLockBF():
    tcode = 000
    while tcode < 1000:
        kbd.write(tcode)
        time.sleep(0.3)
        tcode = tcode + 1


#Main loop
while True:
    display.fill(0)
    if DEVICE_STATUS is 1:
        led.value = not led.value
        display.fill(0)
        display.text('Waiting', 45, 3, 1)
        display.show()
        time.sleep(WAITING)
        if mainBtn.value:
            DEVICE_STATUS = 2
            timer = 5
            while timer > 0:
                display.fill(0)
                display.text('Waiting', 45, 3, 1)
                text = "Start in " + str(timer) + " seconds"
                display.text(text,10,15,1)
                display.show()
                time.sleep(1)
                timer = timer - 1
    else:
        display.text('Script Runing', 25, 3, 1)
        display.text('AutoWalk Selected', 15, 15, 1)
        display.show()
        AutoWalk()
        DEVICE_STATUS = 1
        display.fill(0)
        display.show()
