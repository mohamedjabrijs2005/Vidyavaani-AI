from gtts import gTTS
import io
import base64
import streamlit as st


# ── Text → Speech ──────────────────────────────────────────────────────────────
LANG_CODE = {
    "Tamil":    "ta",
    "Hinglish": "hi",
    "English":  "en",
}

def text_to_speech(text: str, language: str) -> bytes:
    """Convert text to MP3 bytes using gTTS."""
    lang_code = LANG_CODE.get(language, "en")
    tts = gTTS(text=text, lang=lang_code, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def autoplay_audio(audio_bytes: bytes):
    """Embed audio in Streamlit page and autoplay it."""
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


# ── Speech → Text (from uploaded/recorded WAV bytes) ──────────────────────────
def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe audio bytes to text using Google Web Speech API (free, online).
    Returns transcribed string or empty string on failure.
    """
    try:
        import speech_recognition as sr
    except ImportError as err:
        raise ImportError(
            "SpeechRecognition is not installed. Please install it with `pip install SpeechRecognition` "
            "or add `SpeechRecognition==3.10.4` to requirements.txt."
        ) from err
    # Convert WebM/OGG/other formats to standard mono 16kHz WAV using pydub
    try:
        from pydub import AudioSegment
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        audio_bytes = wav_io.getvalue()
    except Exception as e:
        # Fall back to using the raw bytes directly if pydub fails
        pass

    import tempfile
    import os

    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""
    finally:
        os.unlink(tmp_path)
