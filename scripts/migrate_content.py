"""
One-off migration: rewrites _data/content/*.yml from the old 15-type
section model to the new 4-type model (hero / text / relay-bar /
tile-grid). See ARCHITECTURE.md for the full mapping table.

Safe to re-run: sections already in the new shape (type already one of
hero/text/relay-bar/tile-grid with a `layout` key) are left untouched.

Phase 3 note: this script still writes the pre-Phase-3 key names
(`behavior.expand: none/hover/click`) because it predates that change
and is kept only as a historical record of the original 15→4 migration.
Running it against content that's already on the Phase 3 schema
(`behavior.expandable: true/false`, `visibility: ...: hidden_initially`)
is harmless — those sections are already caught by the "already
migrated" check below and left alone — but this script does NOT perform
the Phase 3 key rename itself. That rename was applied by hand across
_data/content/*.yml (see MIGRATION.md, "Phase 3" section) since it only
touched a handful of files and keys, not a new section-type shape.

Usage:
  python3 scripts/migrate_content.py            # writes in place
  python3 scripts/migrate_content.py --check    # prints, doesn't write
"""

from pathlib import Path
import argparse
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "_data/content"


def image_obj(raw=None, optimised=None, alt=None, caption=None,
              crop_x=50, crop_y=50, crop_zoom=100, shape="square"):
    if not raw and not optimised:
        return None
    obj = {}
    if raw:
        obj["src_raw"] = raw
    if optimised:
        obj["src"] = optimised
    if alt:
        obj["alt"] = alt
    if caption:
        obj["caption"] = caption
    obj["crop_x"] = crop_x
    obj["crop_y"] = crop_y
    obj["crop_zoom"] = crop_zoom
    if shape != "square":
        obj["shape"] = shape
    return obj


def meta_row(label, value):
    return {"label": label, "value": value} if value else None


def buttons_from(primary=None, secondary=None):
    out = []
    for b, style in ((primary, "primary"), (secondary, "secondary")):
        if b and b.get("label") and b.get("url"):
            out.append({"label": b["label"], "url": b["url"], "style": style})
    return out


def heading_fields(section):
    return {
        k: section[k]
        for k in ("eyebrow", "title", "subtitle", "alignment")
        if section.get(k) not in (None, "")
    }


def migrate_stats(section):
    tiles = []
    for item in section.get("items", []):
        tiles.append({"title": item.get("number"), "subtitle": item.get("label")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "stats",
        **heading_fields(section),
        "layout": {"columns": 4, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_cards(section):
    tiles = []
    for card in section.get("cards", []):
        meta = [r for r in (meta_row("Schedule", card.get("schedule")),
                             meta_row("Location", card.get("location"))) if r]
        tile = {
            "eyebrow": card.get("label"),
            "title": card.get("title"),
            "body": card.get("description"),
        }
        img = image_obj(raw=card.get("image_raw"), optimised=card.get("image"),
                         alt=card.get("label") or card.get("title"),
                         crop_x=card.get("crop_x", 50), crop_y=card.get("crop_y", 50),
                         crop_zoom=card.get("crop_zoom", 100))
        if img:
            tile["image"] = img
        if meta:
            tile["meta"] = meta
        if card.get("url"):
            tile["buttons"] = [{"label": "Learn more", "url": card["url"], "style": "secondary"}]
        tiles.append({k: v for k, v in tile.items() if v not in (None, "")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "cards",
        **heading_fields(section),
        "layout": {"columns": 3, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_gallery(section):
    tiles = []
    for img in section.get("images", []):
        image = image_obj(raw=img.get("src_raw"), optimised=img.get("src"),
                           alt=img.get("alt"), caption=img.get("caption"),
                           crop_x=img.get("crop_x", 50), crop_y=img.get("crop_y", 50),
                           crop_zoom=img.get("crop_zoom", 100))
        tile = {}
        if image:
            tile["image"] = image
        if img.get("caption"):
            tile["subtitle"] = img["caption"]
        tiles.append(tile)
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "gallery",
        **heading_fields(section),
        "layout": {"columns": 3, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_events(section):
    tiles = []
    for item in section.get("items", []):
        meta = [r for r in (meta_row("Type", item.get("type")),
                             meta_row("Location", item.get("location"))) if r]
        tile = {
            "badge": item.get("date"),
            "title": item.get("title"),
            "body": item.get("description"),
        }
        if meta:
            tile["meta"] = meta
        if item.get("url"):
            tile["buttons"] = [{"label": "View details", "url": item["url"], "style": "secondary"}]
        tiles.append({k: v for k, v in tile.items() if v not in (None, "")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "events",
        **heading_fields(section),
        "layout": {"columns": 3, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_committee(section):
    tiles = []
    for member in section.get("members", []):
        image = image_obj(raw=member.get("image_raw"), optimised=member.get("image_profile"),
                           alt=member.get("name"),
                           crop_x=member.get("crop_x", 50), crop_y=member.get("crop_y", 50),
                           crop_zoom=member.get("crop_zoom", 100))
        tile = {
            "title": member.get("name"),
            "subtitle": member.get("role"),
            "body": member.get("bio"),
        }
        if image:
            tile["image"] = image
        qa = [{"question": q.get("question"), "answer": q.get("answer")}
              for q in member.get("questions", []) if q.get("question") or q.get("answer")]
        if qa:
            tile["qa"] = qa
        if member.get("email"):
            tile["email"] = member["email"]
        tiles.append({k: v for k, v in tile.items() if v not in (None, "")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "committee",
        **heading_fields(section),
        "layout": {"columns": 3, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "hover"},
        "tiles": tiles,
    }


def migrate_sponsors(section):
    tiles = []
    for sponsor in section.get("sponsors", []):
        tile = {"title": sponsor.get("name"), "body": sponsor.get("description")}
        if sponsor.get("url"):
            tile["buttons"] = [{"label": "Visit", "url": sponsor["url"], "style": "secondary"}]
        tiles.append({k: v for k, v in tile.items() if v not in (None, "")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "sponsors",
        **heading_fields(section),
        "layout": {"columns": 4, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_timeline(section):
    tiles = []
    for item in section.get("items", []):
        tiles.append({k: v for k, v in {
            "title": item.get("title"), "body": item.get("description"),
        }.items() if v})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "timeline",
        **heading_fields(section),
        "layout": {"columns": 1, "equal_height": False, "width": "narrow",
                   "padding": "normal", "background": "default", "numbered": True},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_faq(section):
    tiles = []
    for item in section.get("items", []):
        tiles.append({"title": item.get("question"), "body": item.get("answer")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "faq",
        **heading_fields(section),
        "layout": {"columns": 1, "equal_height": False, "width": "narrow",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "click"},
        "tiles": tiles,
    }


def migrate_cta(section):
    tile = {"title": section.get("title"), "body": section.get("body")}
    buttons = buttons_from(section.get("primary_button"), section.get("secondary_button"))
    if buttons:
        tile["buttons"] = buttons
    if section.get("eyebrow"):
        tile["eyebrow"] = section["eyebrow"]
    tile["style"] = "accent"
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "cta",
        "layout": {"columns": 1, "equal_height": False, "width": "narrow",
                   "padding": "spacious", "background": "default", "align_center": True},
        "behavior": {"expand": "none"},
        "tiles": [{k: v for k, v in tile.items() if v not in (None, "")}],
    }


def migrate_embed(section):
    tiles = []
    if section.get("embeds"):
        for e in section["embeds"]:
            tile = {
                "eyebrow": e.get("provider"),
                "title": e.get("title"),
                "body": e.get("description"),
            }
            if e.get("embed_html"):
                tile["embed"] = {"embed_html": e["embed_html"], "width": e.get("frame_width")}
            elif e.get("url"):
                tile["buttons"] = [{"label": e.get("button_label") or "Open", "url": e["url"], "style": "secondary"}]
            tiles.append({k: v for k, v in tile.items() if v not in (None, "")})
    elif section.get("embed_html"):
        tiles.append({"embed": {"embed_html": section["embed_html"]}})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "embed",
        **heading_fields(section),
        "layout": {"columns": 1, "equal_height": False, "width": "narrow",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_socials(section):
    tiles = []
    for item in section.get("items", []):
        image = image_obj(raw=item.get("icon_raw"), optimised=item.get("icon"),
                           alt=item.get("platform"),
                           crop_x=item.get("crop_x", 50), crop_y=item.get("crop_y", 50),
                           crop_zoom=item.get("crop_zoom", 100), shape="round")
        tile = {"eyebrow": item.get("platform"), "title": item.get("title"),
                "body": item.get("description")}
        if image:
            tile["image"] = image
        if item.get("url"):
            tile["buttons"] = [{"label": item.get("button") or "Open", "url": item["url"], "style": "secondary"}]
        tiles.append({k: v for k, v in tile.items() if v not in (None, "")})
    chip_style = section.get("layout") == "logos"
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "socials",
        **heading_fields(section),
        "layout": {"columns": 4, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default",
                   "chip_style": chip_style},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


def migrate_tile_grid(section):
    tiles = []
    for tile in section.get("tiles", []):
        new_tile = {"title": tile.get("title"), "body": tile.get("body")}
        # Old tile_grid supported one level of nested children; fold them
        # into meta rows rather than inventing nested tiles.
        meta = [meta_row(c.get("title"), c.get("body")) for c in tile.get("children", [])]
        meta = [m for m in meta if m]
        if meta:
            new_tile["meta"] = meta
        tiles.append({k: v for k, v in new_tile.items() if v not in (None, "")})
    return {
        "type": "tile-grid", "id": section.get("id"), "preset": "custom",
        **heading_fields(section),
        "layout": {"columns": 3, "equal_height": True, "width": "normal",
                   "padding": "normal", "background": "default"},
        "behavior": {"expand": "none"},
        "tiles": tiles,
    }


MIGRATORS = {
    "stats": migrate_stats,
    "cards": migrate_cards,
    "gallery": migrate_gallery,
    "events": migrate_events,
    "committee": migrate_committee,
    "sponsors": migrate_sponsors,
    "timeline": migrate_timeline,
    "faq": migrate_faq,
    "cta": migrate_cta,
    "embed": migrate_embed,
    "socials": migrate_socials,
    "tile_grid": migrate_tile_grid,
}

PASSTHROUGH = {"hero", "text", "relay-bar"}


def migrate_section(section):
    stype = section.get("type")
    if stype in PASSTHROUGH:
        return section
    if stype == "tile-grid" and "layout" in section:
        return section  # already migrated
    if stype in MIGRATORS:
        return MIGRATORS[stype](section)
    print(f"  ! no migrator for section type '{stype}' (id={section.get('id')}) — left as-is", file=sys.stderr)
    return section


def migrate_file(path, write=True):
    data = yaml.safe_load(path.read_text())
    sections = data.get("sections", [])
    data["sections"] = [migrate_section(s) for s in sections]
    if write:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000))
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Print only, don't write")
    parser.add_argument("--dir", default=str(CONTENT_DIR))
    args = parser.parse_args()

    content_dir = Path(args.dir)
    for path in sorted(content_dir.glob("*.yml")):
        print(f"Migrating {path}")
        migrate_file(path, write=not args.check)


if __name__ == "__main__":
    main()
