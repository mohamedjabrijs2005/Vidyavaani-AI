import streamlit as st
import os

def render_header():
    """Inject premium CSS and render the main header banner."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        /* ── Global ────────────────────────────────── */
        html, body, .stApp, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }
        .block-container { padding-top: 1.2rem !important; }
        footer { visibility: hidden; }
        #MainMenu { visibility: hidden; }

        /* ── Sidebar — dark premium ────────────────── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b192c 0%, #1d3557 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: #e2e8f0 !important;
            font-family: 'Outfit', sans-serif !important;
        }
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stRadio p {
            color: #cbd5e1 !important;
            font-size: 0.92rem;
        }
        section[data-testid="stSidebar"] [data-baseweb="select"] {
            background-color: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            border-radius: 10px !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="radio"] > div {
            background-color: rgba(255,255,255,0.05) !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.8rem !important;
            margin-bottom: 0.3rem !important;
            border: 1px solid rgba(255,255,255,0.08);
            transition: background 0.2s;
        }
        section[data-testid="stSidebar"] [data-baseweb="radio"] > div:hover {
            background-color: rgba(26,115,232,0.25) !important;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.1) !important;
        }

        /* ── Header Banner ─────────────────────────── */
        .vv-banner {
            background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
            border-radius: 20px;
            padding: 2.2rem 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 16px 40px -12px rgba(26,115,232,0.4);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .vv-banner::before {
            content: '';
            position: absolute; top: -40%; right: -20%;
            width: 350px; height: 350px;
            background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 65%);
            pointer-events: none;
        }
        .vv-banner h1 {
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin: 0 0 0.4rem 0 !important;
            letter-spacing: -0.02em;
        }
        .vv-banner p {
            color: #c3d6f7 !important;
            font-size: 1.1rem;
            margin: 0 !important;
            font-weight: 400;
        }

        /* ── Content Cards ─────────────────────────── */
        .vv-card {
            background: white;
            border-radius: 16px;
            padding: 1.8rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
            margin-top: 1.2rem;
            border: 1px solid #e8edf5;
            transition: box-shadow 0.2s;
        }
        .vv-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

        .vv-explain-card {
            border-left: 5px solid #1a73e8;
            background: linear-gradient(to right, #f0f7ff, #ffffff);
        }
        .vv-explain-card h4 {
            color: #1a73e8 !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            margin: 0 0 0.8rem 0 !important;
        }
        .vv-explain-card p {
            color: #334155;
            font-size: 1.02rem;
            line-height: 1.8;
            margin: 0;
        }

        .vv-visual-card {
            background: #0d1b2a;
            border-left: 5px solid #f59e0b;
            border-radius: 16px;
            padding: 1.6rem;
            color: #e2e8f0 !important;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            font-size: 0.92rem;
            line-height: 1.6;
            overflow-x: auto;
            margin-top: 1.2rem;
        }

        /* ── Score Card ────────────────────────────── */
        .vv-score-card {
            background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
            border: 1px solid #bae6fd;
            border-radius: 14px;
            padding: 1.4rem;
            text-align: center;
            margin-top: 1.5rem;
        }
        .vv-score-card h4 { color: #0369a1 !important; font-size: 1.25rem !important; margin: 0 0 0.3rem 0 !important; }
        .vv-score-card p  { color: #0c4a6e; margin: 0; font-size: 0.95rem; }

        /* ── Buttons ───────────────────────────────── */
        .stButton > button {
            background: linear-gradient(135deg, #1a73e8, #1558b0) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.55rem 1.6rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 4px 12px rgba(26,115,232,0.25) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #1558b0, #0d3c7a) !important;
            box-shadow: 0 8px 20px rgba(26,115,232,0.35) !important;
            transform: translateY(-1px) !important;
        }

        /* ── Inputs ────────────────────────────────── */
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 1.5px solid #cbd5e1 !important;
            padding: 0.6rem 1rem !important;
            font-family: 'Outfit', sans-serif !important;
            transition: border-color 0.2s;
        }
        .stTextInput > div > div > input:focus {
            border-color: #1a73e8 !important;
            box-shadow: 0 0 0 3px rgba(26,115,232,0.1) !important;
        }

        /* ── Section headings ─────────────────────── */
        .vv-section-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.3rem;
        }
        .vv-section-sub {
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 1.4rem;
        }
    </style>

    <div class="vv-banner">
        <h1>🎓 VidyaVaani AI</h1>
        <p>Voice-Enabled AI Teaching Assistant · Connecting Dreams Foundation</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with ONLY settings — no content output here."""
    with st.sidebar:
        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
        logo_path = os.path.normpath(logo_path)
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)

        st.markdown("""
        <div style='margin: 0.5rem 0 1.2rem 0;'>
            <p style='font-size:1.3rem; font-weight:700; margin:0; color:#f8fafc !important;'>⚙️ Settings</p>
        </div>
        """, unsafe_allow_html=True)

        language = st.selectbox(
            "🌐 Language",
            ["Hinglish", "Tamil", "English"],
            index=0,
            key="lang_select"
        )

        grade = st.selectbox(
            "📚 Grade Level",
            ["6-8", "9-10", "11-12"],
            index=0,
            key="grade_select"
        )

        st.markdown("""
        <p style='font-size:0.88rem; color:#94a3b8 !important; margin:0.8rem 0 0.4rem 0; font-weight:600;'>🎯 Mode</p>
        """, unsafe_allow_html=True)

        mode = st.radio(
            label="Mode",
            options=["📖 Explain Concept", "🎤 Voice Input", "🧠 Quiz Me", "🗺️ Visual Map"],
            index=0,
            key="mode_select",
            label_visibility="collapsed"
        )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.85rem; color:#cbd5e1 !important; line-height:1.7;'>
            Built for <b style='color:#ffffff !important;'>Connecting Dreams Foundation</b><br>
            Round 2 · AI4Good Track<br><br>
            <span style='color:#f8fafc !important;'>VidyaVaani = Knowledge + Voice</span>
        </div>
        """, unsafe_allow_html=True)

    return language, grade, mode


def render_explanation_card(concept: str, explanation: str):
    """Render a styled explanation card in the main area."""
    formatted = explanation.replace("\n", "<br>")
    st.markdown(f"""
    <div class="vv-card vv-explain-card">
        <h4>📘 {concept}</h4>
        <p>{formatted}</p>
    </div>
    """, unsafe_allow_html=True)


def render_visual_card(visual_text: str):
    """Render a dark-themed visual concept map."""
    st.markdown(f"""
    <div class="vv-visual-card">{visual_text}</div>
    """, unsafe_allow_html=True)


def render_quiz(questions: list[dict]):
    """Render interactive quiz — all answers and scores persist in main area."""
    st.markdown("<p class='vv-section-title'>🧠 Practice Quiz</p>", unsafe_allow_html=True)

    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = {}
    if "quiz_checked" not in st.session_state:
        st.session_state["quiz_checked"] = {}

    total = len(questions)

    for i, q in enumerate(questions):
        st.markdown(f"""
        <div class="vv-card" style="margin-bottom:0.5rem;">
            <p style="font-weight:600; color:#1e293b; margin:0 0 0.8rem 0; font-size:1.02rem;">
                Q{i+1}. {q['question']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        key_ans = f"q_{i}_ans"
        saved_ans = st.session_state["quiz_answers"].get(key_ans, None)
        default_index = 0
        if saved_ans in q["options"]:
            default_index = q["options"].index(saved_ans)

        user_ans = st.radio(
            label=f"Options for Q{i+1}",
            options=q["options"],
            index=default_index,
            key=f"quiz_radio_{i}",
            label_visibility="collapsed"
        )
        st.session_state["quiz_answers"][key_ans] = user_ans

        key_checked = f"q_{i}_checked"
        checked = st.session_state["quiz_checked"].get(key_checked, False)

        if st.button(f"✅ Check Answer #{i+1}", key=f"btn_check_{i}"):
            st.session_state["quiz_checked"][key_checked] = True
            checked = True

        if checked:
            correct_letter = q["answer"].strip().upper()
            chosen_letter = user_ans[0].upper() if user_ans else ""
            if chosen_letter == correct_letter:
                st.success(f"✅ **Correct!** — {q.get('explanation', '')}")
            else:
                st.error(f"❌ **Incorrect.** Correct: **{correct_letter}** — {q.get('explanation', '')}")

        st.markdown("---")

    # Running score card
    total_checked = sum(1 for idx in range(total) if st.session_state["quiz_checked"].get(f"q_{idx}_checked", False))
    if total_checked > 0:
        correct_count = 0
        for idx, q in enumerate(questions):
            if st.session_state["quiz_checked"].get(f"q_{idx}_checked", False):
                user_ans = st.session_state["quiz_answers"].get(f"q_{idx}_ans", "")
                if user_ans and user_ans[0].upper() == q["answer"].strip().upper():
                    correct_count += 1

        st.markdown(f"""
        <div class="vv-score-card">
            <h4>🏆 Score: {correct_count} / {total_checked} Answered Correctly</h4>
            <p>Keep it up! Every question brings you closer to mastery.</p>
        </div>
        """, unsafe_allow_html=True)
