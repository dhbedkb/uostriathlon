"""
Syncs `_data/presets.yml` into the four preset tile-type defaults in
admin/config.yml and admin/config.local.yml.

Presets are edited from Site Settings -> Tile presets, which is really
just editing _data/presets.yml through the same block-list widget a
tile itself uses (the "Tile presets" collection in admin/config.yml
reuses the *block_types alias, same as the committee/faq/sponsor/event
tile types do). This script runs on every publish and rewrites each
preset's `default:` block list inside the Tiles typed-list definition,
so a newly-inserted tile of that preset picks up whatever was last
saved -- no code change needed to edit a preset's *content*.

Only committee/faq/sponsor/event are preset-driven this way. "Blank
tile" (custom) intentionally always starts empty and is left alone.
Adding an entirely new preset *name* still requires a one-line
admin/config.yml edit -- see "Adding a new preset" in
docs/editor-guide.md.

Nothing is written back to _data/presets.yml or committed to git; like
scripts/optimise_site_images.py, this runs fresh on every build.

Usage:
  python3 scripts/apply_presets.py
  python3 scripts/apply_presets.py --check   # print only, don't write
"""

from pathlib import Path
import argparse
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
PRESETS_FILE = ROOT / "_data/presets.yml"
CONFIG_FILES = [ROOT / "admin/config.yml", ROOT / "admin/config.local.yml"]

NAME_RE = re.compile(r"^(?P<indent>[ \t]*)- name: (?P<name>\S+)\s*$")
TYPES_ALIAS_RE = re.compile(r"^[ \t]*types: \*block_types\s*$")
DEFAULT_RE = re.compile(r"^(?P<indent>[ \t]*)default:\s*$")


def block_to_flow_yaml(block):
    """One preset content block -> a single-line YAML flow mapping,
    e.g. {type: title, text: Full Name}, matching the compact style
    already used throughout admin/config.yml."""
    dumped = yaml.safe_dump(block, default_flow_style=True, allow_unicode=True, sort_keys=False)
    return dumped.strip().rstrip(",")


def sync_config(text, presets_by_name):
    lines = text.split("\n")
    out = []
    current_preset = None
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        name_match = NAME_RE.match(line)
        if name_match and name_match.group("name") in presets_by_name:
            current_preset = name_match.group("name")

        if TYPES_ALIAS_RE.match(line) and current_preset in presets_by_name:
            out.append(line)
            i += 1
            if i < len(lines) and DEFAULT_RE.match(lines[i]):
                default_indent = DEFAULT_RE.match(lines[i]).group("indent")
                out.append(lines[i])
                i += 1
                item_indent = default_indent + "  "
                # Skip the existing default list: everything more indented
                # than the `default:` line belongs to it.
                while i < len(lines) and (
                    lines[i].strip() == ""
                    or len(lines[i]) - len(lines[i].lstrip(" ")) > len(default_indent)
                ):
                    i += 1
                for block in presets_by_name[current_preset]["blocks"]:
                    out.append(f"{item_indent}- {block_to_flow_yaml(block)}")
                changed = True
            # Either way, `line` (the types: *block_types line) has already
            # been appended and `i` already advanced past it above -- fall
            # through to the top of the loop rather than the generic
            # append below, or it gets appended a second time (this hit
            # the "Tile presets" collection, which reuses *block_types
            # without a following `default:`, and silently duplicated the
            # line while dropping whatever came after it).
            current_preset = None
            continue

        out.append(line)
        i += 1

    return "\n".join(out), changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Print only, don't write")
    args = parser.parse_args()

    if not PRESETS_FILE.exists():
        print(f"No {PRESETS_FILE}, nothing to sync.")
        return

    data = yaml.safe_load(PRESETS_FILE.read_text()) or {}
    presets = {p["name"]: p for p in data.get("presets", []) if p.get("name")}

    if not presets:
        print("No presets defined, nothing to sync.")
        return

    for config_path in CONFIG_FILES:
        if not config_path.exists():
            continue
        original = config_path.read_text()
        updated, changed = sync_config(original, presets)
        if changed:
            if args.check:
                print(f"Would update {config_path}")
            else:
                config_path.write_text(updated)
                print(f"Updated {config_path}")
        else:
            print(f"{config_path}: no matching presets found, nothing changed")


if __name__ == "__main__":
    main()
