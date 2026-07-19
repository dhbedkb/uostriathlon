from pathlib import Path
import re

targets = [
    "content-card",
    "event-card",
    "stat-card",
    "social-card",
    "gallery-item",
    "cta-card",
    "notice-card",
    "faq-item",
    "sponsor-card",
    "timeline-item",
    "committee-crop-card",
]

changed = []

for p in Path("_includes").glob("*.html"):
    text = p.read_text()
    original = text

    def patch_class(match):
        classes = match.group(1)
        class_list = classes.split()

        if "u-tile" in class_list:
            return match.group(0)

        if any(target in class_list for target in targets):
            return 'class="u-tile ' + classes + '"'

        return match.group(0)

    text = re.sub(r'class="([^"]+)"', patch_class, text)

    if text != original:
        p.write_text(text)
        changed.append(str(p))

if changed:
    print("Updated:")
    for item in changed:
        print(item)
else:
    print("No include files needed updating.")
