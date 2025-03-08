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
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import threading
import queue

# Set page configuration and custom theme
st.set_page_config(
    page_title="AI Text Vision",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(120deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        padding: 0.8rem !important;
        border: none !important;
        border-radius: 10px !important;
        background: linear-gradient(120deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(79,172,254,0.3) !important;
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #4facfe !important;
        border-radius: 10px !important;
        padding: 2rem !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #4facfe !important;
        font-weight: 500 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(79,172,254,0.1) !important;
        border-radius: 10px !important;
    }
    
    /* Success messages */
    .success {
        padding: 1rem !important;
        border-radius: 10px !important;
        background-color: rgba(0,255,0,0.1) !important;
        border-left: 5px solid #00ff00 !important;
    }
    
    /* Error messages */
    .stError {
        padding: 1rem !important;
        border-radius: 10px !important;
        background-color: rgba(255,0,0,0.1) !important;
        border-left: 5px solid #ff0000 !important;
    }
</style>
""", unsafe_allow_html=True)

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

# Global variables for audio control
audio_control = {
    'is_playing': False,
    'should_stop': False,
    'audio_thread': None,
    'command_queue': queue.Queue(),
    'current_position': 0,  # Track current position in audio
    'current_text': '',     # Store current text being read
    'sentences': []         # Store text split into sentences
}

def listen_for_commands():
    recognizer = sr.Recognizer()
    while not audio_control['should_stop']:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=1)
                command = recognizer.recognize_google(audio).lower()
                
                if command in ['pause', 'resume', 'repeat', 'skip']:
                    st.session_state['last_command'] = command
                    audio_control['command_queue'].put(command)
                    
                    if command == 'pause':
                        audio_control['is_playing'] = False
                    elif command == 'resume':
                        audio_control['is_playing'] = True
                    elif command == 'repeat':
                        # Stay on current sentence
                        pass
                    elif command == 'skip':
                        # Move to next sentence if available
                        if audio_control['current_position'] < len(audio_control['sentences']) - 1:
                            audio_control['current_position'] += 1
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            continue
        except Exception as e:
            print(f"Error in voice recognition: {str(e)}")

def play_audio_with_controls(text):
    audio_control['current_text'] = text
    audio_control['sentences'] = text.split('.')
    audio_control['current_position'] = 0
    audio_control['is_playing'] = True
    
    while audio_control['current_position'] < len(audio_control['sentences']):
        if audio_control['is_playing']:
            current_sentence = audio_control['sentences'][audio_control['current_position']].strip()
            if current_sentence:  # Skip empty sentences
                tts = gTTS(text=current_sentence, lang='en')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                audio = AudioSegment.from_file(fp, format="mp3")
                play(audio)
                
                # Move to next sentence unless paused or repeating
                if not audio_control['command_queue'].empty():
                    command = audio_control['command_queue'].get()
                    if command == 'skip':
                        continue  # Skip handled in listen_for_commands
                    elif command == 'repeat':
                        continue  # Stay on current sentence
                    elif command == 'pause':
                        while not audio_control['is_playing']:
                            time.sleep(0.1)
                else:
                    audio_control['current_position'] += 1
        
        time.sleep(0.1)  # Prevent CPU overuse

def play_audio_file(audio_path):
    try:
        audio = AudioSegment.from_mp3(audio_path)
        play(audio)
    except Exception as e:
        print(f"Error playing audio: {str(e)}")

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
    # Main title with gradient effect
    st.title("🔮 InkTalk")
    
    # Subtitle with custom styling
    st.markdown("""
        <p style='text-align: center; color: #4facfe; font-size: 1.2rem; margin-bottom: 2rem;'>
        InkTalk : Listen to Your Notes!
            <br/>
            <span style='font-size: 0.9rem; color: #888;'>
                Created by Team Buffering Bytes
            </span>
        </p>
    """, unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 15px;'>
        """, unsafe_allow_html=True)
        
        # Input method selection with custom styling
        input_method = st.radio(
            "✨ Choose Your Input Method",
            ["📤 Upload Image", "📸 Use Camera"],
            key="input_method"
        )
        
        if "📤 Upload Image" in input_method:
            # Enhanced file uploader
            uploaded_file = st.file_uploader(
                "Drop your image here or click to browse",
                type=['png', 'jpg', 'jpeg'],
                help="Supported formats: PNG, JPG, JPEG"
            )
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                process_image(image)
        else:
            # Enhanced camera input
            camera_image = st.camera_input(
                "Capture your handwritten notes",
                help="Make sure you have good lighting!"
            )
            if camera_image is not None:
                image = Image.open(camera_image)
                process_image(image)
                
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Enhanced instructions with modern styling
        with st.expander("🎯 Quick Guide", expanded=True):
            st.markdown("""
            <div style='background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 10px;'>
            <h4 style='color: #4facfe; margin-bottom: 1rem;'>Steps to Success 🚀</h4>
            
            1. 📱 Select your preferred input method
            2. 📄 Upload or capture your handwritten text
            3. ⚡ Click "Convert" to process
            4. 🎧 Listen to your notes
            5. 💾 Download for offline use
            
            <h4 style='color: #4facfe; margin: 1rem 0;'>Pro Tips 💡</h4>
            
            • 📸 Use good lighting
            • ✍️ Ensure clear handwriting
            • 🎨 High contrast is key
            • 📏 Keep images straight
            • 🔍 Avoid blur
            </div>
            """, unsafe_allow_html=True)

def process_image(image):
    # Display image with enhanced styling
    st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 15px; margin: 1rem 0;'>
            <h4 style='color: #4facfe; margin-bottom: 1rem;'>📸 Preview</h4>
        </div>
    """, unsafe_allow_html=True)
    st.image(image, use_container_width=True)

    # Enhanced conversion button
    if st.button('✨ Convert to Text and Speech ✨'):
        with st.spinner('Processing image...'):
            # Extract text
            text = extract_text(image)
            
            if text:
                # Display extracted text with custom styling
                st.markdown("""
                    <div style='background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;'>
                        <h4 style='color: #4facfe; margin-bottom: 1rem;'>📝 Extracted Text</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"<div style='padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 10px;'>{text}</div>", unsafe_allow_html=True)
                
                try:
                    # Convert to speech
                    output_file = f"output_{int(time.time())}.mp3"
                    output_path = text_to_speech(text, output_file)
                    
                    # Create audio player
                    if os.path.exists(output_path):
                        # Read the audio file once and store in memory
                        with open(output_path, "rb") as audio_file:
                            audio_bytes = audio_file.read()
                        
                        # Enhanced audio section with modern styling
                        st.markdown("""
                            <div style='background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;'>
                                <h4 style='color: #4facfe; margin-bottom: 1rem;'>🎵 Audio Controls</h4>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Create columns for audio player, voice control, and download button
                        audio_col1, audio_col2, audio_col3 = st.columns([2, 1, 1])
                        
                        with audio_col1:
                            st.audio(audio_bytes, format='audio/mp3')
                        
                        with audio_col2:
                            # Voice control section
                            st.markdown("""
                                <div style='background: rgba(79,172,254,0.1); padding: 1rem; border-radius: 10px;'>
                                    <h5 style='color: #4facfe; margin-bottom: 0.5rem;'>🎤 Voice Commands</h5>
                                    <small style='color: #888;'>Say:</small>
                                    <ul style='margin: 0; padding-left: 1.2rem;'>
                                        <li>"Play"</li>
                                        <li>"Pause"</li>
                                        <li>"Stop"</li>
                                        <li>"Read"</li>
                                    </ul>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Start voice command listener
                            if st.button('🎤 Start Voice Control'):
                                audio_control['should_stop'] = False
                                audio_control['audio_thread'] = threading.Thread(
                                    target=listen_for_commands,
                                    daemon=True
                                )
                                audio_control['audio_thread'].start()
                        
                        with audio_col3:
                            # Stylish download button
                            st.download_button(
                                label='💾 Download',
                                data=audio_bytes,
                                file_name='handwriting_audio.mp3',
                                mime='audio/mp3',
                                help='Download the audio file to your device'
                            )
                        
                        # Add success message
                        st.markdown("""
                            <div class='success'>
                                ✨ Audio generated successfully! Click play to listen or download to save.
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating audio: {str(e)}")
            else:
                st.error("No text could be extracted from the image. Please try with a clearer image.")

if __name__ == "__main__":
    main()