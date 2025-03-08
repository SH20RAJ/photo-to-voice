# Photo to Voice

A comprehensive Python application that converts handwritten notes to speech using OCR (Optical Character Recognition) technology, featuring both a web interface and command-line interface with voice command controls.

## Features

### Web Interface (Streamlit)
- 📤 **Upload Interface**: Upload images of handwritten text
- 🔄 **Real-time Processing**: Instant text extraction and display
- 🔊 **Audio Features**: Playback extracted text and download MP3 files
- 👥 **User Experience**: Clean, intuitive interface with clear instructions

### Command-Line Interface
- 📷 **Image Capture**: Take photos of handwritten notes using your webcam
- 🔍 **OCR Processing**: Extract text from images using Tesseract OCR
- 🗣️ **Text-to-Speech**: Read extracted text aloud
- 🎙️ **Voice Control**: Use voice commands to control playback:
  - "pause" - Pause reading
  - "resume" - Continue reading
  - "repeat" - Repeat the current sentence
  - "skip" - Move to the next sentence

## Prerequisites

1. Python 3.x installed ([python.org](https://www.python.org/downloads/))
2. Tesseract OCR installed on your system:
   - macOS: `brew install tesseract`
   - Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`
3. Working webcam (for CLI version)
4. Microphone (for voice commands in CLI version)

## Installation

1. Clone the repository or download the source code

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify Tesseract installation path:
   - macOS: Should be at `/opt/homebrew/bin/tesseract`
   - Windows: Update path in code if different from `C:\Program Files\Tesseract-OCR\tesseract.exe`

## Project Structure

```
├── app.py              # Command-line interface
├── streamlit.py        # Web interface
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
└── audio_output/      # Generated audio files
```

## Usage

### Web Interface
1. Start the Streamlit server:
   ```bash
   streamlit run streamlit.py
   ```
2. Open the provided URL in your web browser
3. Upload an image of handwritten text
4. Click 'Convert to Text and Speech'
5. View extracted text and play/download audio

### Command-Line Interface
1. Run the application:
   ```bash
   python app.py
   ```
2. Choose whether to capture a new image or use an existing one
3. If capturing a new image:
   - Press Space to take the photo
   - Press Esc to cancel
4. The application will extract text and begin reading
5. Use voice commands to control playback

## Best Practices

### Image Quality
- Use well-lit, high-contrast images
- Ensure text is clearly visible
- Avoid blurry or skewed images
- Dark text on light background works best

### Voice Commands
- Speak clearly and at normal volume
- Minimize background noise
- Wait for the command prompt
- Use supported commands only

## Troubleshooting

### Common Issues

1. **Tesseract Not Found**
   - Verify Tesseract installation
   - Check path in code matches installation location
   - Install Tesseract if missing

2. **Poor Text Recognition**
   - Improve image lighting
   - Ensure clear handwriting
   - Try adjusting image preprocessing parameters

3. **Audio Issues**
   - Check speaker/microphone connections
   - Verify PyAudio installation
   - Test system audio settings

4. **Webcam Access**
   - Ensure webcam is connected
   - Check webcam permissions
   - Close other applications using webcam

### Error Messages
- "Audio output directory is not writable": Check folder permissions
- "No text found": Image quality issue or OCR failed
- "Could not access the webcam": Check webcam connection/permissions
- "Error with speech recognition service": Check internet connection

## Dependencies

- `streamlit`: Web interface framework
- `pyttsx3`: Text-to-speech engine
- `pytesseract`: OCR engine wrapper
- `SpeechRecognition`: Voice command processing
- `Pillow`: Image processing
- `opencv-python`: Image capture and preprocessing
- `PyAudio`: Audio processing
- `gTTS`: Google Text-to-Speech for web interface

## License

This project is licensed under the MIT License. See the LICENSE file for details.


Allows real-time voice commands to control playback:(Additional enhancements)
● "Pause" → Stops the audiobook
● "Resume" → Continues reading from where it stopped
● "Repeat" → Reads the last line again
● "Skip" → Moves to the next sentence or paragraph