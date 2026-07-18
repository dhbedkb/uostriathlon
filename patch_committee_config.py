from pathlib import Path

p = Path("admin/config.yml")
text = p.read_text()

start_marker = "              - name: committee"
end_marker = "              - name: sponsors"

start = text.find(start_marker)
end = text.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not find committee block markers in admin/config.yml")

new_block = """              - name: committee
                label: Committee members
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Members
                    name: members
                    widget: list
                    summary: "{{fields.name}} — {{fields.role}}"
                    fields:
                      - { label: Photo, name: image, widget: image, required: false }
                      - label: Photo crop position
                        name: image_position
                        widget: select
                        required: false
                        options:
                          - { label: Centre, value: "center center" }
                          - { label: Top, value: "center top" }
                          - { label: Bottom, value: "center bottom" }
                      - { label: Name, name: name, widget: string, required: false }
                      - { label: Role, name: role, widget: string, required: false }
                      - { label: Bio, name: bio, widget: text, required: false }
                      - { label: Email, name: email, widget: string, required: false }
                      - label: Optional questions
                        name: questions
                        widget: list
                        required: false
                        summary: "{{fields.question}}"
                        fields:
                          - { label: Question, name: question, widget: string, required: false }
                          - { label: Answer, name: answer, widget: text, required: false }
                      - { label: Extra details, name: extra_details, widget: markdown, required: false }

"""

text = text[:start] + new_block + text[end:]

text = text.replace(
    """name: secondary_button
                    widget: object
                    fields:""",
    """name: secondary_button
                    widget: object
                    required: false
                    fields:"""
)

text = text.replace(
    """name: secondary_button
                    widget: object
                    required: false
                    required: false
                    fields:""",
    """name: secondary_button
                    widget: object
                    required: false
                    fields:"""
)

p.write_text(text)
print("Patched admin/config.yml")
