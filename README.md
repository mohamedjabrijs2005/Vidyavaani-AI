# 🎓 VidyaVaani AI — Voice-Enabled Teaching Assistant

> Round 2 Assignment Submission | Connecting Dreams Foundation – AI4Good Track

---

## 📌 Problem Statement

Government school students in India often struggle with complex concepts due to language barriers and lack of personalized attention. **VidyaVaani AI** bridges this gap by providing:

- Voice-based interaction (no typing required)
- Explanations in **Tamil**, **Hinglish**, and **English**
- Grade-adaptive simplification (6–8, 9–10, 11–12)
- AI-generated quizzes for self-assessment
- Smartboard-ready visual concept maps

---

## 🚀 Live Demo

🔗 https://vidyavaani.streamlit.app/

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📖 Concept Explainer | Type any topic → get a clear, grade-appropriate explanation |
| 🎤 Voice Input | Speak your question → AI answers in your language |
| 🧠 Quiz Generator | Auto-generated MCQs with instant feedback |
| 🗺️ Visual Map | ASCII/emoji concept diagram for smartboard display |
| 🔊 Text-to-Speech | Spoken answers in Tamil, Hindi, or English |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI / LLM | Google Gemini 1.5 Flash |
| Speech-to-Text | Google Web Speech API (SpeechRecognition) |
| Text-to-Speech | gTTS (Google Text-to-Speech) |
| Audio Recording | audio-recorder-streamlit |
| Deployment | Streamlit Cloud |

---

## 🧠 Prompt Design

All prompts are carefully engineered for:

1. **Language instruction** — enforces Tamil / Hinglish / English output
2. **Grade calibration** — adjusts vocabulary and analogy complexity
3. **Structured output** — quiz prompts return strict JSON for parsing
4. **Empathy framing** — AI is always a "friendly teacher", not a chatbot

Example prompt pattern:
```
You are a friendly AI teacher for Indian government school students.
[LANGUAGE INSTRUCTION]
[GRADE INSTRUCTION]
Explain: {concept} in 4–6 sentences with one real-life example.
Add a 💡 Did you know? fact.
```

---

## 🌐 Localization Approach

| Language | Code | Use Case |
|---|---|---|
| Tamil | `ta` | Tamil Nadu government schools |
| Hinglish | `hi` | Hindi belt states (UP, Bihar, MP, Rajasthan) |
| English | `en` | Urban schools or English-medium sections |

Gemini 1.5 Flash natively supports multilingual generation. The language instruction is injected into every prompt to enforce consistent output language.

---

## 📂 Folder Structure

```
ai-teaching-assistant/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md
├── utils/
│   ├── ai_engine.py        # Gemini API calls (explain, quiz, visual)
│   └── voice_engine.py     # TTS and STT functions
└── components/
    └── ui_components.py    # Reusable Streamlit UI blocks
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-teaching-assistant.git
cd ai-teaching-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Groq API Key
- Go to [https://console.groq.com/keys]
- Sign in → **Get API Key** → **Create API key**

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Enter your API key in the sidebar and start using!

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file**: `app.py`
5. Click **Deploy**

---

## 📊 Evaluation Criteria Addressed

| Criteria | Weightage | How We Address It |
|---|---|---|
| Technical Implementation | 40% | Gemini API + STT + TTS + structured quiz JSON |
| Empathy / UX Design | 30% | Clean UI, grade-adaptive language, voice-first design |
| AI / Prompt Design | 30% | Structured prompts with language + grade injection |

---

## 🎬 Demo Video Script (3 min)

1. **(0:00–0:30)** — Introduce the problem: language barrier + concept difficulty in government schools
2. **(0:30–1:15)** — Demo: Type "Photosynthesis" → Hinglish explanation → play audio
3. **(1:15–1:50)** — Demo: Voice input mode → speak question → get spoken answer in Tamil
4. **(1:50–2:30)** — Demo: Quiz mode → generate 3 questions → check answers
5. **(2:30–3:00)** — Demo: Visual Map mode → concept diagram + audio narration

---

## 👨‍💻 Developer

**Mohamed Jabri J S **
B.E. Computer Science & Engineering (Interner of Things)
Sri Sairam Institute of Technology, Chennai

---

*Built with ❤️ for Indian government school students*
