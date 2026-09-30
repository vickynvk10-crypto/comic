from pathlib import Path
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.schemas import PromptRequest
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf
from app.config import BASE_DIR

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def run_pipeline(req: PromptRequest):
    outline = generate_outline(
        req.story_prompt, req.character_name, req.setting, req.tone, req.art_style
    )
    story = generate_story(outline, req.character_name, req.tone)
    image_paths = []
    for panel in outline:
        image_prompt = (
            f"{panel['image_prompt']}. Keep character {req.character_name} "
            f"visually consistent. Setting: {req.setting}. Art style: {req.art_style}."
        )
        image_paths.append(generate_image(image_prompt, panel["panel_number"]))
    layout = build_comic_layout(outline, story, image_paths)
    pdf_url = save_pdf(layout)
    return layout, pdf_url

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        req = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout, pdf_url = run_pipeline(req)
        return templates.TemplateResponse(
            request,
            "comic_preview.html",
            {"request": request, "layout": layout, "pdf_url": pdf_url},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request,
            "error.html",
            {"request": request, "error": str(exc)},
            status_code=500,
        )

@router.post("/generate-comic/json")
async def generate_json(req: PromptRequest):
    try:
        layout, pdf_url = run_pipeline(req)
        return JSONResponse({"panels": layout, "pdf_url": pdf_url})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    try:
        path = generate_image(prompt, 0)
        return {"image_url": path.replace(str(BASE_DIR), "").replace("\\", "/")}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_url: str = ""):
    return templates.TemplateResponse(
        request,
        "export_success.html",
        {"request": request, "pdf_url": pdf_url},
    )
