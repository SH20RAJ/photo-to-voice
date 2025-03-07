# Photo to Voice

A Python application that converts handwritten notes to speech using OCR (Optical Character Recognition) technology and adds voice command controls for interacting with the text.

## Features

- 📷 **Image Capture**: Take photos of handwritten notes using your webcam
- 🔍 **OCR Processing**: Extract text from images using Tesseract OCR
- 🗣️ **Text-to-Speech**: Read extracted text aloud
- 🎙️ **Voice Control**: Use voice commands to control playback:
  - "pause" - Pause reading
  - "resume" - Continue reading
  - "repeat" - Repeat the current sentence
  - "skip" - Move to the next sentence

## Requirements

- Python 3.x
- Tesseract OCR installed on your system
- Webcam (for capturing new images)
- Microphone (for voice commands)

## Dependencies

```
pyttsx3
pytesseract
speech_recognition
Pillow (PIL)
opencv-python (cv2)
pyaudio
```

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/downloads/)
2. Install Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`
3. Clone this repository
4. Install required Python packages:
   ```
   pip install pyttsx3 pytesseract SpeechRecognition pillow opencv-python pyaudio
   ```
5. Update the Tesseract path in `app.py` if necessary:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```
2. Choose whether to capture a new image or use an existing one
3. If capturing a new image, press Space to take the photo
4. The application will extract text from the image and begin reading it
5. Use voice commands to control the playback

## How It Works

1. The application uses OpenCV to capture images from your webcam
2. Images are preprocessed to improve OCR accuracy (grayscale + thresholding)
3. Tesseract OCR extracts text from the processed images
4. The pyttsx3 library converts the extracted text to speech
5. Speech Recognition allows you to control the application with voice commands

## Troubleshooting

- **Webcam access issues**: Ensure your webcam is properly connected and not in use by another application
- **OCR accuracy problems**: Try adjusting the lighting when capturing images, or modify the preprocessing parameters
- **Voice command recognition issues**: Speak clearly, reduce background noise, or adjust microphone settings
- **Import errors**: Ensure all required packages are installed using pip

## License

[MIT License](LICENSE)