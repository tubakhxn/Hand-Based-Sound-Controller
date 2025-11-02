# Webcam Volume Control (Windows)

This project uses a webcam, MediaPipe hand tracking, and PyCaw (Windows) to control the system master volume using a two-finger gesture.

Features
- Raise index + middle fingers (both up) to enable volume control.
- Move the two fingers apart to increase volume; bring them closer/lower them to decrease volume.
- Live webcam feed with indicators: connection line, center circle and a vertical volume bar.

Requirements
- Windows (for system volume control via PyCaw). On other OSes the demo visuals work but system control will not.
- Python 3.8+

Installation (Windows / local)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Usage (local Windows)
```powershell
python main.py
# Or for demo-only (no system volume change):
python main.py --no-audio
```

Colab notes
- Colab does not have access to your local system audio and cannot run PyCaw. You can still run a demo of hand tracking inside Colab by using a small JS widget to capture webcam frames, but the script cannot change your computer's master volume from Colab.
- If you want a Colab demo, use the provided `colab-snippet` in this README to capture webcam frames and preview detections; set `--no-audio` for demo mode.

Colab webcam snippet (paste into a notebook cell):

```python
# pip install mediapipe opencv-python
!pip install mediapipe opencv-python

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import cv2, numpy as np

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript("""
  async function takePhoto(quality) {
    const div = document.createElement('div');
    const video = document.createElement('video');
    const stream = await navigator.mediaDevices.getUserMedia({video: true});
    document.body.appendChild(div);
    div.appendChild(video);
    video.srcObject = stream;
    await video.play();
    // Resize
    var canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL('image/jpeg', quality);
    stream.getTracks().forEach(track => track.stop());
    return dataUrl;
  }
  takePhoto(%f).then(dataUrl => {console.log(dataUrl);})();
  """ % quality)
  display(js)

# Note: running a continuous OpenCV real-time pipeline in Colab is flaky. Use this only for short demos.
```

Troubleshooting
- If the webcam is black / not detected: try other camera indices (0, 1, ...), ensure no other app is using the camera.
- If PyCaw import fails: ensure you installed `pycaw` and `comtypes` and running on Windows.

License
MIT
