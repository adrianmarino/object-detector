import cv2
from PIL import Image


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
        color=(255, 255, 255),
        thickness=2
    )


def show_frame(frame, fps_calculator, preview_width):
    write_fps(frame, fps_calculator.next())
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('frame', resize(frame, width=preview_width))

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
