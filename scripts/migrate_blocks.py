"""
One-off migration: rewrites _data/content/*.yml tiles from the
Phase-2 shape (named fields: eyebrow/title/subtitle/image/body/qa/meta/
email/buttons, plus a section-level `preset` and `behavior.expand`)
into the v3 block-list shape (a single ordered `blocks` list per tile,
with an `expand` marker block instead of a visibility field, and
`preset` moved from the section onto each individual tile).

Order used when building each tile's blocks list: eyebrow, title,
subtitle, image (or embed), [expand — inserted here if the section's
old behavior.expand was hover/click], body, one `note` block per old
Q&A pair, one `note` block per old meta row, email, buttons. This
matches the render order the site has used since Phase 2, so migrated
content looks identical once rebuilt.

Section-level `preset` maps to a tile-level `preset` on every tile in
that section: committee -> committee, faq -> faq, sponsors -> sponsor,
events -> event, anything else (cards/gallery/stats/timeline/cta/
embed/socials/custom) -> custom. `behavior` is dropped from the
section entirely once used to decide the expand-block placement.

Safe to re-run: sections whose tiles already have a `blocks` list are
left untouched.

Usage:
  python3 scripts/migrate_blocks.py            # writes in place
  python3 scripts/migrate_blocks.py --check    # prints a diff, doesn't write
"""

from pathlib import Path
import argparse
import difflib
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "_data/content"

PRESET_MAP = {
    "committee": "committee",
    "faq": "faq",
    "sponsors": "sponsor",
    "events": "event",
}


def image_block(image):
    if not image:
        return None
    block = {"type": "image"}
    for key in ("src_raw", "src", "crop_x", "crop_y", "crop_zoom", "shape", "alt"):
        if image.get(key) not in (None, ""):
            block[key] = image[key]
    return block


def embed_block(embed):
    if not embed:
        return None
    block = {"type": "embed"}
    for key in ("provider", "embed_html", "width", "url", "button_label"):
        if embed.get(key) not in (None, ""):
            block[key] = embed[key]
    return block


def migrate_tile(tile, section_expand, tile_preset):
    if "blocks" in tile:
        return tile  # already migrated

    blocks = []

    if tile.get("eyebrow"):
        blocks.append({"type": "eyebrow", "text": tile["eyebrow"]})
    if tile.get("title"):
        blocks.append({"type": "title", "text": tile["title"]})
    if tile.get("subtitle"):
        blocks.append({"type": "subtitle", "text": tile["subtitle"]})

    img = image_block(tile.get("image"))
    if img:
        blocks.append(img)
    else:
        emb = embed_block(tile.get("embed"))
        if emb:
            blocks.append(emb)

    if section_expand in ("hover", "click"):
        blocks.append({"type": "expand"})

    if tile.get("body"):
        blocks.append({"type": "body", "text": tile["body"]})

    for qa in tile.get("qa", []) or []:
        if qa.get("question") or qa.get("answer"):
            blocks.append({"type": "note", "heading": qa.get("question", ""), "detail": qa.get("answer", "")})

    for row in tile.get("meta", []) or []:
        if row.get("label") or row.get("value"):
            blocks.append({"type": "note", "heading": row.get("label", ""), "detail": row.get("value", "")})

    if tile.get("email"):
        blocks.append({"type": "email", "value": tile["email"]})

    if tile.get("buttons"):
        blocks.append({"type": "buttons", "items": tile["buttons"]})

    new_tile = {"preset": tile_preset}
    if tile.get("style"):
        new_tile["style"] = tile["style"]
    if tile.get("badge"):
        new_tile["badge"] = tile["badge"]
    new_tile["blocks"] = blocks
    return new_tile


def migrate_section(section):
    if section.get("type") != "tile-grid":
        return section

    old_preset = section.get("preset")
    tile_preset = PRESET_MAP.get(old_preset, "custom")
    section_expand = (section.get("behavior") or {}).get("expand", "none")

    section = dict(section)
    section.pop("preset", None)
    section.pop("behavior", None)
    section["tiles"] = [migrate_tile(t, section_expand, tile_preset) for t in section.get("tiles", [])]
    return section


def migrate_file(path, write=True):
    data = yaml.safe_load(path.read_text())
    original = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)

    data["sections"] = [migrate_section(s) for s in data.get("sections", [])]
    migrated = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)

    if migrated == original:
        print(f"{path}: no change")
        return

    if write:
        path.write_text(migrated)
        print(f"{path}: migrated")
    else:
        print(f"{path}: would migrate —")
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            migrated.splitlines(keepends=True),
            fromfile=str(path) + " (before)",
            tofile=str(path) + " (after)",
        )
        sys.stdout.writelines(diff)
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Print a diff only, don't write")
    parser.add_argument("--dir", default=str(CONTENT_DIR))
    args = parser.parse_args()

    for path in sorted(Path(args.dir).glob("*.yml")):
        migrate_file(path, write=not args.check)


if __name__ == "__main__":
    main()
