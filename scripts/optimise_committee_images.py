from pathlib import Path
import re
import yaml
from PIL import Image, ImageOps

ROOT = Path(".")
committee_file = ROOT / "_data/content/committee.yml"
output_dir = ROOT / "assets/images/committee/profiles"
output_dir.mkdir(parents=True, exist_ok=True)

def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "committee-member"

def normalise_ref(path):
    if not path:
        return None
    return str(path).lstrip("/")

def crop_square(img, crop_x=50, crop_y=50, crop_zoom=100):
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size

    zoom = max(float(crop_zoom or 100) / 100.0, 1.0)
    side = min(w, h) / zoom

    cx = w * (float(crop_x or 50) / 100.0)
    cy = h * (float(crop_y or 50) / 100.0)

    left = cx - side / 2
    top = cy - side / 2
    right = left + side
    bottom = top + side

    if left < 0:
        right -= left
        left = 0
    if top < 0:
        bottom -= top
        top = 0
    if right > w:
        left -= right - w
        right = w
    if bottom > h:
        top -= bottom - h
        bottom = h

    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    cropped = img.crop((int(left), int(top), int(right), int(bottom)))
    cropped = cropped.resize((900, 900), Image.Resampling.LANCZOS)
    return cropped

if not committee_file.exists():
    raise SystemExit("No committee.yml found")

data = yaml.safe_load(committee_file.read_text())
changed = False

for section in data.get("sections", []):
    if section.get("type") != "committee":
        continue

    for member in section.get("members", []):
        image_ref = member.get("image")
        if not image_ref:
            continue

        image_path = ROOT / normalise_ref(image_ref)
        if not image_path.exists():
            print(f"Skipping missing image: {image_ref}")
            continue

        if "/assets/images/committee/profiles/" in image_ref:
            continue

        name = member.get("name") or image_path.stem
        role = member.get("role") or ""
        filename = slugify(f"{name}-{role}") + ".webp"
        output_path = output_dir / filename
        public_ref = "/" + str(output_path).replace("\\", "/")

        try:
            with Image.open(image_path) as img:
                processed = crop_square(
                    img,
                    member.get("crop_x", 50),
                    member.get("crop_y", 50),
                    member.get("crop_zoom", 100),
                )
                processed.save(output_path, "WEBP", quality=82, method=6)
        except Exception as exc:
            print(f"Could not process {image_ref}: {exc}")
            continue

        member["image"] = public_ref
        member["crop_x"] = 50
        member["crop_y"] = 50
        member["crop_zoom"] = 100
        changed = True

if changed:
    committee_file.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    print("Updated committee.yml with optimised WebP references")
else:
    print("No committee.yml reference changes needed")
