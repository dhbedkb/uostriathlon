from pathlib import Path
import re
import yaml
from PIL import Image, ImageOps

ROOT = Path(".")
CONTENT_DIR = ROOT / "_data/content"
GENERATED_DIR = ROOT / "assets/images/generated"
COMMITTEE_DIR = ROOT / "assets/images/committee/profiles"

GENERATED_DIR.mkdir(parents=True, exist_ok=True)
COMMITTEE_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}

def slugify(value):
    value = str(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "image"

def normalise_ref(ref):
    if not ref:
        return None

    ref = str(ref).strip()

    if ref.startswith("/uostriathlon/"):
        ref = ref[len("/uostriathlon/"):]

    if ref.startswith("uostriathlon/"):
        ref = ref[len("uostriathlon/"):]

    return ref.lstrip("/")

def source_path(ref):
    cleaned = normalise_ref(ref)

    if not cleaned:
        return None

    candidates = [
        ROOT / cleaned,
        ROOT / "_data/content" / cleaned,
    ]

    name = Path(cleaned).name

    candidates.extend([
        ROOT / "assets/images/source" / name,
        ROOT / "assets/images/uploads" / name,
        ROOT / "assets/images/committee/raw" / name,
        ROOT / "_data/content/assets/images/source" / name,
        ROOT / "_data/content/assets/images/uploads" / name,
        ROOT / "_data/content/assets/images/committee/raw" / name,
    ])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Last resort: case-insensitive search by filename.
    lower_name = name.lower()
    for candidate in ROOT.rglob("*"):
        try:
            if candidate.is_file() and candidate.name.lower() == lower_name:
                return candidate
        except OSError:
            pass

    return ROOT / cleaned

def ensure_supported(path):
    return path and path.exists() and path.suffix.lower() in SUPPORTED_EXTENSIONS

def crop_to_aspect(img, aspect_w, aspect_h, crop_x=50, crop_y=50, crop_zoom=100):
    img = ImageOps.exif_transpose(img)

    has_alpha = (
        img.mode in ("RGBA", "LA")
        or (img.mode == "P" and "transparency" in img.info)
    )

    img = img.convert("RGBA" if has_alpha else "RGB")
    w, h = img.size

    zoom = max(float(crop_zoom or 100) / 100.0, 1.0)
    target_ratio = aspect_w / aspect_h

    crop_w = w / zoom
    crop_h = crop_w / target_ratio

    if crop_h > h / zoom:
        crop_h = h / zoom
        crop_w = crop_h * target_ratio

    cx = w * (float(crop_x or 50) / 100.0)
    cy = h * (float(crop_y or 50) / 100.0)

    left = cx - crop_w / 2
    top = cy - crop_h / 2
    right = left + crop_w
    bottom = top + crop_h

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

    return img.crop((int(left), int(top), int(right), int(bottom)))

def save_webp(src, dest, width, height, crop_x=50, crop_y=50, crop_zoom=100):
    dest.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(src) as img:
        cropped = crop_to_aspect(
            img,
            width,
            height,
            crop_x=crop_x,
            crop_y=crop_y,
            crop_zoom=crop_zoom,
        )
        cropped = cropped.resize((width, height), Image.Resampling.LANCZOS)
        cropped.save(dest, "WEBP", quality=82, method=6)

    return "/" + str(dest).replace("\\", "/")

def process_image(ref, page_slug, name, width, height, crop_x=50, crop_y=50, crop_zoom=100):
    src = source_path(ref)

    if not ensure_supported(src):
        print(f"Skipping unsupported or missing image: {ref}")
        return None

    output = GENERATED_DIR / page_slug / (slugify(name) + ".webp")

    return save_webp(
        src,
        output,
        width,
        height,
        crop_x=crop_x,
        crop_y=crop_y,
        crop_zoom=crop_zoom,
    )

def process_committee_member(member):
    raw = member.get("image_raw")

    if not raw:
        if member.get("image_profile"):
            member["image_profile"] = ""
            return True
        return False

    src = source_path(raw)

    if not ensure_supported(src):
        print(f"Skipping unsupported or missing committee image: {raw}")
        return False

    name = f"{member.get('name', '')}-{member.get('role', '')}"
    output = COMMITTEE_DIR / (slugify(name) + ".webp")

    public_ref = save_webp(
        src,
        output,
        900,
        900,
        crop_x=member.get("crop_x", 50),
        crop_y=member.get("crop_y", 50),
        crop_zoom=member.get("crop_zoom", 100),
    )

    if member.get("image_profile") != public_ref:
        member["image_profile"] = public_ref
        return True

    return False

def process_file(yml):
    data = yaml.safe_load(yml.read_text())
    page_slug = slugify(data.get("title") or yml.stem)
    changed = False

    for s_index, section in enumerate(data.get("sections", [])):
        stype = section.get("type")

        if stype == "hero":
            raw = section.get("background_image_raw")
            if raw:
                generated = process_image(
                    raw,
                    page_slug,
                    f"hero-{section.get('id') or s_index}",
                    2000,
                    1125,
                    section.get("background_crop_x", 50),
                    section.get("background_crop_y", 50),
                    section.get("background_crop_zoom", 100),
                )
                if generated and section.get("background_image") != generated:
                    section["background_image"] = generated
                    changed = True

        elif stype == "cards":
            for i, card in enumerate(section.get("cards", [])):
                raw = card.get("image_raw")
                if raw:
                    generated = process_image(
                        raw,
                        page_slug,
                        f"card-{section.get('id') or s_index}-{i}-{card.get('title')}",
                        900,
                        900,
                        card.get("crop_x", 50),
                        card.get("crop_y", 50),
                        card.get("crop_zoom", 100),
                    )
                    if generated and card.get("image") != generated:
                        card["image"] = generated
                        changed = True

        elif stype == "gallery":
            for i, item in enumerate(section.get("images", [])):
                raw = item.get("src_raw")
                if raw:
                    generated = process_image(
                        raw,
                        page_slug,
                        f"gallery-{section.get('id') or s_index}-{i}",
                        1200,
                        1200,
                        item.get("crop_x", 50),
                        item.get("crop_y", 50),
                        item.get("crop_zoom", 100),
                    )
                    if generated and item.get("src") != generated:
                        item["src"] = generated
                        changed = True

        elif stype == "socials":
            for i, item in enumerate(section.get("items", [])):
                raw = item.get("icon_raw")
                if raw:
                    generated = process_image(
                        raw,
                        page_slug,
                        f"social-{section.get('id') or s_index}-{i}-{item.get('platform')}",
                        512,
                        512,
                        item.get("crop_x", 50),
                        item.get("crop_y", 50),
                        item.get("crop_zoom", 100),
                    )
                    if generated and item.get("icon") != generated:
                        item["icon"] = generated
                        changed = True

        elif stype == "committee":
            for member in section.get("members", []):
                if process_committee_member(member):
                    changed = True

    if changed:
        yml.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
        print(f"Updated {yml}")

for yml in CONTENT_DIR.glob("*.yml"):
    process_file(yml)
