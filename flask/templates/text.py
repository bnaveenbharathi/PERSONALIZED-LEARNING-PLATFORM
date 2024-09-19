import cv2
import sounddevice as sd
import queue
import vosk
import json
from googletrans import Translator
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import numpy as np

# Initialize Vosk model for speech recognition
model = vosk.Model("path_to_vosk_model")

# Initialize queue to handle audio input
q = queue.Queue()

# Initialize Google Translate API
translator = Translator()

# Initialize Text-to-Speech (TTS) engine
engine = pyttsx3.init()

# Function to capture audio in real-time
def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

def real_time_speech_to_text():
    """Real-time speech-to-text function using Vosk"""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result['text']  # Return the recognized text

# Function to translate text using Google Translate API
def translate_text(text, target_language):
    """Translate the recognized speech to the target language."""
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Function to convert translated text to speech
def text_to_speech(text):
    """Convert translated text to speech and play it"""
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()
    
    # Play the translated speech audio
    translated_audio = AudioSegment.from_mp3("output.mp3")
    play(translated_audio)

# Main function to process video and audio simultaneously with translation and TTS
def process_video(video_path, target_language='fr'):
    cap = cv2.VideoCapture(video_path)
    
    # Start audio capture for speech-to-text
    while cap.isOpened():
        ret, frame = cap.read()  # Read frame from the video
        if not ret:
            break
        
        # Display video frame
        cv2.imshow('Video', frame)
        
        # Get live speech-to-text
        recognized_text = real_time_speech_to_text()
        
        if recognized_text:
            # Translate the recognized text
            translated_text = translate_text(recognized_text, target_language)
            print(f"Recognized: {recognized_text} | Translated: {translated_text}")
            
            # Convert the translated text to speech and play it
            text_to_speech(translated_text)
            
            # Display the translated text on the video frame (as subtitles)
            frame = cv2.putText(frame, translated_text, (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Display the frame with subtitles
        cv2.imshow('Video with Translation', frame)

        # Press 'q' to quit the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    video_file = "input_video.mp4"  # Path to your video file
    target_lang = "fr"  # Target language for translation, e.g., 'fr' for French
    
    # Call the main function to process the video and translate it live
    process_video(video_file, target_lang)
