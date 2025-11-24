import os
import logging
from gtts import gTTS
# Removed unused imports

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Step 1a: TTS with gTTS (Multilingual Save Function) ---

def text_to_speech_with_gtts_old(input_text, output_filepath, language_code="en"):
    """
    Saves text-to-speech audio to a file using gTTS.
    Supports multilingual output (e.g., 'en', 'hi', 'kn').
    """
    try:
        audioobj = gTTS(
            text=input_text,
            lang=language_code, # Uses dynamic language code
            slow=False
        )
        audioobj.save(output_filepath)
        logging.info(f"gTTS audio saved to {output_filepath} in language code: {language_code}")
    except Exception as e:
        logging.error(f"gTTS failed for language code '{language_code}': {e}")
        raise