#  object-detector

* Detect objects in images, videos and webcam streaming.
* A YOLO v3 predictor.
* Product of a personal research and based on [keras-yolo3](https://github.com/qqwweee/keras-yolo3) , [YOLOv3](https://github.com/xiaochus/YOLOv3) github repos.

## Requeriments

* conda
* 7z

## Setup

**Step 1:** Create project environment.

```bash
conda env create --file environment.yml
```

**Step 2:** Activate project environment.

```bash
source activate object-detector
```

**Step 3:** Extract network weights.

```bash
7z x  model_data/yolo.h5.7z.001 -o./model_data 
```

**Step 4:** Run detector.

```bash
python object-detector.py --input-video input/video3.mp4 --output output/output3.mp4 --predict-bounding-boxes --show-preview
```

**Step 5:** Press ESC key to end process. When input is a video this end process before process all video.

**Step 6:** To show all options.

```bash
python object-detector.py --help
```

## Fix errors

#### ...window.cpp:698: error: (-2:Unspecified error) The function is not implemented. 

```bash
pip install --upgrade pip
pip install opencv-contrib-python
```
