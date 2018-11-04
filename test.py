import argparse
import os
import cv2

parser = argparse.ArgumentParser(
    prog="object-detector",
    description='YOLO Image object detector :)'
)
parser.add_argument('--input-image', help='path of an image file.')
parser.add_argument('--input-video', help='path of a video file.')
parser.add_argument('--input-webcam', help='get video from webcam.')
parser.add_argument('--output', help='path of output file.')

args = parser.parse_args()
print('Image: ', args.image)
print('Video: ', args.video)
print('Webcam: ', args.webcam)
print('Output: ', args.webcam)


if (args.image):
    # Open the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.image)
    outputFile = args.image[:-4]+'_yolo_out_py.jpg'
elif (args.video):
    # Open the video file
    if not os.path.isfile(args.video):
        print("Input video file ", args.video, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.video)
    outputFile = args.video[:-4]+'_yolo_out_py.avi'
else:
    # Webcam input
    cap = cv.VideoCapture(0)
 
# Get the video writer initialized to save the output video
if (not args.image):
    vid_writer = cv.VideoWriter(
        outputFile, 
        cv.VideoWriter_fourcc('M','J','P','G'), 
        30, 
        (
            round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        )
    )