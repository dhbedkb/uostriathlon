from pathlib import Path
import re
import subprocess
import shutil

ROOT = Path(".")
IMAGE_DIR = ROOT / "assets" / "images"

TEXT_EXTENSIONS = {
    ".yml", ".yaml", ".html", ".css", ".md", ".js"
}

IMAGE_EXTENSIONS_TO_CONVERT = {
    ".png", ".jpg", ".jpeg"
}

# ------------------------------------------------------------
# 1. Convert existing raster images to WebP where possible
# ------------------------------------------------------------

if not IMAGE_DIR.exists():
    raise SystemExit("assets/images does not exist")

sips = shutil.which("sips")

converted = []
failed = []

for path in IMAGE_DIR.rglob("*"):
    if not path.is_file():
        continue

    if path.suffix.lower() not in IMAGE_EXTENSIONS_TO_CONVERT:
        continue

    target = path.with_suffix(".webp")

    if target.exists():
        continue

    if not sips:
        failed.append((str(path), "sips not found"))
        continue

    result = subprocess.run(
        ["sips", "-s", "format", "webp", str(path), "--out", str(target)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode == 0 and target.exists():
        converted.append((str(path), str(target)))
    else:
        failed.append((str(path), result.stderr.strip() or result.stdout.strip()))

# ------------------------------------------------------------
# 2. Update all project references to assets/images/* as .webp
# ------------------------------------------------------------

reference_pattern = re.compile(
    r"((?:/)?assets/images/[^\\s\\)\\]'\\\"<>]+?)\\.(png|jpg|jpeg|svg)",
    re.IGNORECASE
)

updated_files = []

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    if ".git" in path.parts:
        continue

    if "_site" in path.parts:
        continue

    if ".jekyll-cache" in path.parts:
        continue

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        continue

    text = path.read_text(errors="ignore")
    new_text = reference_pattern.sub(r"\1.webp", text)

    if new_text != text:
        path.write_text(new_text)
        updated_files.append(str(path))

# ------------------------------------------------------------
# 3. Check for remaining non-WebP image references
# ------------------------------------------------------------

remaining_non_webp = []

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    if ".git" in path.parts or "_site" in path.parts or ".jekyll-cache" in path.parts:
        continue

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        continue

    text = path.read_text(errors="ignore")

    for match in reference_pattern.finditer(text):
        remaining_non_webp.append((str(path), match.group(0)))

# ------------------------------------------------------------
# 4. Check for missing referenced WebP files
# ------------------------------------------------------------

webp_pattern = re.compile(
    r"(?:/)?assets/images/[^\\s\\)\\]'\\\"<>]+?\\.webp",
    re.IGNORECASE
)

missing_webp = set()

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    if ".git" in path.parts or "_site" in path.parts or ".jekyll-cache" in path.parts:
        continue

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        continue

    text = path.read_text(errors="ignore")

    for match in webp_pattern.finditer(text):
        ref = match.group(0).lstrip("/")
        ref_path = ROOT / ref

        if not ref_path.exists():
            missing_webp.add(ref)

# ------------------------------------------------------------
# 5. Output report
# ------------------------------------------------------------

print("\\nConverted images:")
if converted:
    for old, new in converted:
        print(f"  {old} -> {new}")
else:
    print("  None converted, or WebP versions already existed.")

print("\\nUpdated reference files:")
if updated_files:
    for file in updated_files:
        print(f"  {file}")
else:
    print("  No references needed updating.")

print("\\nConversion failures:")
if failed:
    for file, reason in failed:
        print(f"  {file}: {reason}")
else:
    print("  None.")

print("\\nRemaining non-WebP image references:")
if remaining_non_webp:
    for file, ref in remaining_non_webp:
        print(f"  {file}: {ref}")
else:
    print("  None.")

print("\\nMissing referenced WebP files:")
if missing_webp:
    for ref in sorted(missing_webp):
        print(f"  {ref}")
else:
    print("  None.")

print("\\nDone.")
