from lib.input import InputParamsResolver 
from lib.video import VideoCaptureFactory
from lib.video import VideoWriterFactory
from lib.fps_calculator import FpsCalculator
from lib.object_detector.object_detector_factory import ObjectDetectorFactory
from lib.object_detector.settings import Settings

import lib.draw_utils as draw_utils
import numpy as np
import cv2
import sys

params = InputParamsResolver.resolve()

video_capture = VideoCaptureFactory.create(params)
video_writer = VideoWriterFactory.create(video_capture, params)
fps_calculator = FpsCalculator()

settings = Settings()
object_detector = ObjectDetectorFactory.create(settings)


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


def process_frame(frame):
    return object_detector.predict_bounding_boxes(frame) if params['predict_bounding_boxes'] else frame


while cv2.waitKey(1) < 0:
    hasFrame, input_frame = next_frame(video_capture, params)
    output_frame = process_frame(input_frame)
    draw_utils.show_frame(output_frame, fps_calculator, params['preview_width'])
    write_output(output_frame, params)
