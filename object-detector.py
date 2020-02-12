import os

import cv2
import numpy as np

import lib.draw_utils as draw_utils
from lib.fps_calculator import FpsCalculator
from lib.input_params import InputParamsResolver
from lib.keyboard import Keyboard
from lib.object_detector.object_detector_factory import ObjectDetectorFactory
from lib.object_detector.settings import Settings
from lib.video import VideoReader, VideoWriter


def create_reader(params):
    if 'input_image' in params:
        return VideoReader(params['input_image'])
    elif 'input_video' in params:
        return VideoReader(params['input_video'])
    elif 'input_webcam' in params:
        return VideoReader(params['input_webcam'])


def create_input_output():
    reader = create_reader(params)
    return reader, VideoWriter(params['output'], params['output_fps'], reader.size())


def write_output(video_writer, frame, params):
    if 'input_image' in params:
        cv2.imwrite(params['output'], frame.astype(np.uint8))
    else:
        video_writer.write(frame.astype(np.uint8))


def process_frame(object_detector, frame, predict_bounding_boxes):
    return object_detector.predict_bounding_boxes(frame) if predict_bounding_boxes else frame


def show_data(frame, show_preview, preview_width):
    if show_preview:
        draw_utils.show_frame(frame, fps_calculator, preview_width)
    else:
        print("> Processing at", fps_calculator.next())


def hide_tensorflow_logs(): os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def get_to_processing_params():
    return params['input_webcam'], params['preview_width'], params['show_preview'], params['predict_bounding_boxes']


if __name__ == '__main__':
    hide_tensorflow_logs()
    params = InputParamsResolver().resolve()
    keyboard = Keyboard()
    fps_calculator = FpsCalculator()
    reader, writer = create_input_output()
    object_detector = ObjectDetectorFactory.create(Settings())

    flip, preview_width, show_preview, predict_bounding_boxes = get_to_processing_params()

    while not keyboard.is_key_press(Keyboard.ESC()):
        has_frame, input_frame = reader.next(flip=flip)
        if not has_frame:
            break

        output_frame = process_frame(object_detector, input_frame, predict_bounding_boxes)
        show_data(output_frame, show_preview, preview_width)
        write_output(writer, output_frame, params)

    print('> Processing finished!')
    cv2.destroyAllWindows()
    object_detector.close()
    reader.close()
    writer.close()
