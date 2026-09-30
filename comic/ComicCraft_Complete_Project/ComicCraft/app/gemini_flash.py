import json
from google import genai
from app.config import GEMINI_API_KEY, GEMINI_FLASH_MODEL, PANEL_COUNT

def _client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_outline(story_prompt: str, character_name: str, setting: str,
                     tone: str, art_style: str) -> list[dict]:
    client = _client()
    prompt = f"""
Create a cohesive {PANEL_COUNT}-panel comic outline.

User story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON with this exact shape:
{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "short title",
      "scene_description": "visual scene description",
      "image_prompt": "detailed image-generation prompt"
    }}
  ]
}}

Rules:
- Exactly {PANEL_COUNT} panels.
- Keep the same main character and visual identity across all panels.
- Give each panel a clear story purpose: setup, development, complication, climax, ending.
- Image prompts must describe composition, environment, lighting, character action and the requested art style.
- Do not include markdown fences.
"""
    response = client.models.generate_content(
        model=GEMINI_FLASH_MODEL,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    data = json.loads(response.text)
    panels = data.get("panels", [])
    if len(panels) != PANEL_COUNT:
        raise ValueError(f"Gemini returned {len(panels)} panels instead of {PANEL_COUNT}.")
    return panels
