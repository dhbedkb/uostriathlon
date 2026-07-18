from pathlib import Path
import yaml

content_dir = Path("_data/content")

for yml in content_dir.glob("*.yml"):
    data = yaml.safe_load(yml.read_text())
    changed = False

    for section in data.get("sections", []):
        stype = section.get("type")

        if stype == "hero":
            if section.get("background_image") and not section.get("background_image_raw"):
                section["background_image_raw"] = section["background_image"]
                section.setdefault("background_crop_x", 50)
                section.setdefault("background_crop_y", 50)
                section.setdefault("background_crop_zoom", 100)
                changed = True

        if stype == "cards":
            for card in section.get("cards", []):
                if card.get("image") and not card.get("image_raw"):
                    card["image_raw"] = card["image"]
                    card.setdefault("crop_x", 50)
                    card.setdefault("crop_y", 50)
                    card.setdefault("crop_zoom", 100)
                    changed = True

        if stype == "gallery":
            for item in section.get("images", []):
                if item.get("src") and not item.get("src_raw"):
                    item["src_raw"] = item["src"]
                    item.setdefault("crop_x", 50)
                    item.setdefault("crop_y", 50)
                    item.setdefault("crop_zoom", 100)
                    changed = True

        if stype == "socials":
            for item in section.get("items", []):
                if item.get("icon") and not item.get("icon_raw"):
                    item["icon_raw"] = item["icon"]
                    item.setdefault("crop_x", 50)
                    item.setdefault("crop_y", 50)
                    item.setdefault("crop_zoom", 100)
                    changed = True

        if stype == "committee":
            for member in section.get("members", []):
                legacy = member.get("image")
                if legacy and not member.get("image_raw") and not member.get("image_profile"):
                    if "/assets/images/committee/profiles/" in str(legacy):
                        member["image_profile"] = legacy
                        member["image_raw"] = ""
                    else:
                        member["image_raw"] = legacy
                        member["image_profile"] = ""
                    changed = True

                if "image" in member:
                    del member["image"]
                    changed = True

    if changed:
        yml.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
        print(f"Migrated {yml}")
