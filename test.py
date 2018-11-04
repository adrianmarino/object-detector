from lib.input import InputParamsResolver 
from lib.video import VideCaptureFactory
from lib.video import VideWriterFactory
from lib.fps_calculator import FpsCalculator
import numpy as np
import cv2
from timeit import default_timer as timer

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


while cv2.waitKey(1) < 0:
    hasFrame, frame = video_capture.read()
    if not hasFrame or 0xFF == ord('q'):
        print("Done processing !!!")
        print("Output file is stored as ", params['output'])
        cv2.destroyAllWindows()
        cv2.waitKey(3000)
        break

    show_frame(frame, fps_calculator, preview_width)
    
    if 'input_image' in params:
        cv2.imwrite(params['output'], frame.astype(np.uint8))
    else:
        video_writer.write(frame.astype(np.uint8))
