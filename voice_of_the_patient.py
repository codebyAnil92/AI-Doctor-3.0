import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
# Groq dependency has been removed to eliminate the GROQ_API_KEY requirement

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# NOTE: The record_audio function is removed as Gradio handles the microphone recording.
# STT_MODEL and GROQ_API_KEY are no longer needed.

# --- Speech to Text (STT) Function (Using Google's free STT) ---

def transcribe_with_groq(stt_model_unused, audio_filepath):
    """
    Transcribes an audio file using the free Google Speech Recognition.
    
    NOTE: This function is renamed to 'transcribe_with_groq' to avoid modifying 
    the import in your 'gradio_app.py', but it now uses the free Google API.
    The 'stt_model_unused' argument is ignored.
    """
    recognizer = sr.Recognizer()
    
    try:
        # Load the audio file (Gradio provides a filepath, usually a WAV file)
        with sr.AudioFile(audio_filepath) as source:
            audio = recognizer.record(source) # read the entire audio file
            
            logging.info("Sending audio to Google Speech Recognition...")
            
            # Use recognize_google for free, multilingual transcription (auto-detects Hindi/Kannada/English)
            transcription = recognizer.recognize_google(audio)
            
            return transcription
            
    except sr.UnknownValueError:
        logging.warning("Google Speech Recognition could not understand audio.")
        return "Audio not clear or no speech detected."
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        return f"STT Service Error: Failed to contact Google API. Detail: {e}"
    except Exception as e:
        logging.error(f"General transcription error: {e}")
        return f"Transcription Error: Failed to process audio. Detail: {e}"