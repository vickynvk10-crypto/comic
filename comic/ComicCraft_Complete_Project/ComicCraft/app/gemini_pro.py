import json
from google import genai
from app.config import GEMINI_API_KEY, GEMINI_PRO_MODEL

def _client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_story(outline: list[dict], character_name: str, tone: str) -> list[dict]:
    client = _client()
    compact_outline = json.dumps(outline, ensure_ascii=False)
    prompt = f"""
Expand this comic outline into polished panel-by-panel comic writing.

Character: {character_name}
Tone: {tone}
Outline:
{compact_outline}

Return ONLY valid JSON:
{{
  "panels": [
    {{
      "panel_number": 1,
      "caption": "short ambient caption",
      "narration": "1-3 sentence narration",
      "dialogue": ["Character: dialogue", "Character: dialogue"]
    }}
  ]
}}

Rules:
- Exactly one result for every outline panel.
- Preserve panel numbers and story continuity.
- Dialogue should be concise and comic-friendly.
- Keep language suitable for a general audience.
"""
    response = client.models.generate_content(
    model=GEMINI_PRO_MODEL,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    data = json.loads(response.text)
    return data.get("panels", [])
