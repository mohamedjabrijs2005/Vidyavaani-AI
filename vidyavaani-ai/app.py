import streamlit as st
import os
from audio_recorder_streamlit import audio_recorder

from utils.ai_engine import configure_groq, explain_concept, generate_quiz, get_visual_description, QuotaError
from utils.voice_engine import text_to_speech, transcribe_audio
from components.ui_components import (
    render_header, render_sidebar,
    render_explanation_card, render_visual_card, render_quiz, render_welcome_info
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
    .block-container { padding-top: 5.5rem !important; }
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
            st.audio(st.session_state["explain_audio"], format="audio/mp3")
    else:
        render_welcome_info()

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
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
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
        render_explanation_card(st.session_state["voice_transcribed"], st.session_state["voice_explanation"])
        if st.session_state["voice_audio_out"]:
            st.audio(st.session_state["voice_audio_out"], format="audio/mp3")
    elif audio_bytes and len(audio_bytes) > 5000 and not st.session_state["voice_transcribed"]:
        st.error("❌ Could not understand the audio. Please try speaking clearly or use text mode.")
    elif not audio_bytes and not st.session_state["voice_transcribed"]:
        render_welcome_info()

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
    else:
        render_welcome_info()

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
                with st.spinner("🎨 Creating visual map table..."):
                    visual = get_visual_description(concept.strip())
                st.session_state["visual_map"] = visual
                st.session_state["visual_explanation"] = ""
                st.session_state["visual_audio"] = None
            except QuotaError as qe:
                st.warning(str(qe))
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
        else:
            st.warning("Please enter a concept.")

    # Render persisted card if exists
    if st.session_state["visual_map"]:
        col_v, col_m = st.columns([1, 1])
        with col_v:
            st.markdown("### 🗺️ Smartboard Diagram Table")
            render_visual_card(st.session_state["visual_map"])
        with col_m:
            st.markdown("### 🎬 Media & Reference Hub")
            v_concept = st.session_state["visual_concept"]
            encoded_concept = v_concept.replace(" ", "+")
            images_url = f"https://www.google.com/search?tbm=isch&q={encoded_concept}+diagram"
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_concept}+educational+explanation"
            khan_url = f"https://www.khanacademy.org/search?page_search_query={encoded_concept}"
            wikipedia_url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_concept}"
            
            st.markdown(f"""
            <div class="vv-card" style="border-left: 5px solid #1a73e8; background: linear-gradient(to right, #f8fafc, #ffffff); padding: 1.6rem; border-radius: 16px; height: 100%;">
                <h4 style="color: #1a73e8; font-weight: 700; margin-top: 0; margin-bottom: 0.8rem;">🎬 Classroom Resources</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.4rem;">
                    Click the buttons below to open curated interactive teaching resources for <b>{v_concept}</b>:
                </p>
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <a href="{images_url}" target="_blank" style="background: linear-gradient(135deg, #1a73e8, #1558b0); color: white !important; padding: 0.8rem 1.2rem; border-radius: 12px; text-decoration: none; font-weight: 600; display: block; text-align: center; box-shadow: 0 4px 12px rgba(26,115,232,0.2); font-size: 0.95rem;">📷 Open Diagram & Photo Gallery</a>
                    <a href="{youtube_url}" target="_blank" style="background: linear-gradient(135deg, #ff0000, #cc0000); color: white !important; padding: 0.8rem 1.2rem; border-radius: 12px; text-decoration: none; font-weight: 600; display: block; text-align: center; box-shadow: 0 4px 12px rgba(255,0,0,0.2); font-size: 0.95rem;">🎥 Watch Educational Videos on YouTube</a>
                    <a href="{khan_url}" target="_blank" style="background: linear-gradient(135deg, #0c6623, #084c1a); color: white !important; padding: 0.8rem 1.2rem; border-radius: 12px; text-decoration: none; font-weight: 600; display: block; text-align: center; box-shadow: 0 4px 12px rgba(12,102,35,0.2); font-size: 0.95rem;">📖 Lessons on Khan Academy</a>
                    <a href="{wikipedia_url}" target="_blank" style="background: linear-gradient(135deg, #374151, #1f2937); color: white !important; padding: 0.8rem 1.2rem; border-radius: 12px; text-decoration: none; font-weight: 600; display: block; text-align: center; box-shadow: 0 4px 12px rgba(55,65,81,0.2); font-size: 0.95rem;">🧠 Wikipedia Academic Articles</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        render_welcome_info()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#64748b; font-size:0.85rem; padding-bottom:1.5rem;'>
    VidyaVaani AI · Built for Connecting Dreams Foundation · Round 2 Assignment<br>
    Supports Tamil · Hinglish  · English | Grades 6-12
</div>
""", unsafe_allow_html=True)
