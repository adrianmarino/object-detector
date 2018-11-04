import argparse
import os
import sys

def not_found_file_error(path): print(f'Error: Not found {path} file!')
def not_found_input_param(): print(f'Error: Not found input!')

def get_input():
    parser = argparse.ArgumentParser(
        prog="object-detector",
        description='YOLO Image object detector :)'
    )
    parser.add_argument('--input-image',    help='path of an image file.')
    parser.add_argument('--input-video',    help='path of a video file.')
    parser.add_argument('--input-webcam',   help='get video from webcam.')
    parser.add_argument('--output',         help='path of output file.')

    params = {k: v for k, v in dict(parser.parse_args()._get_kwargs()).items() if v is not None }
    if not params: not_found_input_param()

    for name in params:
        if not os.path.isfile(params[name]):
                not_found_file_error(params[name])
                sys.exit(1)
 
    return params
