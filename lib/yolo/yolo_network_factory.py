from lib.yolo.model import yolo_eval, yolo_body, tiny_yolo_body
from lib.yolo.settings import Settings
from lib.yolo.yolo_network import YOLONetwork

from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from keras.utils import multi_gpu_model

import numpy as np
import colorsys
import os


class YOLONetworkFactory:
    @classmethod
    def create(cls, settings=Settings()):
        anchors = cls._get_anchors(settings.anchors_path)
        class_names = cls._get_class(settings.classes_path)
        model = cls._create_model(anchors, class_names, settings)
        colors = cls._get_class_colors(class_names)

        # Generate output tensor targets for filtered bounding boxes.
        input_image_shape = K.placeholder(shape=(2,))

        boxes, scores, classes = yolo_eval(
            model.output,
            anchors,
            len(class_names),
            input_image_shape,
            score_threshold=settings.score,
            iou_threshold=settings.iou
        )

        return YOLONetwork(
            class_names,
            anchors,
            boxes,
            scores,
            classes,
            input_image_shape,
            model,
            colors,
            settings.model_image_size
        )

    @staticmethod
    def _create_model(anchors, class_names, settings):
        model_path = os.path.expanduser(settings.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'
        # Load model, or construct model and load weights.
        num_anchors = len(anchors)
        num_classes = len(class_names)
        is_tiny_version = num_anchors == 6  # default setting
        try:
            model = load_model(
                model_path,
                compile=False
            )
        except:
            model = tiny_yolo_body(Input(shape=(None, None, 3)), num_anchors // 2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None, None, 3)), num_anchors // 3, num_classes)

            model.load_weights(model_path)  # make sure model, anchors and classes match
        else:
            assert model.layers[-1].output_shape[-1] == \
                   num_anchors / len(model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        if settings.gpu_num >= 2:
            model = multi_gpu_model(model, gpus=settings.gpu_num)

        return model

    @staticmethod
    def _get_class_colors(class_names):
        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(class_names), 1., 1.)
                      for x in range(len(class_names))]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        return colors

    @staticmethod
    def _get_class(classes_path):
        classes_path = os.path.expanduser(classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    @staticmethod
    def _get_anchors(path):
        path = os.path.expanduser(path)
        with open(path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)
