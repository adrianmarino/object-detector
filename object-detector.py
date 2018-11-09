from lib.input_params import InputParamsResolver
from lib.keyboard import Keyboard
from lib.video import VideoReader, VideoWriter
from lib.fps_calculator import FpsCalculator
from lib.object_detector.object_detector_factory import ObjectDetectorFactory
from lib.object_detector.settings import Settings

import lib.draw_utils as draw_utils
import numpy as np
import cv2
import os


def create_video_reader(params):
    if 'input_image' in params:
        return VideoReader(params['input_image'])
    elif 'input_video' in params:
        return VideoReader(params['input_video'])
    elif 'input_webcam' in params:
        return VideoReader()


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


# -----------------------------------------------------------------------------
# Program
# -----------------------------------------------------------------------------
try:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    params = InputParamsResolver().resolve()
    flip = params['input_webcam']
    preview_width = params['preview_width']
    show_preview = params['show_preview']
    predict_bounding_boxes = params['predict_bounding_boxes']

    keyboard = Keyboard()
    fps_calculator = FpsCalculator()

    video_reader = create_video_reader(params)
    video_writer = VideoWriter(
        path=params['output'],
        size=video_reader.size(),
        fps=params['output_fps']
    )
    object_detector = ObjectDetectorFactory.create(Settings())

    while not keyboard.is_key_press(Keyboard.ESC()):
        has_frame, input_frame = video_reader.next(flip=flip)
        if not has_frame:
            break

        output_frame = process_frame(object_detector, input_frame, predict_bounding_boxes)
        show_data(output_frame, show_preview, preview_width)
        write_output(video_writer, output_frame, params)
    print('> Processing finished!')

except Exception as error:
    print(f'> Error when process input!. {error}')

finally:
    cv2.destroyAllWindows()
    object_detector.close()
    video_reader.close()
    video_writer.close()
