import pyttsx3
import pytesseract
import speech_recognition as sr
from PIL import Image
import time
import os
import cv2
import sys
import pyaudio  # Required for speech recognition

# Ensure Python 3.x is being used
if sys.version_info[0] < 3:
    print("Error: This script requires Python 3.x")
    sys.exit(1)

# Set the path for Tesseract OCR (Update if necessary)
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

# Initialize text-to-speech engine
speech_engine = pyttsx3.init()
is_paused = False  # Flag to track pause state
current_sentence_index = 0  # Keeps track of the sentence being read

def text_to_speech(text):
    """Reads aloud the given text using text-to-speech."""
    speech_engine.say(text)
    speech_engine.runAndWait()

def listen_for_command():
    """Listens for user commands (pause, resume, repeat, skip)."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Say a command (pause, resume, repeat, skip)...")
        try:
            recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"✅ You said: {command}")
            return command
        except sr.UnknownValueError:
            print("⚠ Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
    return None

def capture_handwritten_note():
    """Captures an image of a handwritten note using a webcam."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return None
    
    print("📸 Press 'Space' to capture the image or 'Esc' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        cv2.imshow("Scan Handwritten Note", frame)
        key = cv2.waitKey(1)

        if key == 32:  # Space key to capture
            image_path = "captured_note.png"
            cv2.imwrite(image_path, frame)
            print(f"✅ Image saved as {image_path}")
            break
        elif key == 27:  # Esc key to exit
            print("❌ Image capture canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return image_path

def preprocess_image(image_path):
    """Enhances image for better OCR accuracy (grayscale + thresholding)."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read {image_path}")
        return None

    # Convert to grayscale and apply thresholding for better readability
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    processed_path = "processed_note.png"
    cv2.imwrite(processed_path, binary)  # Save the processed image
    return processed_path

def extract_text_from_image(image_path):
    """Extracts handwritten text from an image using OCR."""
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return ""
    
    processed_image = preprocess_image(image_path)
    if not processed_image:
        return ""

    # Optimize OCR settings
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(Image.open(processed_image), config=custom_config)
    
    print("📝 Extracted Text:\n", extracted_text)
    return extracted_text.strip()

def read_notes_aloud(image_path):
    """Reads handwritten notes aloud, allowing voice commands for control."""
    global is_paused, current_sentence_index

    text = extract_text_from_image(image_path)
    if not text:
        print("❌ No text found. Exiting...")
        return
    
    sentences = text.split('. ')  # Split text into sentences

    while current_sentence_index < len(sentences):
        if not is_paused:
            text_to_speech(sentences[current_sentence_index])
            print(f"📖 Reading: {sentences[current_sentence_index]}")

        time.sleep(2)  # Give time before listening for a command

        command = listen_for_command()

        if command:
            if "pause" in command:
                print("⏸ Paused.")
                is_paused = True
            elif "resume" in command:
                print("▶ Resuming...")
                is_paused = False
            elif "repeat" in command:
                print("🔄 Repeating last sentence...")
                text_to_speech(sentences[current_sentence_index])
            elif "skip" in command:
                print("⏭ Skipping to next sentence...")
                current_sentence_index += 1
                if current_sentence_index < len(sentences):
                    text_to_speech(sentences[current_sentence_index])

        if not is_paused:
            current_sentence_index += 1  # Move to the next sentence

if __name__ == "__main__":
    print(f"⚙ Using Python version: {sys.version}")

    # Check for missing dependencies
    try:
        import pyttsx3, pytesseract, cv2, speech_recognition, pyaudio
    except ImportError as e:
        print(f"❌ Missing module: {e.name}. Install it using 'pip install {e.name}'")
        sys.exit(1)

    print("\n📷 Do you want to scan a new handwritten note? (yes/no)")
    user_choice = input().strip().lower()
    
    if user_choice == "yes":
        image_path = capture_handwritten_note()
    else:
        # Replace this path with an existing image file on your system
        image_path = r"o.png"

    if image_path:
        read_notes_aloud(image_path)
