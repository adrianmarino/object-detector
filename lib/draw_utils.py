import cv2

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
        color=(0, 0, 124), 
        thickness=2
    )

def show_frame(frame, fps_calculator, preview_width):
    write_fps(frame, fps_calculator.next())
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('frame', resize(frame, width=preview_width))
