"""
Reads every content file, finds any *_raw image references, applies the
crop/zoom the editor recorded, resizes to the size the section needs, and
saves a compressed WebP into assets/images/generated (or
assets/images/committee/profiles for committee photos).

This keeps the raw, full-size upload in the repo for future re-cropping,
while the site itself only ever loads the small, compressed WebP.

Compression is tuned per use rather than one flat setting for every image:
a large hero photo is on screen for a second behind text and can take a
lower quality; a small icon or logo is looked at directly and gets a
higher one. See docs/image-pipeline.md for the reasoning and the full
table of sizes/qualities.

Run automatically by .github/workflows/deploy.yml before every build.
Can also be run locally:

  python3 scripts/optimise_site_images.py
"""

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

# WebP quality by use. Large, briefly-seen backgrounds tolerate more
# compression than small images people actually look closely at.
QUALITY_HERO = 76
QUALITY_PHOTO = 80
QUALITY_ICON = 88
QUALITY_LOGO = 92


def slugify(value):
    value = re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")
    return value or "image"


def normalise_ref(ref):
    ref = str(ref or "").strip()
    for prefix in ("/uostriathlon/", "uostriathlon/"):
        if ref.startswith(prefix):
            ref = ref[len(prefix):]
    return ref.lstrip("/")


def source_path(ref):
    cleaned = normalise_ref(ref)
    if not cleaned:
        return None

    name = Path(cleaned).name
    candidates = [
        ROOT / cleaned,
        ROOT / "assets/images/source" / name,
        ROOT / "assets/images/uploads" / name,
        ROOT / "assets/images/committee/raw" / name,
        ROOT / "assets/images/brand" / name,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    lower_name = name.lower()
    for candidate in ROOT.rglob("*"):
        try:
            if candidate.is_file() and candidate.name.lower() == lower_name:
                return candidate
        except OSError:
            pass

    return None


def supported(path):
    return bool(path) and path.exists() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def crop_to_aspect(img, aspect_w, aspect_h, crop_x=50, crop_y=50, crop_zoom=100):
    img = ImageOps.exif_transpose(img)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
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

    left = max(0, cx - crop_w / 2)
    top = max(0, cy - crop_h / 2)
    right = min(w, left + crop_w)
    bottom = min(h, top + crop_h)
    left = max(0, right - crop_w)
    top = max(0, bottom - crop_h)

    return img.crop((int(left), int(top), int(right), int(bottom)))


def save_webp(src, dest, width, height, crop_x=50, crop_y=50, crop_zoom=100, quality=QUALITY_PHOTO):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        cropped = crop_to_aspect(img, width, height, crop_x, crop_y, crop_zoom)
        cropped = cropped.resize((width, height), Image.Resampling.LANCZOS)
        # method=6 is WebP's slowest/smallest compression effort setting.
        # This only runs on publish, so it's worth spending the extra CPU
        # time for a smaller file. No EXIF/ICC data is carried over, since
        # `cropped` is a fresh image built from pixel data only.
        cropped.save(dest, "WEBP", quality=quality, method=6)
    return "/" + str(dest).replace("\\", "/")


def process_image(ref, page_slug, name, width, height, crop_x=50, crop_y=50, crop_zoom=100, quality=QUALITY_PHOTO):
    src = source_path(ref)
    if not supported(src):
        print(f"Skipping unsupported or missing image: {ref}")
        return None
    dest = GENERATED_DIR / page_slug / (slugify(name) + ".webp")
    return save_webp(src, dest, width, height, crop_x, crop_y, crop_zoom, quality)


def process_committee_member(member):
    raw = member.get("image_raw")
    if not raw:
        return False

    src = source_path(raw)
    if not supported(src):
        print(f"Skipping unsupported or missing committee image: {raw}")
        return False

    name = f"{member.get('name', '')}-{member.get('role', '')}"
    dest = COMMITTEE_DIR / (slugify(name) + ".webp")
    public_ref = save_webp(
        src, dest, 900, 900,
        member.get("crop_x", 50), member.get("crop_y", 50), member.get("crop_zoom", 100),
        quality=QUALITY_PHOTO,
    )

    if member.get("image_profile") != public_ref:
        member["image_profile"] = public_ref
        return True
    return False


def process_file(yml_path):
    data = yaml.safe_load(yml_path.read_text())
    page_slug = slugify(data.get("title") or yml_path.stem)
    changed = False

    for s_index, section in enumerate(data.get("sections", [])):
        stype = section.get("type")

        if stype == "hero" and section.get("background_image_raw"):
            generated = process_image(
                section["background_image_raw"], page_slug, f"hero-{section.get('id') or s_index}",
                2000, 1125,
                section.get("background_crop_x", 50), section.get("background_crop_y", 50), section.get("background_crop_zoom", 100),
                quality=QUALITY_HERO,
            )
            if generated and section.get("background_image") != generated:
                section["background_image"] = generated
                changed = True

        elif stype == "cards":
            for i, card in enumerate(section.get("cards", [])):
                if not card.get("image_raw"):
                    continue
                generated = process_image(
                    card["image_raw"], page_slug, f"card-{section.get('id') or s_index}-{i}-{card.get('title')}",
                    900, 900,
                    card.get("crop_x", 50), card.get("crop_y", 50), card.get("crop_zoom", 100),
                    quality=QUALITY_PHOTO,
                )
                if generated and card.get("image") != generated:
                    card["image"] = generated
                    changed = True

        elif stype == "gallery":
            for i, item in enumerate(section.get("images", [])):
                if not item.get("src_raw"):
                    continue
                generated = process_image(
                    item["src_raw"], page_slug, f"gallery-{section.get('id') or s_index}-{i}",
                    1200, 1200,
                    item.get("crop_x", 50), item.get("crop_y", 50), item.get("crop_zoom", 100),
                    quality=QUALITY_PHOTO,
                )
                if generated and item.get("src") != generated:
                    item["src"] = generated
                    changed = True

        elif stype == "socials":
            for i, item in enumerate(section.get("items", [])):
                if not item.get("icon_raw"):
                    continue
                generated = process_image(
                    item["icon_raw"], page_slug, f"social-{section.get('id') or s_index}-{i}-{item.get('platform')}",
                    512, 512,
                    item.get("crop_x", 50), item.get("crop_y", 50), item.get("crop_zoom", 100),
                    quality=QUALITY_ICON,
                )
                if generated and item.get("icon") != generated:
                    item["icon"] = generated
                    changed = True

        elif stype == "committee":
            for member in section.get("members", []):
                if process_committee_member(member):
                    changed = True

    if changed:
        yml_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
        print(f"Updated {yml_path}")


def main():
    for yml_path in CONTENT_DIR.glob("*.yml"):
        process_file(yml_path)

    # Also optimise the brand logo, if one has been uploaded.
    settings_path = ROOT / "_data/settings.yml"
    if settings_path.exists():
        settings = yaml.safe_load(settings_path.read_text()) or {}
        logo_raw = (settings.get("brand") or {}).get("logo")
        if logo_raw and not str(logo_raw).startswith("/assets/images/generated"):
            src = source_path(logo_raw)
            if supported(src):
                dest = GENERATED_DIR / "brand" / "logo.webp"
                generated = save_webp(
                    src, dest, 240, 240,
                    settings["brand"].get("logo_crop_x", 50),
                    settings["brand"].get("logo_crop_y", 50),
                    settings["brand"].get("logo_crop_zoom", 100),
                    quality=QUALITY_LOGO,
                )
                settings["brand"]["logo"] = generated
                settings_path.write_text(yaml.safe_dump(settings, sort_keys=False, allow_unicode=True))
                print("Updated _data/settings.yml (logo)")


if __name__ == "__main__":
    main()
