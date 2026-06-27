from groq import Groq
import time

MODEL_NAME = "llama-3.3-70b-versatile"
client = None

def configure_groq(api_key: str):
    global client
    client = Groq(api_key=api_key)


def _safe_generate(prompt: str, retries: int = 2) -> str:
    """Call Groq with automatic retry on quota/rate-limit errors."""
    global client
    if not client:
        raise ValueError("Groq client is not configured. Call configure_groq first.")
        
    for attempt in range(retries + 1):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=MODEL_NAME,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            err = str(e)
            if "429" in err or "RateLimit" in err or "quota" in err.lower() or "ResourceExhausted" in err:
                if attempt < retries:
                    wait = 5 * (attempt + 1)   # Groq limits are typically shorter, wait 5s then 10s
                    time.sleep(wait)
                    continue
                raise QuotaError(
                    "⚠️ **Quota limit reached.** Your Groq API key has hit its rate limit or quota.\n\n"
                    "**Quick fixes:**\n"
                    "- Wait a minute and try again\n"
                    "- Check your usage dashboard on [Groq Console](https://console.groq.com)"
                )
            raise


class QuotaError(Exception):
    """Raised when Groq API quota or rate limit is exhausted."""
    pass


def explain_concept(concept: str, language: str, grade: str) -> str:
    """
    Explain a concept in simple terms based on selected language and grade.
    language: 'Tamil' | 'Hinglish' | 'English'
    grade:    '6-8' | '9-10' | '11-12'
    """
    lang_instruction = {
        "Tamil":    "Respond ONLY in Tamil language using simple words a school student would understand.",
        "Hinglish": "Respond in Hinglish (Hindi + English mix) like a friendly teacher speaking to students.",
        "English":  "Respond in simple English suitable for school students.",
    }.get(language, "Respond in simple English.")

    grade_instruction = {
        "6-8":  "The student is in Grade 6–8. Use very basic analogies and everyday examples.",
        "9-10": "The student is in Grade 9–10. You can introduce slightly technical terms but explain them.",
        "11-12":"The student is in Grade 11–12. You can use proper subject terminology.",
    }.get(grade, "")

    prompt = f"""
You are a friendly AI teacher for Indian government school students.
{lang_instruction}
{grade_instruction}

Explain this concept clearly in 4–6 sentences with one relatable real-life example:
Concept: {concept}

After the explanation, add a single "💡 Did you know?" fun fact related to this concept.
"""
    return _safe_generate(prompt)


def generate_quiz(concept: str, language: str, num_questions: int = 3) -> list[dict]:
    """
    Generate MCQ quiz questions. Returns list of dicts:
    { question, options: [A,B,C,D], answer, explanation }
    """
    lang_instruction = {
        "Tamil":    "Write ALL text (questions, options, explanations) in Tamil.",
        "Hinglish": "Write ALL text in Hinglish (Hindi+English mix).",
        "English":  "Write ALL text in English.",
    }.get(language, "Write in English.")

    prompt = f"""
You are a quiz generator for Indian school students.
{lang_instruction}

Generate exactly {num_questions} multiple-choice questions about: "{concept}"

Return ONLY a valid JSON array. No markdown, no explanation outside the JSON. Do not wrap it in a markdown json block.
Format:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A",
    "explanation": "..."
  }}
]
"""
    text = _safe_generate(prompt)
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    import json
    return json.loads(text.strip())


def get_visual_description(concept: str) -> str:
    """
    Returns a simple visual description / diagram in markdown table format
    suitable for displaying as a structured concept table.
    """
    prompt = f"""
Create a highly structured, elegant Markdown table representing the visual concept map/diagram flow for:
"{concept}"

The table should outline the stages, processes, or parts of the concept with clear descriptions and relevant emojis.
Structure columns as follows:
| Stage/Part | Process/Description | Visual Icon |

Include 4 to 8 clear steps/parts. Return ONLY the markdown table. No explanation text outside.
"""
    return _safe_generate(prompt)
