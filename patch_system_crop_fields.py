from pathlib import Path

p = Path("admin/config.yml")
text = p.read_text()

if "background_crop_x" not in text:
    text = text.replace(
        '- { label: Background image, name: background_image, widget: image, required: false }',
        '''- { label: Background image, name: background_image, widget: image, required: false }
                  - { label: Background crop horizontal %, name: background_crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                  - { label: Background crop vertical %, name: background_crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                  - { label: Background crop zoom %, name: background_crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false }'''
    )

if "Card crop horizontal %" not in text:
    text = text.replace(
        '- { label: Image, name: image, widget: image, required: false }',
        '''- { label: Image, name: image, widget: image, required: false }
                      - { label: Card crop horizontal %, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Card crop vertical %, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Card crop zoom %, name: crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false }'''
    )

if "Gallery crop horizontal %" not in text:
    text = text.replace(
        '- { label: Image, name: src, widget: image }',
        '''- { label: Image, name: src, widget: image }
                      - { label: Gallery crop horizontal %, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Gallery crop vertical %, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Gallery crop zoom %, name: crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false }'''
    )

    text = text.replace(
        '- { label: Image, name: src, widget: image, required: false }',
        '''- { label: Image, name: src, widget: image, required: false }
                      - { label: Gallery crop horizontal %, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Gallery crop vertical %, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Gallery crop zoom %, name: crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false }'''
    )

if "Social image crop horizontal %" not in text:
    text = text.replace(
        '- { label: Icon, name: icon, widget: image, required: false }',
        '''- { label: Icon, name: icon, widget: image, required: false }
                      - { label: Social image crop horizontal %, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Social image crop vertical %, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Social image crop zoom %, name: crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false }'''
    )

p.write_text(text)

print("Crop controls patched into config.")
