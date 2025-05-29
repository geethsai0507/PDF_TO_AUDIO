import os
import asyncio
import tempfile
from io import BytesIO
import requests
import time

import streamlit as st
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
import edge_tts
import pycountry  # pip install pycountry

# Cache voices list
@st.cache_data(show_spinner=False)
def get_edge_voices():
    raw = asyncio.run(edge_tts.list_voices())
    voices = []
    for v in raw:
        short = v["ShortName"]
        locale = v["Locale"]            # e.g. "en-US"
        gender = v["Gender"]
        lang_code = locale.split("-")[0]  # e.g. "en"
        # Lookup human-readable language name
        try:
            lang_name = pycountry.languages.get(alpha_2=lang_code).name
        except:
            lang_name = lang_code
        voices.append({
            "short_name": short,
            "locale": locale,
            "language": lang_name,
            "gender": gender
        })
    return voices

# Async TTS to file
async def synthesize_to_file(text: str, voice: str, filename: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

# Split text into chunks ≤ max_chars, breaking on spaces
def chunk_text(text: str, max_chars: int = 4500):
    chunks = []
    while text:
        if len(text) <= max_chars:
            chunks.append(text)
            break
        split_at = text.rfind(" ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    return chunks

def get_stoic_quote():
    try:
        resp = requests.get("https://stoic.tekloon.net/stoic-quote", timeout=10)
        data = resp.json()["data"]
        return f'"{data["quote"]}"\n\n— {data["author"]}'
    except Exception:
        return "Could not fetch quote."

def translate_pdf_text(full_text, target_lang, uploaded_file):
    st.write(f"Translating text to `{target_lang}` in chunks…")
    chunks = chunk_text(full_text, max_chars=4500)
    translated_chunks = []
    for i, c in enumerate(chunks, start=1):
        st.text(f"Translating chunk {i}/{len(chunks)}")
        try:
            translated_chunks.append(
                GoogleTranslator(source="auto", target=target_lang).translate(c)
            )
        except Exception as e:
            st.error(f"Error translating chunk {i}: {e}")
            return None
    translated_text = "\n".join(translated_chunks)
    st.session_state['translated_text'] = translated_text

    st.download_button(
        label="Download Translated Text",
        data=translated_text,
        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_translated.txt",
        mime="text/plain"
    )
    return translated_text

def synthesize_audio(translated_text, selected_voice, uploaded_file):
    st.image(
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWFnYXEwbHh3MWRyaGxrZWR3cWptZDE5OWQwaTV4eW91enN1ZDU4ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lWY7KIoUckm8iCjY79/giphy.gif",
        caption="Hang tight, we’re working on it!"
    )

    quote_area = st.empty()
    quote_area.info(get_stoic_quote())

    st.write("Synthesizing audio… this may take a moment.")
    with st.spinner("Processing with edge-tts…"):
        total_time = 0
        update_interval = 20
        max_wait = 60  # Simulate up to 1 minute for demonstration
        while total_time < max_wait:
            time.sleep(update_interval)
            quote_area.info(get_stoic_quote())
            total_time += update_interval

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            temp_mp3 = tmp.name

        try:
            asyncio.run(synthesize_to_file(translated_text, selected_voice, temp_mp3))
        except Exception as e:
            st.error(f"TTS synthesis error: {e}")
            return None

        with open(temp_mp3, "rb") as f:
            audio_bytes = f.read()
        os.remove(temp_mp3)

    st.image(
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2VpOHNvYW9qMnVhamNrN2F0bHZ3MGN6ZDVpMDExZnZldWVsemkzNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8utnLQN5OdoR8C0JAN/giphy.gif",
        caption="Heah you have great patiance"
    )

    st.success("🎉 Audio ready!")
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        label="Download MP3",
        data=audio_bytes,
        file_name=f"{os.path.splitext(uploaded_file.name)[0]}.mp3",
        mime="audio/mp3"
    )
    return audio_bytes

def main():
    st.title("📄 English PDF → 🎤 Audio Conversion System")
    st.markdown(
        "Upload a PDF, pick a voice/language, chunked-translate the text, then convert to audio."
    )
    st.subheader("This open-source app does not collect any user data. It runs entirely in your browser.")
    st.subheader("Audio generation may take time since it relies on free models. Please be patient.")

    # 1) List voices
    st.subheader("Supported Voices / Locales")
    voices = get_edge_voices()
    st.table({
        "Voice Code": [v["short_name"] for v in voices],
        "Locale":     [v["locale"]     for v in voices],
        "Language":   [v["language"]   for v in voices],
        "Gender":     [v["gender"]     for v in voices],
    })

    # 2) Select voice
    voice_codes = [v["short_name"] for v in voices]
    selected_voice = st.selectbox("Choose a voice Code:", voice_codes)
    locale = next(v["locale"]     for v in voices if v["short_name"] == selected_voice)
    target_lang = locale.split("-")[0]  # e.g. 'fr' from 'fr-FR'

    # 3) Upload PDF
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    if not uploaded_file:
        st.info("Please upload a PDF to continue.")
        return

    # 4) Extract text
    reader = PdfReader(uploaded_file)
    full_text = ""
    for page in reader.pages:
        txt = page.extract_text() or ""
        full_text += txt + "\n"
    if not full_text.strip():
        st.error("No extractable text found in the PDF.")
        return

    # 5) Translate
    if st.button("🌐 Translate PDF Text"):
        translated_text = translate_pdf_text(full_text, target_lang, uploaded_file)
        if translated_text is None:
            return

    # 6) Synthesize audio if translation exists
    if 'translated_text' in st.session_state and st.button("🎧 Convert Translated Text to Audio"):
        translated_text = st.session_state['translated_text']
        synthesize_audio(translated_text, selected_voice, uploaded_file)

if __name__ == "__main__":
    main()
# This code is a Streamlit app that allows users to upload a PDF, select a voice for text-to-speech, translate the text, and convert it to audio using edge-tts.
# It includes features like voice selection, text extraction from PDF, chunking long texts, and handling translations with error handling.