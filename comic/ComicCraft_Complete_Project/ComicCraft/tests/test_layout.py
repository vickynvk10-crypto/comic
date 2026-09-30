from app.layout_builder import build_comic_layout

def test_build_layout():
    outline = [
        {"panel_number": 1, "title": "Start", "scene_description": "A", "image_prompt": "B"},
        {"panel_number": 2, "title": "Middle", "scene_description": "C", "image_prompt": "D"},
    ]
    story = [
        {"panel_number": 1, "caption": "X", "narration": "Y", "dialogue": ["Fia: Hi"]},
    ]
    layout = build_comic_layout(outline, story, ["/static/panels/1.png", "/static/panels/2.png"])
    assert len(layout) == 2
    assert layout[0]["caption"] == "X"
    assert layout[1]["caption"] == ""
