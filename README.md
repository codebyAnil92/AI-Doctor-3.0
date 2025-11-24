# 🩺 Gemini-Powered Multilingual AI Doctor (Voice & Vision)

A multimodal AI application that acts as a preliminary medical assistant. Patients can submit a voice query (in English, Hindi, or Kannada) and an optional image (e.g., a skin condition, X-ray) through a simple Gradio web interface. The system uses Google Gemini for combined analysis and responds verbally in the user's selected language.

---

## ✨ Features

* **Multimodal Analysis**: Uses the **Google Gemini 2.5 Flash** model to analyze text query and image input simultaneously.
* **Multilingual Speech-to-Text (STT)**: Transcribes voice input in **English, Hindi, or Kannada** using the free Google Speech Recognition service.
* **Multilingual Text-to-Speech (TTS)**: Generates the doctor's audio response in **English (`en`), Hindi (`hi`), or Kannada (`kn`)** using the free `gTTS` library.
* **Intuitive UI**: Hosted via a Gradio interface for easy interaction in the browser.

---

## ⚙️ Prerequisites

You must have the following system dependencies installed before setting up the Python environment:

1.  **Python 3.8+**
2.  **FFmpeg**: Required by the `pydub` library for handling and converting audio files.
    * **Windows**: Recommended to install via a package manager like Chocolatey (`choco install ffmpeg`).
    * **macOS**: Install via Homebrew (`brew install ffmpeg`).
    * **Linux (Debian/Ubuntu)**: Install via `sudo apt update && sudo apt install ffmpeg`.

---

## 🚀 Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/codebyanil92/AI-Doctor-2.0.git](https://github.com/codebyanil/AI-Doctor-2.0.git)
    cd AI-Doctor-2.0
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/macOS
    venv\Scripts\activate      # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🔑 Configuration

You need to obtain a **Google Gemini API Key** and insert it directly into the codebase.

1.  Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Open **`brain_of_the_doctor.py`**.
3.  Replace the placeholder with your actual key:

    ```python
    # brain_of_the_doctor.py
    MY_ACTUAL_GEMINI_KEY = "PASTE_YOUR_BRAND_NEW_GEMINI_KEY_HERE" 
    ```

    > **Note**: This project no longer requires API keys for Groq or ElevenLabs.

---

## ▶️ How to Run

1.  Ensure your virtual environment is active (`source venv/bin/activate`).
2.  Run the main application file:
    ```bash
    python gradio_app.py
    ```
3.  The application will start, and a link (usually `http://127.0.0.1:7860/`) will appear in your console. Open this link in your web browser.

## 📁 Project Structure