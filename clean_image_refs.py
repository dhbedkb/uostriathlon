from pathlib import Path
import yaml

IMAGE_KEYS = {
    "image", "image_raw", "image_profile",
    "background_image", "background_image_raw",
    "src", "src_raw",
    "icon", "icon_raw",
    "logo", "thumbnail", "photo",
    "profile_image", "hero_image"
}

CROP_KEYS = {
    "crop_x", "crop_y", "crop_zoom",
    "background_crop_x", "background_crop_y",
    "background_crop_zoom", "image_position"
}

IMAGE_EXTS = (
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
    ".bmp", ".tif", ".tiff", ".ico", ".heic", ".avif"
)

def is_image_ref(value):
    if not isinstance(value, str):
        return False
    lower = value.lower()
    return (
        "/assets/images/" in lower
        or "/uostriathlon/assets/images/" in lower
        or lower.endswith(IMAGE_EXTS)
    )

def clean(node):
    changed = False
    if isinstance(node, dict):
        for key in list(node.keys()):
            value = node[key]
            if key in IMAGE_KEYS or key in CROP_KEYS or is_image_ref(value):
                del node[key]
                changed = True
            elif clean(value):
                changed = True
    elif isinstance(node, list):
        for item in node:
            if clean(item):
                changed = True
    return changed

for path in sorted(Path("_data").rglob("*.yml")):
    data = yaml.safe_load(path.read_text())
    if data is None:
        continue
    if clean(data):
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
        print("Cleaned", path)
