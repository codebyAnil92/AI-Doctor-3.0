import os
import gradio as gr
import logging

# Import the corrected functions 
from brain_of_the_doctor import analyze_image_with_query
# Note: transcribe_with_groq now uses the free Google STT
from voice_of_the_patient import transcribe_with_groq 
from voice_of_the_doctor import text_to_speech_with_gtts_old 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration (MULTILINGUAL PROMPT FIX) ---

SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
    What's in this image?. Do you find anything wrong with it medically? 
    If you make a differential, suggest some remedies for them. 
    
    CRITICAL INSTRUCTION: Respond in the exact language of the patient's query. If the query is in Hindi, respond in Hindi. If it is in Kannada, respond in Kannada.
    
    Donot add any numbers or special characters in your response. Your response should be in one long paragraph. 
    Also always answer as if you are answering to a real person. Donot say 'In the image I see' but say 'With what I see, I think you have ....'
    Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
    Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


# --- Main Logic (NEW LANGUAGE PARAMETER) ---

def process_inputs(audio_filepath, image_filepath, response_language):
    """
    Handles the transcription, image analysis, and TTS generation pipeline.
    
    Returns: transcribed_text (str), doctor_response (str), voice_of_doctor (filepath)
    """
    speech_to_text_output = ""
    doctor_response = ""
    temp_output_file = os.path.join(os.path.dirname(__file__), "doctor_response.mp3")

    # 1. Speech to Text (STT)
    if audio_filepath:
        try:
            # transcribe_with_groq now uses the free Google STT (and ignores the STT_MODEL argument)
            # We pass a placeholder value (e.g., None) for the now-unused model argument.
            speech_to_text_output = transcribe_with_groq(None, audio_filepath) 
        except Exception as e:
            logging.error(f"Transcription failed: {e}")
            return f"Transcription Error: Failed to process audio. Detail: {e}", "", None
    else:
        speech_to_text_output = "No voice query provided."

    # 2. Multimodal LLM Analysis
    if image_filepath and os.path.exists(image_filepath):
        try:
            doctor_response = analyze_image_with_query(
                query=speech_to_text_output, 
                image_path=image_filepath, 
                system_prompt=SYSTEM_PROMPT
            )
        except Exception as e:
            logging.error(f"LLM analysis failed: {e}")
            doctor_response = f"LLM Error: Could not generate response. Detail: {e}"
    else:
        # If no image is provided, respond only to text query
        doctor_response = f"Your voice input was: {speech_to_text_output}. Please provide an image for analysis."

    # 3. Text to Speech (TTS) - Using the multilingual gTTS function
    try:
        text_to_speech_with_gtts_old(
            input_text=doctor_response, 
            output_filepath=temp_output_file,
            language_code=response_language 
        )
        return speech_to_text_output, doctor_response, temp_output_file
        
    except Exception as e:
        logging.error(f"TTS generation failed: {e}")
        return speech_to_text_output, doctor_response, f"Error generating TTS audio in language code '{response_language}'. Detail: {e}"


# --- Gradio Interface ---

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="1. Record Patient's Voice"),
        gr.Image(type="filepath", label="2. Upload Medical Image (Optional)"),
        gr.Dropdown(
            choices=[("English", "en"), ("Hindi (हिंदी)", "hi"), ("Kannada (ಕನ್ನಡ)", "kn")],
            value="en",
            label="3. Select Response Language (Doctor's Voice)"
        )
    ],
    outputs=[
        gr.Textbox(label="4. Patient's Speech (Text)", lines=3),
        gr.Textbox(label="5. Doctor's Medical Response", lines=5),
        gr.Audio(label="6. Doctor's Voice", value=None) 
    ],
    title="Gemini-Powered Voice-and-Vision AI Doctor (Multilingual & Free-Tier API)",
    description="Speak your symptoms and upload a medical image. The AI will transcribe your query (in any language) and respond in the selected language.",
    theme="gradio/monochrome"
)

if __name__ == "__main__":
    iface.launch()