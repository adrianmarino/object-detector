import argparse
import os

from lib.video import available_video_ports


def intersection(lst1, lst2): return list(set(lst1) & set(lst2))


class NotFountFileError(Exception):
    def __init__(self, name, path): super(NotFountFileError, self).__init__(f'Error: Not found {path} {name} file!')


class InputParamsResolver:

    def __init__(self):
        parser = argparse.ArgumentParser(prog="object-detector", description='YOLO object detector :)')
        parser.add_argument('--input-image', help='Path of an image file.')
        parser.add_argument('--input-video', help='Path of a video file.')
        parser.add_argument('--output', help='Path of an output file.')
        parser.add_argument(
            '--input-webcam',
            help=f"Input video device port. Available: {', '.join(available_video_ports())} (/dev/videoX).",
            type=int,
            default=0
        )
        parser.add_argument(
            '--output-fps',
            help='Output video FPS. Often used with webcam input videos',
            type=int,
            default=30
        )
        parser.add_argument(
            '--show-preview',
            help='Show preview window.',
            action='store_true',
            default=False
        )
        parser.add_argument(
            '--preview-width',
            help='Preview window width.',
            type=int,
            default=1500
        )
        parser.add_argument(
            '--predict-bounding-boxes',
            help='Predict & plot bounding boxes',
            action='store_true',
            default=False
        )
        self.parser = parser

    @property
    def params(self):
        return {k: v for k, v in dict(self.parser.parse_args()._get_kwargs()).items() if v is not None}

    @property
    def path_params(self):
        return {name: value for name, value in self.params.items() if name in ['input_image', 'input_video']}

    def resolve(self):
        for name, path in self.path_params.items():
            if not os.path.isfile(path):
                raise NotFountFileError(name, path)
        return self.params
