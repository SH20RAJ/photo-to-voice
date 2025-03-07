import streamlit as st
import pyttsx3
import pytesseract
from PIL import Image
import cv2
import numpy as np
import io
import platform
import os

# Set up Tesseract path
if platform.system() == "Darwin":  # macOS
    pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

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
    
    engine = None
    try:
        engine = pyttsx3.init()
        # Configure the engine for better audio quality
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Save to file with proper format
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        # Verify the file was created and is readable
        if not os.path.exists(output_path):
            raise Exception("Failed to generate audio file")
        if not os.access(output_path, os.R_OK):
            raise Exception("Generated audio file is not readable")
        
        return output_path
    
    except Exception as e:
        # Clean up any partially created file
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise Exception(f"Error generating audio: {str(e)}")
    
    finally:
        # Ensure engine resources are properly cleaned up
        if engine:
            try:
                engine.stop()
            except:
                pass

def main():
    st.title("📝 Handwriting to Voice Converter")
    st.write("Upload an image of handwritten text to convert it to speech")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)

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
                        output_file = "output.mp3"
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

    # Add instructions
    with st.expander("How to use"):
        st.write("""
        1. Click 'Browse files' to upload an image of handwritten text
        2. Click 'Convert to Text and Speech' to process the image
        3. View the extracted text and play the audio
        4. Download the audio file if needed
        
        For best results:
        - Ensure good lighting and clear handwriting
        - Use high-contrast images (dark text on light background)
        - Avoid blurry or skewed images
        """)

if __name__ == "__main__":
    main()