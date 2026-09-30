# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 web application based on the supplied project document. It creates a five-panel comic from a user prompt, generates narration/dialogue, generates panel artwork, previews the result, and exports a PDF.

## Architecture

- Frontend: HTML + CSS + Jinja2
- Backend: FastAPI
- Story outline: Gemini Flash
- Story expansion: Gemini model configured as `GEMINI_PRO_MODEL`
- Images: Gemini image generation by default, with optional local Diffusers/Stable Diffusion
- PDF: FPDF2

## Important model note

The original project document specifies older `gemini-1.5-flash`, `gemini-1.5-pro`, and `runwayml/stable-diffusion-v1-5`. This implementation keeps the same roles but makes model IDs configurable through `.env`, so you can use currently available Gemini models without changing application code.

## Windows setup

1. Install Python 3.11.
2. Open this folder in VS Code.
3. Open Terminal.
4. Create a virtual environment:

   `python -m venv .venv`

5. Activate it:

   `.venv\Scripts\activate`

6. Install dependencies:

   `python -m pip install --upgrade pip`

   `pip install -r requirements.txt`

7. Copy `.env.example` to `.env`.
8. Put your Gemini API key into `.env`.
9. Start:

   `uvicorn app.main:app --reload`

10. Open:

   http://127.0.0.1:8000

   API docs:

   http://127.0.0.1:8000/docs

## Fast test without image AI

Set:

`IMAGE_PROVIDER=placeholder`

The story still uses Gemini, while panel images are generated as local test placeholders.

## Gemini image mode

Set:

`IMAGE_PROVIDER=gemini`

This is the default. It uses the configured Gemini image model.

## Stable Diffusion mode

The project document calls for Hugging Face Diffusers + Stable Diffusion. For local image generation, install a compatible PyTorch build for your machine, then:

`pip install diffusers transformers accelerate safetensors`

Set:

`IMAGE_PROVIDER=diffusers`

A local GPU is strongly recommended for practical generation speed. The model is downloaded and cached on first use.

## API example

POST `/generate-comic/json`:

```json
{
  "story_prompt": "A brave fox explores an enchanted forest.",
  "character_name": "Fia",
  "setting": "enchanted forest",
  "tone": "funny",
  "art_style": "comic book"
}
```

## Project structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── config.py
│   ├── schemas.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   ├── export_success.html
│   └── error.html
├── static/
│   ├── css/style.css
│   ├── panels/
│   └── exports/
├── requirements.txt
├── .env.example
└── README.md
```

## Troubleshooting

- `GEMINI_API_KEY is not configured`: check `.env` and restart Uvicorn.
- Model not found: change the model variables in `.env` to a model available to your API project.
- Image generation fails: temporarily set `IMAGE_PROVIDER=placeholder` to verify the rest of the application.
- Diffusers/PyTorch installation errors: install the PyTorch build appropriate for your OS and hardware before installing the optional Diffusers packages.
- PDF contains no panel image: check that image generation completed and that `static/panels` contains PNG files.

## Testing checklist

1. Home page opens.
2. Submit a story prompt.
3. Five panels are returned.
4. Each panel has title, scene description, image and story text.
5. PDF link opens/downloads.
6. `/docs` exposes API documentation.
