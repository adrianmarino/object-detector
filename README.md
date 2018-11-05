#  object-detector

Detect objects in images, videos and webcam streaming videos.

## Requeriments

* conda

## Setup

**Step 1:** Create project environment.

```bash
conda env create --file environment.yml
```

**Step 2:** Activate project environment.

```bash
source activate object-detector
```

**Step 3:** Run detector.

```bash
python object-detector.py --input-video input/videos/videoplayback.mp4 --output output/videos/video.mp4
```
