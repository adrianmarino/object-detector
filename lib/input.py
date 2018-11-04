import argparse
import os
import sys

class InputParamsResolver:
    def _not_found_file_error(self, path): print(f'Error: Not found {path} file!')
    def _not_found_input_param(self): print(f'Error: Not found input!')

    def resolve(self):
        parser = argparse.ArgumentParser(
            prog="object-detector",
            description='YOLO Image object detector :)'
        )
        parser.add_argument('--input-image',    help='path of an image file.')
        parser.add_argument('--input-video',    help='path of a video file.')
        parser.add_argument('--input-webcam',   help='get video from webcam.')
        parser.add_argument('--output',         help='path of output file.')

        params = {k: v for k, v in dict(parser.parse_args()._get_kwargs()).items() if v is not None }
        if not params: self._not_found_input_param()

        for name in params:
            if name in ['output', 'input_webcam']: continue
            if not os.path.isfile(params[name]):
                self._not_found_file_error(params[name])
                sys.exit(1)
    
        return params
