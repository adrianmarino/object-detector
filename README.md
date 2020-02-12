#  object-detector

* Detect objects in images, videos and video streaming from a webcam.
* A [YOLOv3](https://pjreddie.com/darknet/yolo/) predictor writen in python with keras.
* Product of a personal investigation to internalize myself in the matter.
* **Strongly based** :) on [YOLOv3](https://github.com/xiaochus/YOLOv3) and [keras-yolo3](https://github.com/qqwweee/keras-yolo3).

**Sample Video**

<p align="center">
    <a href="https://www.youtube.com/watch?v=GIXVGANX9WM" rel="noopener noreferrer" target="_blank">
        <img src="https://raw.githubusercontent.com/adrianmarino/object-detector/master/images/video.png" alt="Sample Video" width="800">
    </a>
</p>

**Webcam Screenshot**

<p align="center">
    <img src="https://raw.githubusercontent.com/adrianmarino/object-detector/master/images/webcam.png" alt="Webcam Screenshot" width="817">
</p>

**Sample Image**

<p align="center">
    <img src="https://raw.githubusercontent.com/adrianmarino/object-detector/master/output/processed_image.jpg" alt="Sample Image" width="800">
</p>

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

* **bash**

    ```bash
    echo -e "export PATH=.:\$PATH:$PATH" >> ~/.bashrc
    echo "alias object-detector='source activate object-detector;python object-detector.py'" >> ~/.bashrc
    source ~/.bashrc
    ```

* **zsh**

    ```bash
    echo -e "export PATH=.:\$PATH:$PATH" >> ~/.zshrc
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
    object-detector \s
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

    **Note**: `--input-webcam`: `0` is the integrated laptop webcam video port number, but also you can use another ports for external webcams or external video input devices. Values: From 0 to N.

* Press **ESC** key to end process. When input is a video this end process before process all video.

* To view all options:

    ```bash
    object-detector --help
    
    $ object-detector --help
    usage: object-detector [-h] [--input-image INPUT_IMAGE]
                           [--input-video INPUT_VIDEO] [--output OUTPUT]
                           [--input-webcam INPUT_WEBCAM] [--output-fps OUTPUT_FPS]
                           [--show-preview] [--preview-width PREVIEW_WIDTH]
                           [--predict-bounding-boxes]
    
    YOLO object detector :)
    
    optional arguments:
      -h, --help            show this help message and exit
      --input-image INPUT_IMAGE
                            Path of an image file.
      --input-video INPUT_VIDEO
                            Path of a video file.
      --output OUTPUT       Path of an output file.
      --input-webcam INPUT_WEBCAM
                            Input video device port. Available: 0, 2
                            (/dev/videoX).
      --output-fps OUTPUT_FPS
                            Output video FPS. Ofter use with webcam input videos
      --show-preview        Show preview window.
      --preview-width PREVIEW_WIDTH
                            Preview window width.
      --predict-bounding-boxes
                            Predict & plot bounding boxes
    ```
    
    **Note**:You can see that `--input-webcam` description shows video ports of currently active devices. In this case:
    * `0`: Integrated laptop webcam.
    * `2`: External USB webcam.

## Known issues

* **...window.cpp:698: error: (-2:Unspecified error) The function is not implemented.** 

    ```bash
    pip install --upgrade pip
    pip install opencv-contrib-python
    ```

* **macOS**: Webcam input only works under classic terminal but not in another like iterm.

## Future tasks

* Python notebook to make transfer learning to predict another classes.
* Use Nvidia NVENC encoder/decoder (Process video using GPU cuda cores) to increase video frame rate.
* Rewrite yolo model to improve my understanding of the model.
