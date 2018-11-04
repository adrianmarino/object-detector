from lib.input import InputParamsResolver 
from lib.video import VideCaptureFactory
from lib.video import VideWriterFactory
import numpy as np
import cv2
from timeit import default_timer as timer

image_height = image_width = 416
preview_width = 800

params          = InputParamsResolver().resolve()
video_capture   = VideCaptureFactory().create(params)
video_writer    = VideWriterFactory().create(video_capture, params)

def resize(frame, width = 100.0):
    r = width / frame.shape[1]
    dim = (width, int(frame.shape[0] * r))

    # perform the actual resizing of the image and show it
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

accum_time = 0
curr_fps = 0
fps = "FPS: ??"
prev_time = timer()
while cv2.waitKey(1) < 0:
    hasFrame, frame = video_capture.read()
    if not hasFrame or 0xFF == ord('q'):
        print("Done processing !!!")
        print("Output file is stored as ", params['output'])
        cv2.destroyAllWindows()
        cv2.waitKey(3000)
        break

    curr_time = timer()
    exec_time = curr_time - prev_time
    prev_time = curr_time
    accum_time = accum_time + exec_time
    curr_fps = curr_fps + 1
    if accum_time > 1:
        accum_time = accum_time - 1
        fps = "FPS: " + str(curr_fps)
        curr_fps = 0

    cv2.putText(frame, text=fps, org=(10, 45), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=1.8, color=(0, 0, 124), thickness=2)

    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('frame', resize(frame, width=preview_width))

    # Write the frame with the detection boxes
    if 'input_image' in params:
        cv2.imwrite(params['output'], frame.astype(np.uint8))
    else:
        video_writer.write(frame.astype(np.uint8))
