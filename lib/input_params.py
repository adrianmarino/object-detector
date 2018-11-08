import argparse
import sys
import os


class InputParamsResolver:

    @staticmethod
    def _not_found_file_error(path): print(f'Error: Not found {path} file!')

    @staticmethod
    def _not_found_input_param(): print(f'Error: Not found input!')

    @staticmethod
    def _not_found_output_param(): print(f'Error: Not found output!')

    @staticmethod
    def resolve():
        parser = argparse.ArgumentParser(
            prog="object-detector",
            description='YOLO Image object detector :)'
        )
        parser.add_argument(
            '--input-image',
            help='path of an image file.'
        )
        parser.add_argument(
            '--input-video',
            help='path of a video file.'
        )
        parser.add_argument(
            '--input-webcam',
            help='get video streming from webcam.',
            action='store_true',
            default=False
        )
        parser.add_argument(
            '--output',
            help='path of an output file.'
        )
        parser.add_argument(
            '--output-fps',
            help='fps of output video. Ofter use with webcam input videos',
            type=int,
            default=30
        )
        parser.add_argument(
            '--show-preview',
            help='show a preview on a system window.',
            action='store_true',
            default=False
        )
        parser.add_argument(
            '--preview-width',
            help='preview window width.',
            type=int,
            default=1200
        )
        parser.add_argument(
            '--predict-bounding-boxes',
            help='predict & plot bounding boxes',
            action='store_true',
            default=False
        )

        params = {k: v for k, v in dict(parser.parse_args()._get_kwargs()).items() if v is not None }

        if not params:
            InputParamsResolver._not_found_input_param()
        if 'output' in params:
            InputParamsResolver._not_found_output_param()

        exclude_params = [
            'output', 'predict_bounding_boxes', 'preview_width', 'input_webcam', 'show_preview', 'output_fps'
        ]
        for name in params:
            if name in exclude_params:
                continue
            if not os.path.isfile(params[name]):
                InputParamsResolver._not_found_file_error(params[name])
                sys.exit(1)

        return params