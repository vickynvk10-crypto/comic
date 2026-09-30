from pathlib import Path
import base64
import re
from PIL import Image, ImageDraw, ImageFont
from app.config import (
    BASE_DIR, GEMINI_API_KEY, GEMINI_IMAGE_MODEL,
    IMAGE_PROVIDER, SD_MODEL_ID, SD_STEPS, HF_API_KEY
)

PIPELINE = None

def _safe_name(text: str, fallback: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return (name[:60] or fallback)

def _placeholder(prompt: str, panel_number: int, output: Path) -> str:
    # Always-working fallback: creates a clean illustrated placeholder.
    img = Image.new("RGB", (1024, 768), "white")
    draw = ImageDraw.Draw(img)
    title = f"ComicCraft — Panel {panel_number}"
    draw.rectangle((25, 25, 999, 743), outline="black", width=8)
    draw.text((55, 60), title, fill="black")
    lines = [prompt[i:i+58] for i in range(0, min(len(prompt), 350), 58)]
    y = 150
    for line in lines:
        draw.text((55, y), line, fill="black")
        y += 38
    draw.ellipse((650, 220, 850, 420), outline="black", width=6)
    draw.text((680, 300), "AI\nPANEL", fill="black", align="center")
    img.save(output, format="PNG")
    return str(output)

def _gemini_image(prompt: str, output: Path) -> str:
    from google import genai
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    client = genai.Client(api_key=GEMINI_API_KEY)
    interaction = client.interactions.create(
        model=GEMINI_IMAGE_MODEL,
        input=prompt,
    )
    image_data = getattr(getattr(interaction, "output_image", None), "data", None)
    if not image_data:
        # Some SDK responses expose image blocks in steps.
        for step in getattr(interaction, "steps", []) or []:
            for block in getattr(step, "content", []) or []:
                if getattr(block, "type", "") == "image":
                    image_data = getattr(block, "data", None)
                    if image_data:
                        break
            if image_data:
                break
    if not image_data:
        raise RuntimeError("Gemini image model did not return image data.")
    output.write_bytes(base64.b64decode(image_data))
    return str(output)

def _diffusers_image(prompt: str, output: Path) -> str:
    global PIPELINE
    import torch
    from diffusers import StableDiffusionPipeline
    if PIPELINE is None:
        kwargs = {"use_safetensors": True}
        if HF_API_KEY:
            kwargs["token"] = HF_API_KEY
        PIPELINE = StableDiffusionPipeline.from_pretrained(SD_MODEL_ID, **kwargs)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        PIPELINE = PIPELINE.to(device)
    image = PIPELINE(
        prompt,
        num_inference_steps=SD_STEPS,
        height=768,
        width=1024,
    ).images[0]
    image.save(output)
    return str(output)

def generate_image(image_prompt: str, panel_number: int) -> str:
    output_dir = BASE_DIR / "static" / "panels"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"panel_{panel_number}_{_safe_name(image_prompt, 'scene')}.png"

    try:
        if IMAGE_PROVIDER == "gemini":
            return _gemini_image(image_prompt, output)
        if IMAGE_PROVIDER == "diffusers":
            return _diffusers_image(image_prompt, output)
    except Exception as exc:
        print(f"[image-generator] provider failed: {exc}")

    return _placeholder(image_prompt, panel_number, output)
