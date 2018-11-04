#  object-detector

Detect objects under images, videos and from webcam streaming video.

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
python test.py --input-video input/videos/videoplayback.mp4 --output output/videos/output.mp4
```