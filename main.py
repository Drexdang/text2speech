import streamlit as st
import os
import time
import glob
from gtts import gTTS
from deep_translator import GoogleTranslator

# Create a temporary folder to save audio files
try:
    os.mkdir("temp")
except FileExistsError:
    pass

st.title("Text to Speech By Drex-Dang")

# Input text
text = st.text_input("Enter text")

# Input language selection
in_lang = st.selectbox(
    "Select your input language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
)

lang_dict = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja"
}

input_language = lang_dict[in_lang]

# Output language selection
out_lang = st.selectbox(
    "Select your output language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
)

output_language = lang_dict[out_lang]

# English accent selection
english_accent = st.selectbox(
    "Select your English accent",
    ("Default", "India", "United Kingdom", "United States", "Canada", "Australia", "Ireland", "South Africa"),
)

tld_dict = {
    "Default": "com",
    "India": "co.in",
    "United Kingdom": "co.uk",
    "United States": "com",
    "Canada": "ca",
    "Australia": "com.au",
    "Ireland": "ie",
    "South Africa": "co.za"
}

tld = tld_dict[english_accent]

# Function to translate text and convert to speech
def text_to_speech(input_language, output_language, text, tld):
    translator = GoogleTranslator(source=input_language, target=output_language)
    trans_text = translator.translate(text)
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    file_name = text[:20].replace(' ', '_') if text else "audio"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_name, trans_text

# Checkbox to display output text
display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
    if text.strip():  # Check if text is not empty
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file_path = f"temp/{result}.mp3"
        audio_bytes = open(audio_file_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        if display_output_text:
            st.markdown("## Output text:")
            st.write(output_text)
    else:
        st.error("Please enter some text to convert.")

# Function to remove files older than n days
def remove_files(n_days):
    now = time.time()
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - n_days * 86400:
            os.remove(f)
            print("Deleted", f)

# Remove files older than 7 days
remove_files(7)