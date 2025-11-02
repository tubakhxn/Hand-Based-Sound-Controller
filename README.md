# 🎚️ Hand-Based Sound Controller  
### #Webcam Volume Control (Windows)

Control your **system’s master volume** using **hand gestures** — powered by **MediaPipe**, **OpenCV**, and **PyCaw** (for Windows).

---

## 🚀 Features
- ✌️ Raise **index + middle fingers** to enable volume control.  
- 📈 Move fingers apart to **increase volume**, bring them closer/lower to **decrease volume**.  
- 🎥 Real-time webcam feed with visual indicators:
  - Connection line between fingers  
  - Center circle  
  - Vertical volume bar  

---

## 🖥️ Requirements
- **Windows OS** (for PyCaw system volume control)
- **Python 3.8+**
> 💡 On macOS/Linux: demo visuals will work, but system volume control will not.

---

## ⚙️ Installation (Windows / Local)

1. **Create and activate a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## ▶️ Usage (Local Windows)
```powershell
python main.py
# Or for demo-only (no system volume change):
python main.py --no-audio
```

---

## 🧠 Colab Notes
> ⚠️ Colab cannot access your local audio system (PyCaw).  
> You can still run a **hand tracking demo** visually, but volume changes won’t affect your device.

### 📸 Colab Webcam Snippet
```python
# Install dependencies
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

# ⚠️ Note:
# Continuous real-time OpenCV pipelines may not work stably in Colab.
# Use this snippet only for short gesture demos.
```

---

## 🛠️ Troubleshooting
- 🕶️ **Webcam not detected / black screen:** Try using another camera index (0, 1, …) or ensure no other app is using your webcam.  
- 🧩 **PyCaw import fails:** Make sure `pycaw` and `comtypes` are installed and that you’re on Windows.  

---

## 👤 Author & Credits
**Project by:** [@tubakhxn](https://github.com/tubakhxn)  

💡 Feel free to **fork** this repo, modify, and experiment — but please **don’t just copy and re-upload** it as your own.  
Show support by giving the repo a ⭐ if it helped you!  

---

## 📄 License
MIT License — you’re free to use, modify, and share responsibly with proper credit.
