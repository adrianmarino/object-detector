#  object-detector

* Detect objects in images, videos and webcam streaming.
* A YOLO v3 predictor.

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
python object-detector.py --input-video input.mp4 --output output.mp4 --predict-bounding-boxes --preview-width 500
```

**Step 5:** Press ESC to end process. When input is a video this end process before process all video.


## Fix errors

#### ...window.cpp:698: error: (-2:Unspecified error) The function is not implemented. 

```bash
pip install --upgrade pip
pip install opencv-contrib-python
```
