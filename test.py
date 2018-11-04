from lib.input import InputParamsResolver 
from lib.video import VideCaptureFactory
from lib.video import VideWriterFactory
from lib.fps_calculator import FpsCalculator
import numpy as np
import cv2
import sys

image_height = image_width = 416
preview_width = 800

params          = InputParamsResolver().resolve()
video_capture   = VideCaptureFactory().create(params)
video_writer    = VideWriterFactory().create(video_capture, params)
fps_calculator  = FpsCalculator()

def resize(frame, width = 100.0):
    r = width / frame.shape[1]
    dim = (width, int(frame.shape[0] * r))

    # perform the actual resizing of the image and show it
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

def write_fps(frame, value):
    cv2.putText(
        frame, 
        text=value, 
        org=(10, 45), 
        fontFace=cv2.FONT_HERSHEY_DUPLEX,
        fontScale=1.8, 
        color=(0, 0, 124), 
        thickness=2
    )

def show_frame(frame, fps_calculator, preview_width):
    write_fps(frame, fps_calculator.next())
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('frame', resize(frame, width=preview_width))

def write_output(frame, params):
    if 'input_image' in params:
        cv2.imwrite(params['output'], frame.astype(np.uint8))
    else:
        video_writer.write(frame.astype(np.uint8))

def stop_processing(params):
    print("Done processing !!!")
    print("Output file is stored as ", params['output'])
    cv2.destroyAllWindows()
    cv2.waitKey(3000)
    sys.exit(1)

def next_frame(video_capture, params):
    hasFrame, frame = video_capture.read() 
    if not hasFrame: stop_processing(params)
    return hasFrame, frame 

while cv2.waitKey(1) < 0:
    hasFrame, frame = next_frame(video_capture, params)
    show_frame(frame, fps_calculator, preview_width)
    write_output(frame, params)
