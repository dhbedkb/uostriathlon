"""
Reference-scanning cleanup for source/uploaded images only.

This script does NOT touch generated derivatives such as:
- assets/images/generated
- assets/images/committee/profiles

Generated derivatives should be handled by the optimiser, not by generic cleanup.

Usage:
  python3 scripts/cleanup_unreferenced_images.py
  python3 scripts/cleanup_unreferenced_images.py --apply
"""

from pathlib import Path
import argparse

ROOT = Path(".")
BASEURL = "/uostriathlon"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".svg",
    ".bmp",
    ".tif",
    ".tiff",
    ".ico",
    ".heic",
    ".avif",
}

# Source/upload folders only. Do not include generated folders here.
SCAN_DIRS = [
    ROOT / "assets/images/source",
    ROOT / "assets/images/uploads",
    ROOT / "assets/images/brand",
    ROOT / "assets/images/committee/raw",
]

# Places where real image references may live.
# Do not include admin/config.yml or admin/config.local.yml, because those contain
# media_folder/public_folder directory paths rather than actual file references.
REFERENCE_GLOBS = [
    "_data/**/*.yml",
    "_includes/*.html",
    "_layouts/*.html",
    "*.md",
    "assets/css/main.css",
]


def normalise(value):
    value = str(value).strip().strip("'\"")

    if value.startswith(BASEURL + "/"):
        value = value[len(BASEURL):]

    return value.lstrip("/")


def build_reference_text():
    chunks = []

    for pattern in REFERENCE_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file():
                chunks.append(path.read_text(errors="ignore"))

    return "\n".join(chunks)


def is_candidate_file(path):
    if not path.is_file():
        return False

    if path.name in {".gitkeep", ".DS_Store"}:
        return False

    return path.suffix.lower() in IMAGE_EXTENSIONS


def is_referenced(path, reference_text):
    rel = normalise(str(path.relative_to(ROOT)).replace("\\", "/"))

    possible_forms = {
        rel,
        "/" + rel,
        BASEURL + "/" + rel,
    }

    return any(form in reference_text for form in possible_forms)


def collect_candidates():
    candidates = []

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue

        for path in scan_dir.rglob("*"):
            if is_candidate_file(path):
                candidates.append(path)

    return sorted(candidates)


def main():
    parser = argparse.ArgumentParser(
        description="Find and optionally remove unreferenced source/upload images."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete unreferenced images. Default is dry-run.",
    )

    args = parser.parse_args()

    reference_text = build_reference_text()
    candidates = collect_candidates()

    unreferenced = []

    for path in candidates:
        if not is_referenced(path, reference_text):
            unreferenced.append(path)

    print("Candidate source/upload image files found:", len(candidates))
    print("Unreferenced source/upload image files found:", len(unreferenced))
    print()

    if unreferenced:
        print(("Removing" if args.apply else "Would remove") + " files:")
        for path in unreferenced:
            print("  " + str(path))
    else:
        print("No unreferenced source/upload images found.")

    if args.apply:
        for path in unreferenced:
            path.unlink()
        print()
        print("Deleted", len(unreferenced), "file(s).")
    else:
        print()
        print("Dry run only. Re-run with --apply to delete these files.")


if __name__ == "__main__":
    main()
