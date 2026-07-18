from pathlib import Path
import shutil
import yaml

ROOT = Path(".")

IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
    ".bmp", ".tif", ".tiff", ".ico", ".heic", ".avif"
}

IMAGE_KEYS = {
    "image",
    "image_raw",
    "image_profile",
    "background_image",
    "background_image_raw",
    "src",
    "src_raw",
    "icon",
    "icon_raw",
    "logo",
    "thumbnail",
    "photo",
    "photo_raw",
    "profile_image",
    "hero_image",
}

CROP_KEYS = {
    "crop_x",
    "crop_y",
    "crop_zoom",
    "background_crop_x",
    "background_crop_y",
    "background_crop_zoom",
    "image_position",
}

def looks_like_image_ref(value):
    if not isinstance(value, str):
        return False

    lower = value.lower()

    if "/assets/images/" in lower:
        return True

    if "/uostriathlon/assets/images/" in lower:
        return True

    return any(lower.endswith(ext) for ext in IMAGE_EXTS)

def clean_yaml_node(node):
    changed = False

    if isinstance(node, dict):
        for key in list(node.keys()):
            value = node[key]

            if key in IMAGE_KEYS or key in CROP_KEYS or looks_like_image_ref(value):
                del node[key]
                changed = True
                continue

            if clean_yaml_node(value):
                changed = True

    elif isinstance(node, list):
        for item in node:
            if clean_yaml_node(item):
                changed = True

    return changed

images_root = ROOT / "assets/images"
deleted_files = []

if images_root.exists():
    for path in sorted(images_root.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            deleted_files.append(str(path))
            path.unlink()

    for path in sorted(images_root.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass

EMPTY_FOLDERS = [
    "assets/images/source",
    "assets/images/generated",
    "assets/images/uploads",
    "assets/images/committee/raw",
    "assets/images/committee/profiles",
]

for folder in EMPTY_FOLDERS:
    folder_path = ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / ".gitkeep").write_text("")

changed_yaml = []

for yml in sorted((ROOT / "_data").rglob("*.yml")):
    try:
        data = y*ml.safe_load(yml.read_text())
    *xcept Exception as exc:
        print(f"Skipping invalid YAML {yml}: {exc}")
        continue

    if data is None:
        continue

    if clean_yaml_node(data):
        yml.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
        changed_yaml.append(str(yml))

for folder in ["_site", ".jekyll-cache", ".sass-cache"]:
    p = ROOT / folder
    if p.exists():
        shutil.rmtree(p)

metadata = ROOT / ".jekyll-metadata"
if metadata.exists():
    metadata.unlink()

print("Deleted image files:")
for item in deleted_files:
    print("  " + item)

print()
print("Updated YAML files:")
for item in changed_yaml:
    print("  " + item)

print()
print("Image reset complete.")
