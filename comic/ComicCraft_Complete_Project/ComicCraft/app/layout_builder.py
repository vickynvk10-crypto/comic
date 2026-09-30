def build_comic_layout(outline: list[dict], story: list[dict], image_paths: list[str]) -> list[dict]:
    story_by_number = {item.get("panel_number"): item for item in story}
    layout = []
    for index, panel in enumerate(outline):
        number = panel["panel_number"]
        extra = story_by_number.get(number, {})
        layout.append({
            "panel_number": number,
            "title": panel.get("title", f"Panel {number}"),
            "image_path": image_paths[index],
            "scene_description": panel.get("scene_description", ""),
            "image_prompt": panel.get("image_prompt", ""),
            "caption": extra.get("caption", ""),
            "narration": extra.get("narration", ""),
            "dialogue": extra.get("dialogue", []),
        })
    return layout
