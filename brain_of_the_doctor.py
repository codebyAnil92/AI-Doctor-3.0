import os
import logging
import mimetypes 
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Step 1: Configuration and API Key (CRITICAL FIX) ---

# 🚨 IMPORTANT: PASTE YOUR BRAND NEW, UNREVOKED GEMINI API KEY HERE.
MY_ACTUAL_GEMINI_KEY = "AIzaSyAkA0Kf8q1coY2hLCVmw2SMPivlREvgSf4" 

# CRITICAL FIX 1: Assign the key directly.
GEMINI_API_KEY = MY_ACTUAL_GEMINI_KEY

# CRITICAL FIX 2: Define the model
VISION_MODEL = "gemini-2.5-flash"

if not GEMINI_API_KEY or "PASTE_YOUR_BRAND_NEW_GEMINI_KEY_HERE" in GEMINI_API_KEY:
    logging.error("❌ FATAL: GEMINI_API_KEY is missing or invalid. Please update the key.")


# --- Step 2: Multimodal LLM Analysis Function (CRITICAL FILE FIX) ---

def analyze_image_with_query(query: str, image_path: str, system_prompt: str) -> str:
    """
    Analyzes an image and a text query using the Gemini API.
    Uses raw bytes to bypass path/file errors.
    """
    
    if not GEMINI_API_KEY:
        return f"Service Error: Gemini API Key not configured."
    
    if not image_path or not os.path.exists(image_path):
        return f"File Error: The image file was not found. Please ensure the file is correctly uploaded."
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = "image/jpeg"
        
        logging.info(f"Processing image: {os.path.basename(image_path)} with MIME type: {mime_type}")
        
        # Read the file content into memory (bytes) manually
        with open(image_path, "rb") as f:
            image_data = f.read()

        image_part = types.Part.from_bytes(data=image_data, mime_type=mime_type)
        
        prompt_parts = [
            image_part,
            query
        ]

        response = client.models.generate_content(
            model=VISION_MODEL,
            contents=prompt_parts,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        
        return response.text.replace('\n', ' ').strip()
        
    except Exception as e:
        logging.error(f"Gemini API call failed. Detail: {e}")
        return f"API Call Error: The external LLM service failed. Detail: {e}"