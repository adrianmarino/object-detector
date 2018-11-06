from lib.input import InputParamsResolver 
from lib.video import VideCaptureFactory
from lib.video import VideWriterFactory
from lib.fps_calculator import FpsCalculator
from lib.yolo.yolo_network_factory import YOLONetworkFactory
from lib.yolo.settings import Settings

import lib.draw_utils as draw_utils
import numpy as np
import cv2
import sys

preview_width = 2400
params = InputParamsResolver.resolve()
video_capture = VideCaptureFactory().create(params)
video_writer = VideWriterFactory().create(video_capture, params)
fps_calculator = FpsCalculator()
settings = Settings()
network = YOLONetworkFactory.create(settings)


def write_output(frame, params):
    if 'input_image' in params:
        cv2.imwrite(params['output'], frame.astype(np.uint8))
    else:
        video_writer.write(frame.astype(np.uint8))


def stop_processing(params):
    print("End processing!")
    print("Output file is stored as ", params['output'])
    cv2.destroyAllWindows()
    cv2.waitKey(3000)
    sys.exit(1)


def next_frame(video_capture, params):
    hasFrame, frame = video_capture.read() 
    if not hasFrame:
        stop_processing(params)
    return hasFrame, frame 


while cv2.waitKey(1) < 0:
    hasFrame, input_frame = next_frame(video_capture, params)
    output_frame = network.predict(input_frame)
    draw_utils.show_frame(output_frame, fps_calculator, preview_width)
    write_output(output_frame, params)
