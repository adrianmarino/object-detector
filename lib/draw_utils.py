import cv2
import numpy as np
from PIL import ImageDraw, Image


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
        fontScale=1.2,
        color=(255, 255, 255),
        thickness=2
    )


def show_frame(frame, fps_calculator, preview_width):
    frame_copy = frame.copy()
    write_fps(frame_copy, fps_calculator.next())
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('frame', resize(frame_copy, width=preview_width))


def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128, 128, 128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image


def draw_bounding_box(box, color, font, image, predicted_class_name, score, thickness):
    label = '{} {:.0f}%'.format(predicted_class_name, score * 100)
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
            outline=color,
            width=1
        )
    draw.rectangle(
        [
            tuple(text_origin),
            tuple(text_origin + label_size)
        ],
        fill=color,
        width=1
    )
    draw.text(text_origin, label.capitalize(), fill=(0, 0, 0), font=font)
    del draw


def get_boxed_image(image, image_size):
    if image_size != (None, None):
        assert image_size[0] % 32 == 0, 'Multiples of 32 required'
        assert image_size[1] % 32 == 0, 'Multiples of 32 required'
        boxed_image = letterbox_image(
            image,
            tuple(reversed(image_size))
        )
    else:
        new_image_size = (
            image.width - (image.width % 32),
            image.height - (image.height % 32)
        )
        boxed_image = letterbox_image(image, new_image_size)
    return boxed_image
