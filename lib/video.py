import cv2


class VideoCaptureFactory:
    @staticmethod
    def create(params):
        if 'input_image' in params: return cv2.VideoCapture(params['input_image'])
        if 'input_video' in params: return cv2.VideoCapture(params['input_video'])
        if 'input_webcam' in params: return cv2.VideoCapture(0)


class VideoWriterFactory:
    @staticmethod
    def create(cap, params):
        return cv2.VideoWriter(
            params['output'],
            cv2.VideoWriter_fourcc('M','J','P','G'),
            params['output_fps'],
            (
                round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )
        )
