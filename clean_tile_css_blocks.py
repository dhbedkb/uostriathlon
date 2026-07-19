from pathlib import Path

p = Path("assets/css/main.css")
text = p.read_text()

titles = [
    "WIDGET FRAME CONTRACT V2",
    "SOCIAL WIDGET RESPONSIVE SIZING V5",
    "SOCIAL WIDGET NATIVE TILE GRID V7",
    "SOCIAL WIDGET BALANCED GRID V4",
    "SOCIAL WIDGET STRETCH FIX V1",
    "SOCIAL WIDGET GRID CONTRACT V3",
    "FACEBOOK WIDGET BOUNDARY TUNING V1",
    "SOCIAL WIDGET STABLE LAYOUT V8",
    "SOCIAL WIDGET MEASURED STABLE LAYOUT V9",
]
titles += [
    "SOCIAL WIDGET BALANCED STRUCTURE V10",
    "SOCIAL WIDGET NATURAL STACK V11",
    "SOCIAL WIDGET FINAL BALANCED LAYOUT V12",
    "SOCIAL WIDGET EXPLICIT BALANCED LAYOUT V13",
    "SOCIAL WIDGET TRUE STACK LAYOUT V14",
    "SOCIAL WIDGET CLEAN STACK LAYOUT V15",
    "SOCIAL WIDGET FINAL STRUCTURE V16",
    "SOCIAL WIDGET STRICT GAP LAYOUT V17",
    "SOCIAL WIDGET GAP LOCK V18",
]
titles += [
    "SOCIAL WIDGET FACEBOOK FRAME FIT V18B",
    "SOCIAL WIDGET FRAME WRAP V19",
    "SOCIAL WIDGET FACEBOOK CROP V20",
    "SOCIAL WIDGET FRAME SHRINKWRAP V21",
    "SOCIAL WIDGET TILE SHRINKWRAP V22",
    "SOCIAL WIDGET OUTER TILE SPACING V23",
    "SOCIAL WIDGET HARD RESET V24",
    "UNIVERSAL TILE SYSTEM V1",
    "SOCIAL WIDGET TILE COMPONENT V1",
]

def remove_block(source, title):
    marker = "/* =====================================================\n   " + title
    start = source.find(marker)

    if start == -1:
        return source

    next_block = source.find("/* =====================================================", start + len(marker))

    if next_block == -1:
        return source[:start].rstrip() + "\n"

    return source[:start].rstrip() + "\n\n" + source[next_block:]

for title in titles:
    text = remove_block(text, title)

p.write_text(text.rstrip() + "\n")
print("Removed old tile/social widget CSS blocks.")
