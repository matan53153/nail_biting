# 👋 Nail Biting Detector

A macOS menu bar app that uses your camera and AI to detect nail-biting behavior in real-time and alerts you with visual popups.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/platform-macOS-lightgrey.svg" alt="macOS">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
</p>

## 🎯 Features

- **Real-time Detection**: Uses MediaPipe AI to detect when your hands are near your mouth
- **100% Private**: All processing happens locally on your Mac - no data sent anywhere
- **Visual Alerts**: Full-screen red flash alerts when nail-biting is detected
- **Adjustable Sensitivity**: Choose between High, Medium, or Low sensitivity levels
- **Menu Bar Integration**: Lives quietly in your menu bar with simple emoji indicators
  - 👋 = Inactive
  - 👁️ = Monitoring active
- **Easy Toggle**: Enable/disable monitoring with one click
- **Background Operation**: Runs continuously in the background

## 📋 Requirements

- macOS (tested on macOS 14+)
- Python 3.8 or higher
- Built-in or external webcam
- Camera permissions granted

## 🚀 Installation

### Quick Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/nail-biting-detector.git
cd nail-biting-detector
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

3. Activate the virtual environment and run:
```bash
source venv/bin/activate
python nail_biting_detector.py
```

### Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python nail_biting_detector.py
```

## 💡 Usage

### Starting the App

1. Run the app: `python nail_biting_detector.py`
2. Look for the **👋** icon in your menu bar (top-right)
3. Click it and select **"Start Monitoring"**
4. Grant camera permission when prompted
5. The icon changes to **👁️** when monitoring is active

### When Detection Occurs

- A **red semi-transparent flash** will cover your screen for 0.5 seconds
- This interrupts the behavior and makes you aware of it
- 2-second cooldown between alerts to avoid spam

### Adjusting Sensitivity

Click the menu bar icon and select **Sensitivity**:
- **High**: Very sensitive - detects hands from farther away
- **Medium**: Default - balanced detection
- **Low**: Less sensitive - only triggers when very close

### Stopping Monitoring

Click the menu bar icon and select **"Stop Monitoring"**

## 🛠️ How It Works

The app uses:
- **MediaPipe**: Google's hand and face landmark detection
- **OpenCV**: Camera access and image processing
- **rumps**: macOS menu bar app framework
- **PyObjC**: Native macOS alerts

**Detection Logic:**
1. Captures video frames from your camera
2. Detects hand landmarks (21 points per hand)
3. Detects face mesh (468 landmarks)
4. Calculates distance between fingertips and mouth
5. Triggers alert when distance falls below sensitivity threshold

## 📁 Project Structure

```
nail-biting-detector/
├── nail_biting_detector.py  # Main application
├── requirements.txt          # Python dependencies
├── setup.sh                  # Automated setup script
├── run.sh                    # Quick run script
├── README.md                 # This file
├── QUICKSTART.md            # Quick reference guide
└── .gitignore               # Git ignore rules
```

## 🔒 Privacy

This app:
- ✅ Runs 100% offline
- ✅ Does not save any images or videos
- ✅ Does not send any data to the internet
- ✅ Only processes video frames in memory
- ✅ All detection happens locally on your Mac

## 🐛 Troubleshooting

### Camera Not Working

- Check **System Settings → Privacy & Security → Camera**
- Make sure **Terminal** or **Python** has camera access enabled
- Try restarting the app

### Too Many False Alerts

- Lower the sensitivity in the menu
- Ensure good lighting conditions
- Adjust your camera angle

### App Won't Start

- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python3 --version` (need 3.8+)

### Menu Bar Icon Not Appearing

- Check if other menu bar apps are hiding it
- Try rearranging menu bar icons (⌘+drag)
- Restart the app

## 💪 Tips for Best Results

1. **Good Lighting**: Ensure your face is well-lit
2. **Camera Position**: Position camera to see both face and hands
3. **Start with Medium**: Adjust sensitivity based on your experience
4. **Run Continuously**: For best habit-breaking results, run throughout your day

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - feel free to use and modify for personal use.

## 🙏 Credits

Inspired by apps like [HandsOff](https://handsoffapp.com) and [StopNailBiting](https://stopnailbiting.app)

Built with:
- [MediaPipe](https://google.github.io/mediapipe/) by Google
- [rumps](https://github.com/jaredks/rumps) - Python menu bar apps
- [OpenCV](https://opencv.org/) - Computer vision

## ⭐ Show Your Support

If this app helps you break your nail-biting habit, give it a star on GitHub!

---

Made with ❤️ to help people break bad habits
