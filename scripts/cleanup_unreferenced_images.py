from pathlib import Path
import argparse
import re

ROOT = Path(".")

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
    ".bmp", ".tif", ".tiff", ".ico", ".heic", ".avif"
}

SCAN_DIRS = [
    ROOT / "assets/images/source",
    ROOT / "assets/images/uploads",
    ROOT / "assets/images/brand",
    ROOT / "assets/images/committee/raw",
    ROOT / "assets/images/committee/profiles",
    ROOT / "assets/images/generated",
]

DATA_DIRS = [
    ROOT / "_data",
]

def normalise_path(value):
    value = str(value).strip().strip("'\"")

    if value.startswith("/uostriathlon/assets/images/"):
        return value.replace("/uostriathlon/", "", 1).lstrip("/")

    if value.startswith("/assets/images/"):
        return value.lstrip("/")

    if value.startswith("assets/images/"):
        return value

    return None


def collect_references():
    references = set()

    for data_dir in DATA_DIRS:
        if not data_dir.exists():
            continue

        for path in data_dir.rglob("*.yml"):
            text = path.read_text(errors="ignore")

            matches = re.findall(
                r'(?:"|\')?(/?uostriathlon/assets/images/[^"\'\s]+|/?assets/images/[^"\'\s]+)(?:"|\')?',
                text
            )

            for match in matches:
                normalised = normalise_path(match)
                if normalised:
                    references.add(normalised)

    return references

def is_candidate_file(path):
    if not path.is_file():
        return False

    if path.name in {".gitkeep", ".DS_Store"}:
        return False

    return path.suffix.lower() in IMAGE_EXTENSIONS


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
        description="Find and optionally remove unreferenced images."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete unreferenced images. Default is dry-run."
    )

    args = parser.parse_args()

    references = collect_references()
    candidates = collect_candidates()

    unreferenced = []

    for path in candidates:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")

        if rel not in references:
            unreferenced.append(path)

    print("Referenced image paths found:", len(references))
    print("Candidate image files found:", len(candidates))
    print("Unreferenced image files found:", len(unreferenced))
    print()

    if unreferenced:
        print("Unreferenced files:")
        for path in unreferenced:
            print("  " + str(path))

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
