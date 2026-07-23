"""
Reads every content file, finds any raw image references (the hero
background, or an image block's src_raw inside a tile's `blocks` list),
applies the crop/zoom the editor recorded, resizes to the size that
kind of image needs, and saves a compressed WebP into
assets/images/generated (or assets/images/committee/profiles for
committee-preset tile images, kept separate for backwards compatibility
with existing uploads).

Because every non-hero image on the site now lives at the same place in
the data shape — a block of type "image" somewhere in
`sections[].tiles[].blocks` — this script doesn't need one branch per
section type, or even one branch per tile preset. A brand-new preset
never requires a change here: if a tile has an image block, it's
already handled, and a tile can have as many image blocks as it likes
(each is found and processed independently, keyed by its position in
the list).

Compression is tuned by *shape*, not by what the image is a photo of: a
square tile photo (card, gallery, committee, sponsor…) gets one
treatment, a round tile image (icon-style, e.g. social platform logos)
gets another, tuned for a small sharp-edged graphic. See
docs/image-pipeline.md for the reasoning.

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
QUALITY_TILE = 80
QUALITY_ICON = 88
QUALITY_LOGO = 92

TILE_SIZE = (1000, 1000)
ICON_SIZE = (512, 512)
HERO_SIZE = (2000, 1125)
LOGO_SIZE = (240, 240)


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


def save_webp(src, dest, size, crop_x=50, crop_y=50, crop_zoom=100, quality=QUALITY_TILE):
    dest.parent.mkdir(parents=True, exist_ok=True)
    width, height = size
    with Image.open(src) as img:
        cropped = crop_to_aspect(img, width, height, crop_x, crop_y, crop_zoom)
        cropped = cropped.resize((width, height), Image.Resampling.LANCZOS)
        # method=6 is WebP's slowest/smallest compression effort setting.
        # This only runs on publish, so it's worth spending the extra CPU
        # time for a smaller file. No EXIF/ICC data is carried over, since
        # `cropped` is a fresh image built from pixel data only.
        cropped.save(dest, "WEBP", quality=quality, method=6)
    return "/" + str(dest).replace("\\", "/")


def process_hero(section, page_slug, s_index, changed_flag):
    raw = section.get("background_image_raw")
    if not raw:
        return changed_flag
    src = source_path(raw)
    if not supported(src):
        print(f"Skipping unsupported or missing hero image: {raw}")
        return changed_flag
    dest = GENERATED_DIR / page_slug / f"hero-{section.get('id') or s_index}.webp"
    generated = save_webp(
        src, dest, HERO_SIZE,
        section.get("background_crop_x", 50), section.get("background_crop_y", 50),
        section.get("background_crop_zoom", 100), quality=QUALITY_HERO,
    )
    if section.get("background_image") != generated:
        section["background_image"] = generated
        return True
    return changed_flag


def tile_text(tile, block_type):
    """First block of a given type's `text` field, for naming generated files."""
    for block in tile.get("blocks", []):
        if block.get("type") == block_type and block.get("text"):
            return block["text"]
    return ""


def process_tile_images(tile, page_slug, section, s_index, t_index):
    """A tile's blocks list can contain any number of image blocks (in
    practice usually zero or one). Each is looked up and compressed the
    same way, keyed by its position in the list so multiple images on
    one tile don't collide."""
    changed = False

    for b_index, block in enumerate(tile.get("blocks", [])):
        if block.get("type") != "image" or not block.get("src_raw"):
            continue

        src = source_path(block["src_raw"])
        if not supported(src):
            print(f"Skipping unsupported or missing tile image: {block['src_raw']}")
            continue

        is_round = block.get("shape") == "round"
        name_bits = f"{section.get('id') or s_index}-{t_index}-{b_index}-{tile_text(tile, 'title') or tile_text(tile, 'eyebrow')}"
        slug = slugify(name_bits)

        # Committee-preset photos keep their historical output folder so
        # existing generated assets and any external references don't move.
        if tile.get("preset") == "committee":
            dest = COMMITTEE_DIR / (slugify(f"{tile_text(tile, 'title')}-{tile_text(tile, 'subtitle')}") + ".webp")
        else:
            dest = GENERATED_DIR / page_slug / (slug + ".webp")

        size = ICON_SIZE if is_round else TILE_SIZE
        quality = QUALITY_ICON if is_round else QUALITY_TILE

        generated = save_webp(
            src, dest, size,
            block.get("crop_x", 50), block.get("crop_y", 50), block.get("crop_zoom", 100),
            quality=quality,
        )
        if block.get("src") != generated:
            block["src"] = generated
            changed = True

    return changed


def process_file(yml_path):
    data = yaml.safe_load(yml_path.read_text())
    page_slug = slugify(data.get("title") or yml_path.stem)
    changed = False

    for s_index, section in enumerate(data.get("sections", [])):
        stype = section.get("type")

        if stype == "hero":
            changed = process_hero(section, page_slug, s_index, changed) or changed

        elif stype == "tile-grid":
            for t_index, tile in enumerate(section.get("tiles", [])):
                if process_tile_images(tile, page_slug, section, s_index, t_index):
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
                    src, dest, LOGO_SIZE,
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
