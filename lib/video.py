import cv2
import numpy as np


class VideoReader:
    def __init__(self, input=0): self.reader = cv2.VideoCapture(input)

    def next(self, flip=False):
        has_frame, frame = self.reader.read()
        return has_frame, cv2.flip(frame.copy(), 1) if flip else frame

    def size(self): return round(self.width()), round(self.height())

    def width(self): return self.reader.get(cv2.CAP_PROP_FRAME_WIDTH)

    def height(self): return self.reader.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def close(self): self.reader.release()


class VideoWriter:
    def __init__(self, path, fps, size):
        self.writer = cv2.VideoWriter(
            path,
            cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
            fps,
            size
        )

    def write(self, frame): self.writer.write(frame.astype(np.uint8))

    def close(self): self.writer.release()
