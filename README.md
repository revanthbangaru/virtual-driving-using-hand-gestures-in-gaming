# VirtualSteering 🎮

A real-time gesture-based game controller that converts hand gestures into keyboard inputs using computer vision and pose detection.

## Overview

VirtualSteering allows you to control games and applications using hand gestures captured from your webcam. Make hand movements in the air to steer vehicles, trigger actions, and interact with games without needing a physical controller.

## Features

✨ **Real-Time Hand Detection** - Detects and tracks up to 2 hands simultaneously using Google's MediaPipe

🎯 **Intuitive Gesture Recognition**:
- **Forward**: Keep both hands at the same level
- **Turn Left**: Raise your left hand higher
- **Turn Right**: Raise your right hand higher
- **Backward**: Use only one hand
- **Boost**: Raise both thumbs up for speed boost

📊 **Live Visual Feedback** - On-screen display shows detected hands, landmarks, and current actions

⚡ **Low Latency** - Smooth and responsive gesture detection with dead zone filtering

🎮 **Game Compatible** - Works with any game that accepts keyboard input (WASD + Spacebar)

## Requirements

- **Python 3.7+**
- **Windows OS** (uses Windows API for keyboard input)
- **Webcam** (built-in or external)
- **RAM**: Minimum 2GB
- **GPU** (optional, but recommended for better performance)

## Installation

### 1. Clone or Download the Repository
```bash
git clone https://github.com/yourusername/VirtualSteering.git
cd VirtualSteering
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install opencv-python mediapipe
```

## Usage

### Run the Application
```bash
python steering.py
```

### Controls

Once the application starts:

| Gesture | Action | Key |
|---------|--------|-----|
| Both hands level | Move forward | W |
| Left hand higher | Turn left | W + A |
| Right hand higher | Turn right | W + D |
| Single hand | Move backward | S |
| Both thumbs up | Boost | Space |

### Exiting
Press **Q** to quit the application.

## How It Works

### Architecture

```
Webcam Input
    ↓
OpenCV (Video Capture)
    ↓
MediaPipe (Hand Pose Detection)
    ↓
Gesture Recognition Algorithm
    ↓
Key State Management
    ↓
Windows API Input Simulation (keyinput.py)
    ↓
Game/Application Response
```

### Components

#### `steering.py`
- Main application logic
- Hand landmark detection
- Gesture recognition algorithm
- Keyboard state management
- Video display and feedback

**Key Functions:**
- `is_thumbs_up()`: Detects thumbs up gesture
- `set_key()`: Manages key press/release states
- Main loop: Captures frames, processes gestures, applies inputs

#### `keyinput.py`
- Windows API keyboard input simulation
- Uses `ctypes` to access Windows `SendInput()` function
- Supports W, A, S, D, and Spacebar keys
- Handles both key press and key release events

**Key Functions:**
- `press_key(key)`: Simulates key press
- `release_key(key)`: Simulates key release

#### `test_mp.py`
- Debug utility for testing MediaPipe installation

## Project Structure

```
VirtualSteering/
├── steering.py          # Main application
├── keyinput.py          # Windows keyboard input module
├── test_mp.py           # MediaPipe testing utility
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── LICENSE              # Project license
```

## Troubleshooting

### Hand Detection Issues
- **Problem**: Hands not being detected
  - Ensure adequate lighting in the environment
  - Keep hands visible to webcam
  - Try adjusting `min_detection_confidence` in `steering.py` (default: 0.7)

### Keys Not Registering
- **Problem**: Game not responding to inputs
  - Make sure the game window is focused
  - Check that the key codes in `keyinput.py` match your game's key bindings
  - Run as Administrator if having permission issues

### Lag or Latency
- **Problem**: Delayed response to gestures
  - Reduce video resolution in `cv2.VideoCapture(0)`
  - Lower `model_complexity` in MediaPipe configuration
  - Ensure CPU/GPU is not heavily loaded

### Webcam Access Denied
- **Problem**: "Permission denied" error
  - Grant camera permissions in Windows Settings
  - Check antivirus/firewall blocking the application

## Performance Tips

1. **Lighting**: Good lighting improves hand detection accuracy
2. **Distance**: Keep hands 0.5-1.5 meters from the camera
3. **Background**: Plain backgrounds work better than complex backgrounds
4. **GPU**: Enable GPU acceleration in MediaPipe for better performance
5. **Resolution**: Adjust video input resolution based on your system capabilities

## Customization

### Adjusting Dead Zone
Edit the `DEAD_ZONE` variable in `steering.py` to change steering sensitivity:
```python
DEAD_ZONE = 50  # Increase for less sensitive steering
```

### Adding More Gestures
Modify `is_thumbs_up()` function to add custom gesture recognition based on hand landmarks.

### Changing Key Bindings
Edit the `keys` dictionary in `keyinput.py` to map different keys.

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| OS | Windows 7+ | Windows 10+ |
| Python | 3.7 | 3.10+ |
| RAM | 2GB | 4GB+ |
| CPU | 2 cores | 4+ cores |
| GPU | Optional | NVIDIA/AMD with CUDA |

## Limitations

- ⚠️ **Windows Only**: Currently supports only Windows due to Windows API keyboard input
- ⚠️ **Single Gesture Set**: Limited to predefined gestures (extendable)
- ⚠️ **2-Hand Maximum**: Detects maximum 2 hands

## Future Enhancements

- [ ] Multi-platform support (Linux, macOS)
- [ ] Additional gesture recognition (pinch, swipe, etc.)
- [ ] Gesture customization UI
- [ ] Hand tracking confidence visualization
- [ ] Gesture recording and playback
- [ ] Performance optimization for mobile devices

## Dependencies

- **opencv-python**: Real-time video processing
- **mediapipe**: Hand pose detection and landmark tracking

For detailed version information, see `requirements.txt`.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for bugs and feature requests.

## Author

VirtualSteering - Created for gesture-based game control


## Disclaimer

This project is for educational and personal use. Ensure you have the right to use this in your gaming environment and comply with game terms of service.

---


**Ready to control games with your hands? Start with `python steering.py`!** 🚀
