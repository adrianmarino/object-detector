#  object-detector

* Detect objects in images, videos and video streaming from a webcam.
* A [YOLOv3](https://pjreddie.com/darknet/yolo/) predictor writen in python with keras.
* Product of a personal investigation to internalize myself in the matter.
* **Strongly based** :) on [YOLOv3](https://github.com/xiaochus/YOLOv3) and [keras-yolo3](https://github.com/qqwweee/keras-yolo3).

**Sample Video**
[![Sample Video](https://raw.githubusercontent.com/adrianmarino/object-detector/master/output/sample.png)](http://www.youtube.com/watch?v=GIXVGANX9WM "Sample Video")

### Pending issues

* Python notebook to make transfer learning to predict another classes.
* Only use open-cv to process images to increase fps.
* Rewrite bounding boxes building
* Rewrite yolo model to improve my understanding of process.

## Requeriments

* [anaconda](https://www.anaconda.com/download/#linux)
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

**Step 3:** Before all you need activate object-detector environment every time you use it with this:

```bash
source activate object-detector
```

or forget use it creating a bash/zsh alias:

**bash**:
```bash
echo -e "export PATH=.:\$PATH" >> ~/.bashrc
echo "alias object-detector='source activate object-detector;python object-detector.py'" >> ~/.bashrc
source ~/.bashrc
```

**zsh**:
```bash
echo -e "export PATH=.:\$PATH" >> ~/.zshrc
echo "alias object-detector='source activate object-detector;python object-detector.py'" >> ~/.zshrc
source ~/.zshrc
```

with this you can use object detector as a regular command in the following way:

```bash
object-detector params
```

instead of:

```bash
source activate object-detector
python object-detector.py params
```

## Use

* Detect objects in an image:

```bash
object-detector \
    --input-image input/image.jpg \
    --output output/processed_image.jpg \
    --predict-bounding-boxes
```

* Detect objects on video:

```bash
object-detector \
    --input-video input/video.mp4 \
    --output output/processed_video.mp4 \
    --predict-bounding-boxes \
    --show-preview
```

* Detect objects in a video streaming from webcam:

```bash
object-detector \
    --input-webcam 0 \
    --output output/processed_video.mp4 \
    --output-fps 10 \
    --predict-bounding-boxes \
    --show-preview
```

Note: `--input-webcam 0` is the laptop integrated webcam port but can use another port like: 1, 2, 3...N.

* Press **ESC** key to end process. When input is a video this end process before process all video.

* To view all options:

```bash
object-detector --help
```

## Known issues

#### ...window.cpp:698: error: (-2:Unspecified error) The function is not implemented. 

```bash
pip install --upgrade pip
pip install opencv-contrib-python
```

#### macOS: Webcam input only works under classic terminal but not in another like iterm.
