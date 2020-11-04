import time
import sys
import threading
#import messageHandler

sys.path.append('../grovepi/Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../grovepi/Software/Python/grove_rgb_lcd')

#GrovePi Modules
import grovepi
import grove_rgb_lcd

#TODO: Declare port numbers
LED = 1
ULTRASONIC = 2
BUTTON = 3

#Initialize grovepi
grovepi.pinMode(LED,"OUTPUT")
grovepi.pinMode(BUTTON,"INPUT")
grove_rgb_lcd.textCommand(0x01) # Clear display

#Initialize threading
lock = threading.Lock() #define I2C lock


if __name__ == '__main__':
    # while True:
    #     with lock:
    #         button = grovepi.digitalRead(BUTTON)
    #     if(button):
    #         start = time.time()
    print(time.time())
    sleep(1)
