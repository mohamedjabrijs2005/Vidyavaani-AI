import streamlit as st
import os
from audio_recorder_streamlit import audio_recorder

from utils.ai_engine import configure_groq, explain_concept, generate_quiz, get_visual_description, QuotaError
from utils.voice_engine import text_to_speech, autoplay_audio, transcribe_audio
from components.ui_components import (
    render_header, render_sidebar,
    render_explanation_card, render_visual_card, render_quiz
)

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VidyaVaani AI – Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom global padding adjustments
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Render premium header
render_header()
# Render sidebar menu (now only outputs settings and modes)
language, grade, mode = render_sidebar()

# ── API Key Loading & Guard ───────────────────────────────────────────────────
api_key = None

# 1. Try to load from Streamlit secrets
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

# 2. Try to load from environment variables
if not api_key:
    api_key = os.environ.get("GROQ_API_KEY")

# Check if key is configured
if not api_key or api_key == "your-api-key-here":
    st.info("💡 **Welcome to VidyaVaani AI!**")
    st.markdown(f"""
    <div style='background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;'>
        <h4 style='color: #b45309; margin: 0 0 0.5rem 0;'>🔑 Configuration Required</h4>
        <p style='color: #78350f; margin: 0; font-size: 0.95rem; line-height: 1.6;'>
            To use this assistant, please configure your Groq API Key in the backend secrets:
            <br><br>
            1. Open the file <b><a href="file:///c:/Users/safik/Desktop/CDG%20Project/vidyavaani-ai/ai-teaching-assistant/.streamlit/secrets.toml">.streamlit/secrets.toml</a></b> in your text editor.
            2. Replace <code>"your-api-key-here"</code> with your actual Groq API key from <a href="https://console.groq.com" target="_blank">Groq Console</a>.
            3. Save the file and reload the web app.
            <br><br>
            <i>Note: You can also set it as the <code>GROQ_API_KEY</code> environment variable.</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

configure_groq(api_key)

# ══════════════════════════════════════════════════════════════════════════════
# MODE 1 — Explain Concept
# ══════════════════════════════════════════════════════════════════════════════
if mode == "📖 Explain Concept":
    st.markdown("## 📖 Concept Explainer")
    st.markdown("Type any topic from your syllabus and get a simple, clear explanation.")

    # Initialize concept explainer session states
    if "explain_concept" not in st.session_state:
        st.session_state["explain_concept"] = ""
    if "explain_result" not in st.session_state:
        st.session_state["explain_result"] = ""
    if "explain_audio" not in st.session_state:
        st.session_state["explain_audio"] = None

    concept = st.text_input(
        "Enter a concept",
        value=st.session_state["explain_concept"],
        placeholder="e.g., Photosynthesis, Pythagoras Theorem, French Revolution..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        explain_btn = st.button("✨ Explain", use_container_width=True)
    with col2:
        speak_btn = st.button("🔊 Explain & Speak", use_container_width=True)

    if (explain_btn or speak_btn) and concept.strip():
        st.session_state["explain_concept"] = concept.strip()
        try:
            with st.spinner("🤔 Thinking..."):
                explanation = explain_concept(concept.strip(), language, grade)
            st.session_state["explain_result"] = explanation
            if speak_btn:
                with st.spinner("🔊 Generating audio..."):
                    audio = text_to_speech(explanation, language)
                st.session_state["explain_audio"] = audio
            else:
                st.session_state["explain_audio"] = None
        except QuotaError as qe:
            st.warning(str(qe))
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

    elif (explain_btn or speak_btn) and not concept.strip():
        st.warning("Please enter a concept first.")

    # Render persisted card if exists
    if st.session_state["explain_result"]:
        render_explanation_card(st.session_state["explain_concept"], st.session_state["explain_result"])
        if st.session_state["explain_audio"]:
            autoplay_audio(st.session_state["explain_audio"])
            st.audio(st.session_state["explain_audio"], format="audio/mp3")

# ══════════════════════════════════════════════════════════════════════════════
# MODE 2 — Voice Input
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🎤 Voice Input":
    st.markdown("## 🎤 Ask by Voice")
    st.markdown("Record your question and the AI will explain it in your language.")
    st.info("🎙️ Click the microphone button below, speak your question, then click again to stop.")

    audio_bytes = audio_recorder(
        text="Click to record",
        recording_color="#e8533a",
        neutral_color="#1a73e8",
        icon_size="2x",
    )

    # Initialize voice session states
    if "voice_audio" not in st.session_state:
        st.session_state["voice_audio"] = None
    if "voice_transcribed" not in st.session_state:
        st.session_state["voice_transcribed"] = ""
    if "voice_explanation" not in st.session_state:
        st.session_state["voice_explanation"] = ""
    if "voice_audio_out" not in st.session_state:
        st.session_state["voice_audio_out"] = None

    if audio_bytes:
        # Check if the audio is new to prevent infinite loops on page rerun
        if st.session_state["voice_audio"] != audio_bytes:
            st.session_state["voice_audio"] = audio_bytes
            try:
                with st.spinner("🔍 Transcribing your voice..."):
                    transcribed = transcribe_audio(audio_bytes)
                st.session_state["voice_transcribed"] = transcribed
            except ImportError as ie:
                st.error(f"❌ {ie}")
                st.session_state["voice_transcribed"] = ""
                st.session_state["voice_explanation"] = ""
                st.session_state["voice_audio_out"] = None
            else:
                if transcribed:
                    try:
                        with st.spinner("🤔 Generating explanation..."):
                            explanation = explain_concept(transcribed, language, grade)
                        st.session_state["voice_explanation"] = explanation
                        with st.spinner("🔊 Generating spoken answer..."):
                            audio_out = text_to_speech(explanation, language)
                        st.session_state["voice_audio_out"] = audio_out
                    except QuotaError as qe:
                        st.warning(str(qe))
                    except Exception as e:
                        st.error(f"⚠️ Unexpected error: {e}")
                else:
                    st.session_state["voice_transcribed"] = ""
                    st.session_state["voice_explanation"] = ""
                    st.session_state["voice_audio_out"] = None

    # Render persisted card if exists
    if st.session_state["voice_transcribed"]:
        st.success(f"📝 You asked: **{st.session_state['voice_transcribed']}**")
        render_explanation_card(st.session_state["voice_transcribed"], st.session_state["voice_explanation"])
        if st.session_state["voice_audio_out"]:
            autoplay_audio(st.session_state["voice_audio_out"])
            st.audio(st.session_state["voice_audio_out"], format="audio/mp3")
    elif audio_bytes and not st.session_state["voice_transcribed"]:
        st.error("❌ Could not understand the audio. Please try speaking clearly or use text mode.")

# ══════════════════════════════════════════════════════════════════════════════
# MODE 3 — Quiz Me
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🧠 Quiz Me":
    st.markdown("## 🧠 Quiz Generator")
    st.markdown("Test your understanding with AI-generated MCQ questions.")

    concept = st.text_input(
        "Topic to be quizzed on",
        placeholder="e.g., Laws of Motion, Cell Division, World War II..."
    )

    num_q = st.slider("Number of Questions", min_value=2, max_value=5, value=3)

    if st.button("🎯 Generate Quiz", use_container_width=False):
        if concept.strip():
            with st.spinner("📝 Creating your quiz..."):
                try:
                    questions = generate_quiz(concept.strip(), language, num_q)
                    st.session_state["quiz_questions"] = questions
                    st.session_state["quiz_concept"] = concept.strip()
                    if "quiz_answers" in st.session_state:
                        st.session_state["quiz_answers"] = {}
                    if "quiz_checked" in st.session_state:
                        st.session_state["quiz_checked"] = {}
                except QuotaError as qe:
                    st.warning(str(qe))
                except Exception as e:
                    st.error(f"Failed to generate quiz: {e}")
        else:
            st.warning("Please enter a topic.")

    if "quiz_questions" in st.session_state:
        render_quiz(st.session_state["quiz_questions"])

# ══════════════════════════════════════════════════════════════════════════════
# MODE 4 — Visual Map
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🗺️ Visual Map":
    st.markdown("## 🗺️ Concept Visual Map")
    st.markdown("Get a smartboard-ready visual diagram of any concept.")

    # Initialize visual session states
    if "visual_concept" not in st.session_state:
        st.session_state["visual_concept"] = ""
    if "visual_map" not in st.session_state:
        st.session_state["visual_map"] = ""
    if "visual_explanation" not in st.session_state:
        st.session_state["visual_explanation"] = ""
    if "visual_audio" not in st.session_state:
        st.session_state["visual_audio"] = None

    concept = st.text_input(
        "Enter concept for visual map",
        value=st.session_state["visual_concept"],
        placeholder="e.g., Water Cycle, Digestive System, Ohm's Law..."
    )

    if st.button("🖼️ Generate Visual Map", use_container_width=False):
        if concept.strip():
            st.session_state["visual_concept"] = concept.strip()
            try:
                with st.spinner("🎨 Creating visual map..."):
                    visual = get_visual_description(concept.strip())
                    explanation = explain_concept(concept.strip(), language, grade)
                st.session_state["visual_map"] = visual
                st.session_state["visual_explanation"] = explanation
                with st.spinner("🔊 Narrating explanation..."):
                    audio = text_to_speech(explanation, language)
                st.session_state["visual_audio"] = audio
            except QuotaError as qe:
                st.warning(str(qe))
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
        else:
            st.warning("Please enter a concept.")

    # Render persisted card if exists
    if st.session_state["visual_map"]:
        col_v, col_e = st.columns([1, 1])
        with col_v:
            st.markdown("### 🗺️ Diagram")
            render_visual_card(st.session_state["visual_map"])
        with col_e:
            st.markdown("### 📖 Explanation")
            render_explanation_card(st.session_state["visual_concept"], st.session_state["visual_explanation"])
        
        if st.session_state["visual_audio"]:
            autoplay_audio(st.session_state["visual_audio"])
            st.audio(st.session_state["visual_audio"], format="audio/mp3")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#64748b; font-size:0.85rem; padding-bottom:1.5rem;'>
    VidyaVaani AI · Built for Connecting Dreams Foundation · Round 2 Assignment<br>
    Supports Tamil · Hinglish  · English | Grades 6-12
</div>
""", unsafe_allow_html=True)
