import streamlit as st
from gtts import gTTS
import pytesseract
from PIL import Image
import cv2
import numpy as np
import io
import platform
import os
import time

# Set up Tesseract path
if platform.system() == "Darwin":  # macOS
    pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"
else:  # Linux (Streamlit Cloud) or Windows
    pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def preprocess_image(image):
    # Convert to OpenCV format
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    return binary

def extract_text(image):
    # Preprocess the image
    processed_image = preprocess_image(image)
    
    # Extract text using Tesseract
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    
    return text.strip()

# Add this after imports
OUTPUT_DIR = "audio_output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def text_to_speech(text, output_file="output.mp3"):
    output_path = os.path.join(OUTPUT_DIR, output_file)
    
    # Ensure output directory exists and is writable
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    elif not os.access(OUTPUT_DIR, os.W_OK):
        raise Exception("Audio output directory is not writable")
    
    try:
        # Create gTTS object and save to file
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        
        # Verify the file was created and is readable
        if not os.path.exists(output_path):
            raise Exception("Failed to generate audio file")
        if not os.access(output_path, os.R_OK):
            raise Exception("Generated audio file is not readable")
        
        # Verify file size is greater than 0
        if os.path.getsize(output_path) == 0:
            raise Exception("Generated audio file is empty")
            
        return output_path
    
    except Exception as e:
        # Clean up any partially created file
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise Exception(f"Error generating audio: {str(e)}")

def main():
    st.title("📝 Handwriting to Voice Converter")
    st.write("Upload an image of handwritten text or capture using camera to convert it to speech")

    # Input method selection
    input_method = st.radio("Choose input method", ["Upload Image", "Use Camera"])

    if input_method == "Upload Image":
        # File uploader
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            process_image(image)
    else:
        # Camera input
        camera_image = st.camera_input("Take a picture")
        if camera_image is not None:
            image = Image.open(camera_image)
            process_image(image)

    # Add instructions
    with st.expander("How to use"):
        st.write("""
        1. Choose between uploading an image or using camera
        2. If uploading: Click 'Browse files' to upload an image of handwritten text
           If using camera: Click 'Take a picture' to capture the text
        3. Click 'Convert to Text and Speech' to process the image
        4. View the extracted text and play the audio
        5. Download the audio file if needed
        
        For best results:
        - Ensure good lighting and clear handwriting
        - Use high-contrast images (dark text on light background)
        - Avoid blurry or skewed images
        - Keep the camera steady when capturing
        """)

def process_image(image):
    st.image(image, caption='Input Image', use_container_width=True)

    # Add a button to process the image
    if st.button('Convert to Text and Speech'):
        with st.spinner('Processing image...'):
            # Extract text
            text = extract_text(image)
            
            if text:
                st.subheader("Extracted Text:")
                st.write(text)
                
                try:
                    # Convert to speech
                    output_file = f"output_{int(time.time())}.mp3"
                    output_path = text_to_speech(text, output_file)
                    
                    # Create audio player
                    if os.path.exists(output_path):
                        # Read the audio file once and store in memory
                        with open(output_path, "rb") as audio_file:
                            audio_bytes = audio_file.read()
                        
                        # Display audio player
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        # Add download button using the same audio bytes
                        st.download_button(
                            label="Download Audio",
                            data=audio_bytes,
                            file_name="handwriting_audio.mp3",
                            mime="audio/mp3"
                        )
                except Exception as e:
                    st.error(f"Error generating audio: {str(e)}")
            else:
                st.error("No text could be extracted from the image. Please try with a clearer image.")

if __name__ == "__main__":
    main()