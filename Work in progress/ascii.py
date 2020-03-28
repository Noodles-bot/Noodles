from pynput.keyboard import *
import time
keyboard = Controller()
n = ',beg'
i = input("Start sequence [Y/N]:")
if i.lower() == 'y':
    while True:
        time.sleep(2.65)
        keyboard.type(str(n))
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(2.65)
        keyboard.type(',search')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

else:
    print('Program stopped')
