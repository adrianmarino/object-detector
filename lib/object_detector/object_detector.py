# -*- coding: utf-8 -*-
import numpy as np
from keras import backend as K
from PIL import Image
from lib.draw_utils import get_boxed_image, draw_bounding_box, load_font


class ObjectDetector(object):
    def __init__(
            self,
            class_names,
            anchors,
            boxes,
            scores,
            classes,
            input_image_shape,
            model,
            colors,
            model_image_size,
            font_path
    ):
        self.class_names = class_names
        self.anchors = anchors
        self.boxes = boxes
        self.scores = scores
        self.classes = classes
        self.input_image_shape = input_image_shape
        self.model = model
        self.colors = colors
        self.model_image_size = model_image_size
        self.sess = K.get_session()
        self.font_path = font_path

    def predict_bounding_boxes(self, image):
        image = Image.fromarray(image)
        out_boxes, out_classes, out_scores = self._predict(image)
        self.draw_bounding_boxes(image, out_boxes, out_classes, out_scores)
        return np.asarray(image)

    def draw_bounding_boxes(self, image, out_boxes, out_classes, out_scores):
        font = load_font(image, self.font_path)
        thickness = (image.size[0] + image.size[1]) // 800
        for index, clazz in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[clazz]
            box = out_boxes[index]
            score = out_scores[index]
            color = self.colors[clazz]
            draw_bounding_box(box, color, font, image, predicted_class, score, thickness)

    def _predict(self, image):
        boxed_image = get_boxed_image(image, self.model_image_size)

        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        return out_boxes, out_classes, out_scores

    def close(self): self.sess.close()
