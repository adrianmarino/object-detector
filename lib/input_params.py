import argparse
import os


def intersection(lst1, lst2): return list(set(lst1) & set(lst2))


class NotFountFileError(Exception):
    def __init__(self, name, path): super(NotFountFileError, self).__init__(f'Error: Not found {path} {name} file!')


class InputParamsResolver:

    def __init__(self):
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
        self.parser = parser

    @property
    def params(self):
        return {k: v for k, v in dict(self.parser.parse_args()._get_kwargs()).items() if v is not None }

    @property
    def path_params(self):
        return {name: value for name, value in self.params.items() if name in ['input_image', 'input_video']}

    def resolve(self):
        for name, path in self.path_params.items():
            if not os.path.isfile(path):
                raise NotFountFileError(name, path)
        return self.params


