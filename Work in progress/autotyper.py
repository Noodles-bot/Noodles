from pynput.keyboard import *
import time

keyboard = Controller()
delay = 1
message = 'test'
resume_key = Key.f8
pause_key = Key.f7
exit_key = Key.esc

pause = True
running = True


def on_press(key):
    global running, pause

    if key == resume_key:
        pause = False
        print("[Resumed]")
    elif key == pause_key:
        pause = True
        print("[Paused]")
    elif key == exit_key:
        running = False
        print("[Exit]")


def display_controls():
    print("// - Settings: ")
    print("\t message = " + message)
    print("\t delay = " + str(delay) + '\n')

    print("// - Controls:")
    print("\t F1 = Resume")
    print("\t F2 = Pause")
    print("\t ESC = Exit")
    print("-----------------------------")
    print('Press F1 to start ...')


def main():
    lis = Listener(on_press=on_press)
    lis.start()

    display_controls()
    while running:
        if not pause:
            keyboard.type(message)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(delay)

    lis.stop()


if __name__ == "__main__":
    main()
