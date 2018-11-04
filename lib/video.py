import cv2

class VideCaptureFactory:
    def create(self, params):
        if 'input_webcam' in params: return cv2.VideoCapture(0)
        if 'input_image' in params: return cv2.VideoCapture(params['input_image'])
        if 'input_video' in params: return cv2.VideoCapture(params['input_video'])

class VideWriterFactory:
    def create(self, cap, params):
        return cv2.VideoWriter(
            params['output'], 
            cv2.VideoWriter_fourcc('M','J','P','G'), 
            30, 
            (
                round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )
        )
