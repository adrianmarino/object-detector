from lib.input import InputParamsResolver 
from lib.video import VideCaptureFactory
from lib.video import VideWriterFactory

params          = InputParamsResolver().resolve()
video_capture   = VideCaptureFactory().create(params)
video_writer    = VideWriterFactory().create(video_capture, params)