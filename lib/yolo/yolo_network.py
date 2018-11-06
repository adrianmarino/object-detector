# -*- coding: utf-8 -*-
import numpy as np
from keras import backend as K

from PIL import ImageFont, ImageDraw, Image

from lib.draw_utils import letterbox_image

class YOLONetwork(object):
    def __init__(
            self,
            class_names,
            anchors,
            boxes,
            scores,
            classes,
            input_image_shape,
            yolo_model,
            colors,
            model_image_size
    ):
        self.class_names = class_names
        self.anchors = anchors
        self.boxes = boxes
        self.scores = scores
        self.classes = classes
        self.input_image_shape = input_image_shape
        self.yolo_model = yolo_model
        self.colors = colors
        self.model_image_size = model_image_size
        self.sess = K.get_session()

    def predict(self, frame):
        image = Image.fromarray(frame)

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (
                image.width - (image.width % 32),
                image.height - (image.height % 32)
            )
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })

        font = ImageFont.truetype(
            font='model_data/font/FiraMono-Medium.otf',
            size=np.floor(2e-2 * image.size[1] + 0.5).astype('int32')
        )
        thickness = (image.size[0] + image.size[1]) // 800

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.0f}%'.format(predicted_class, score * 100)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top])

            # My kingdom for a good redistributable image drawing library.
            for i in range(thickness):
                draw.rectangle(
                    [
                        left + i,
                        top + i,
                        right - i,
                        bottom - i
                    ],
                    outline=self.colors[c],
                    width=1
                )

            draw.rectangle(
                [
                    tuple(text_origin),
                    tuple(text_origin + label_size)
                ],
                fill=self.colors[c],
                width=1
            )
            draw.text(text_origin, label.capitalize(), fill=(0, 0, 0), font=font)
            del draw

        return np.asarray(image)

    def close(self):
        self.sess.close()
