#  object-detector

* Detect objects in images, videos and video streaming from a webcam.
* A [YOLOv3](https://pjreddie.com/darknet/yolo/) predictor writen in python with keras.
* Product of a personal investigation to internalize myself in the matter and strongly based :) on [YOLOv3](https://github.com/xiaochus/YOLOv3) and [keras-yolo3](https://github.com/qqwweee/keras-yolo3).

## Requeriments

* conda
* 7z
* A respectable video card (i.e. GeForce GTX 1060 or higher)

## Setup

**Step 1:** Create project environment.

```bash
conda env create --file environment.yml
```

**Step 2:** Extract network weights.

```bash
7z x  model_data/yolo.h5.7z.001 -o./model_data 
```

## Use

Before all activate object-detector environment:

```bash
source activate object-detector
```

Next you can:

* Detect objects in an image.

```bash
python object-detector.py --input-image input/image.jpg \
    --output output/processed_image.jpg \
    --predict-bounding-boxes
```

* Detect objects on video.

```bash
python object-detector.py --input-video input/video.mp4 \
    --output output/processed_video.mp4 \
    --predict-bounding-boxes \
    --show-preview
```

* Detect objects from webcam video streaming.

```bash
python object-detector.py --input-webcam \
    --output output/processed_video.mp4 \
    --output-fps 10 \
    --predict-bounding-boxes \
    --show-preview
```

* Press **ESC** key to end process. When input is a video this end process before process all video.

* To view all options.

```bash
python object-detector.py --help
```

### Pending issues

* Only use open-cv to process images to increase processing fps.
* Rewrite bounding boxes building and yolo model source code to improve my understanding of the process.

## Fix errors

#### ...window.cpp:698: error: (-2:Unspecified error) The function is not implemented. 

```bash
pip install --upgrade pip
pip install opencv-contrib-python
```