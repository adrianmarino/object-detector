from lib.kbhit import KBHit
import cv2


class Keyboard:

    @staticmethod
    def ESC(): return 27

    def __init__(self):
        self.input = KBHit()

    def is_key_press(self, key_code):
        if cv2.waitKey(1) > 0:
            return True

        if self.input.kbhit():
            char = self.input.getch()
            return ord(char) == key_code

        return False
