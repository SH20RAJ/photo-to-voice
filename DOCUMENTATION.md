# Handwriting to Voice Converter Documentation

## Project Overview
This project provides a handwriting-to-voice converter application with two interfaces:
1. A web interface built with Streamlit
2. A command-line interface with voice command controls

The application uses OCR (Optical Character Recognition) to extract text from handwritten notes and converts it to speech.

## Features

### Web Interface (Streamlit)
- Upload images of handwritten text
- Real-time text extraction and display
- Audio playback of extracted text
- Download audio files in MP3 format
- User-friendly interface with clear instructions

### Command-Line Interface
- Webcam capture of handwritten notes
- Voice command controls:
  - Pause/Resume playback
  - Repeat current sentence
  - Skip to next sentence
- Real-time text extraction and speech output

## Setup Instructions

### Prerequisites
1. Python 3.x installed
2. Tesseract OCR installed on your system:
   - macOS: `brew install tesseract`
   - Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`
3. Working webcam (for CLI version)
4. Microphone (for voice commands in CLI version)

### Installation Steps

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

4. Verify Tesseract installation:
   - macOS: Should be at `/opt/homebrew/bin/tesseract`
   - Windows: Update path in code if different from `C:\Program Files\Tesseract-OCR\tesseract.exe`

## Running the Application

### Web Interface (Streamlit)
1. Start the Streamlit server:
   ```bash
   streamlit run streamlit.py
   ```
2. Open the provided URL in your web browser
3. Upload an image of handwritten text
4. Click 'Convert to Text and Speech'
5. View extracted text and play/download audio

### Command-Line Interface
1. Run the CLI version:
   ```bash
   python app.py
   ```
2. Choose to capture new image or use existing one
3. If capturing new image:
   - Press Space to capture
   - Press Esc to cancel
4. Use voice commands to control playback

## Project Structure

```
├── app.py              # Command-line interface
├── streamlit.py        # Web interface
├── requirements.txt    # Project dependencies
├── README.md          # Project overview
└── audio_output/      # Generated audio files
```

## Dependencies

- `pyttsx3`: Text-to-speech engine
- `pytesseract`: OCR engine wrapper
- `SpeechRecognition`: Voice command processing
- `Pillow`: Image processing
- `opencv-python`: Image capture and preprocessing
- `PyAudio`: Audio processing
- `streamlit`: Web interface framework
- `gTTS`: Google Text-to-Speech for web interface

## Best Practices

### Image Quality
- Use well-lit, high-contrast images
- Ensure text is clearly visible
- Avoid blurry or skewed images
- Dark text on light background works best

### Voice Commands (CLI)
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

## Performance Optimization

1. **Image Processing**
   - Resize large images before processing
   - Use appropriate thresholding values
   - Consider image format (PNG/JPEG)

2. **Memory Usage**
   - Clean up temporary files
   - Process one image at a time
   - Close resources after use

3. **Response Time**
   - Use appropriate OCR settings
   - Optimize image preprocessing
   - Consider hardware capabilities

## Support

For issues and questions:
1. Check troubleshooting section
2. Verify dependencies and versions
3. Review error messages
4. Check system requirements

## License

This project is licensed under the MIT License. See the LICENSE file for details.