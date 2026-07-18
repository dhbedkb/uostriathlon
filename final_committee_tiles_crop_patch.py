from pathlib import Path

LT = chr(60)
GT = chr(62)

def write(path, text):
    text = text.replace("[[LT]]", LT).replace("[[GT]]", GT)
    Path(path).write_text(text)

# ------------------------------------------------------------
# 1. Committee template:
#    - desktop grid tiles
#    - role under name
#    - tile expands vertically
#    - image constrained to tile width
#    - crop/framing fields using object-position
# ------------------------------------------------------------

write("_includes/committee.html", """[[LT]]section id="{{ include.section_id }}" class="section section-committee" data-section-type="committee"[[GT]]
  [[LT]]div class="container"[[GT]]
    {% include section-heading.html
      eyebrow=include.section.eyebrow
      title=include.section.title
      subtitle=include.section.subtitle
      alignment=include.section.alignment
    %}

    {% if include.section.members %}
      [[LT]]div class="committee-grid committee-card-grid"[[GT]]
        {% for member in include.section.members %}
          {% assign crop_x = member.crop_x | default: 50 %}
          {% assign crop_y = member.crop_y | default: 50 %}

          {% assign has_extra = false %}
          {% if member.image or member.bio or member.email or member.questions or member.extra_details %}
            {% assign has_extra = true %}
          {% endif %}

          [[LT]]details class="committee-card-tile reveal-card"[[GT]]
            [[LT]]summary class="committee-card-summary"[[GT]]
              [[LT]]span class="committee-card-heading"[[GT]]
                [[LT]]span class="committee-card-name"[[GT]]{{ member.name | default: "Committee member" }}[[LT]]/span[[GT]]
                {% if member.role %}
                  [[LT]]span class="committee-card-role"[[GT]]{{ member.role }}[[LT]]/span[[GT]]
                {% endif %}
              [[LT]]/span[[GT]]

              [[LT]]span class="committee-card-toggle" aria-hidden="true"[[GT]][[LT]]/span[[GT]]
            [[LT]]/summary[[GT]]

            {% if has_extra %}
              [[LT]]div class="committee-card-expanded"[[GT]]
                {% if member.image %}
                  [[LT]]div
                    class="committee-card-image-frame"
                    style="--committee-crop-x: {{ crop_x }}%; --committee-crop-y: {{ crop_y }}%;"
                  [[GT]]
                    [[LT]]img
                      class="committee-card-image"
                      src="{{ member.image | relative_url }}"
                      alt="{{ member.name | default: 'Committee member' }}"
                      loading="lazy"
                    [[GT]]
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.bio %}
                  [[LT]]p class="committee-card-bio"[[GT]]{{ member.bio }}[[LT]]/p[[GT]]
                {% endif %}

                {% if member.questions %}
                  [[LT]]div class="committee-card-questions"[[GT]]
                    {% for item in member.questions %}
                      {% if item.question or item.answer %}
                        [[LT]]div class="committee-card-question"[[GT]]
                          {% if item.question %}
                            [[LT]]strong[[GT]]{{ item.question }}[[LT]]/strong[[GT]]
                          {% endif %}
                          {% if item.answer %}
                            [[LT]]p[[GT]]{{ item.answer }}[[LT]]/p[[XGT]]
                          {% endif %}
                        [[LT]]/div[[GT]]
                      {% endif %}
                    {% endfor %}
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.extra_details %}
                  [[LT]]div class="committee-card-extra"[[GT]]
                    {{ member.extra_details | markdownify }}
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.email %}
                  [[LT]]p class="committee-card-email"[[GT]]
                    [[LT]]a class="text-link" href="mailto:{{ member.email }}"[[GT]]Email →[[LT]]/a[[GT]]
                  [[LT]]/p[[GT]]
                {% endif %}
              [[LT]]/div[[GT]]
            {% endif %}
          [[LT]]/details[[GT]]
        {% endfor %}
      [[LT]]/div[[GT]]
    {% endif %}
  [[LT]]/div[[GT]]
[[LT]]/section[[GT]]
""".replace("[[LT]]/p[[XGT]]", "[[LT]]/p[[GT]]"))

print("Updated _includes/committee.html")


# ------------------------------------------------------------
# 2. CSS final override:
#    Explicitly beats older committee CSS.
# ------------------------------------------------------------

css_path = Path("assets/css/main.css")
css = css_path.read_text()

marker = "/* FINAL OVERRIDE V2: committee cards grid with constrained image framing */"

if marker not in css:
    css += """

/* FINAL OVERRIDE V2: committee cards grid with constrained image framing */

/*
  This block intentionally overrides earlier committee/profile/tile styles.
  Desired behaviour:
  - Desktop: multi-column card grid.
  - Initial card: compact tile showing name and role only.
  - Role always sits below name.
  - Expanded content grows vertically inside the same card width.
  - Image is square and constrained to card width.
  - Crop/framing comes from crop_x/crop_y fields in CMS.
*/

.section-committee .committee-card-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)) !important;
  gap: 1rem !important;
  align-items: start !important;
  max-width: 1120px;
  margin-inline: auto;
}

/* On wide desktop keep a clean 3-column layout */
@media (min-width: 1050px) {
  .section-committee .committee-card-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

/* Undo old one-column/list tile assumptions */
.section-committee .committee-tile-list,
.section-committee .committee-compact-grid {
  display: grid !important;
  grid-template-columns: inherit !important;
}

.section-committee .committee-card-tile {
  display: block !important;
  width: 100% !important;
  max-width: none !important;
  border: 1px solid var(--color-border);
  border-radius: 1.25rem;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.12), transparent 18rem),
    var(--color-surface);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
  transition:
    transform 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.section-committee .committee-card-tile:hover,
.section-committee .committee-card-tile:focus-within {
  transform: translateY(-2px);
  border-color: rgba(247, 211, 93, 0.45);
  box-shadow: 0 22px 72px rgba(0, 0, 0, 0.25);
}

.section-committee .committee-card-tile[open] {
  border-color: rgba(247, 211, 93, 0.55);
}

/* Compact initial tile */
.section-committee .committee-card-summary {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 1rem !important;
  min-height: 88px !important;
  padding: 1rem 1.15rem !important;
  cursor: pointer;
  list-style: none;
}

.section-committee .committee-card-summary::-webkit-details-marker {
  display: none;
}

/* Name and role stacked vertically */
.section-committee .committee-card-heading {
  display: grid !important;
  gap: 0.28rem !important;
  min-width: 0;
}

.section-committee .committee-card-name {
  display: block !important;
  font-size: clamp(1.18rem, 2.2vw, 1.65rem) !important;
  line-height: 1.05 !important;
  font-weight: 950 !important;
  color: var(--color-text);
}

.section-committee .committee-card-role {
  display: block !important;
  color: var(--color-gold) !important;
  font-size: 0.78rem !important;
  font-weight: 900 !important;
  letter-spacing: 0.08em !important;
  line-height: 1.25 !important;
  text-transform: uppercase !important;
}

/* Plus/minus control */
.section-committee .committee-card-toggle {
  position: relative;
  flex: 0 0 auto;
  width: 2rem;
  height: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
}

.section-committee .committee-card-toggle::before,
.section-committee .committee-card-toggle::after {
  content: "";
  position: absolute;
  inset: 50% auto auto 50%;
  width: 0.78rem;
  height: 2px;
  background: var(--color-gold);
  transform: translate(-50%, -50%);
}

.section-committee .committee-card-toggle::after {
  transform: translate(-50%, -50%) rotate(90deg);
}

.section-committee .committee-card-tile[open] .committee-card-toggle {
  background: var(--color-gold);
  border-color: var(--color-gold);
}

.section-committee .committee-card-tile[open] .committee-card-toggle::before,
.section-committee .committee-card-tile[open] .committee-card-toggle::after {
  background: #000000;
}

.section-committee .committee-card-tile[open] .committee-card-toggle::after {
  display: none;
}

/* Expanded body remains inside the tile width */
.section-committee .committee-card-expanded {
  width: 100% !important;
  max-width: 100% !important;
  border-top: 1px solid var(--color-border);
  padding: 1rem 1.15rem 1.15rem !important;
  box-sizing: border-box;
}

/* Image constrained to card width */
.section-committee .committee-card-image-frame {
  width: 100% !important;
  max-width: 100% !important;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 1rem;
  margin: 0 0 1rem 0;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.24), transparent 14rem),
    #101010;
}

.section-committee .committee-card-image {
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  object-fit: cover !important;
  object-position: var(--committee-crop-x, 50%) var(--committee-crop-y, 50%) !important;
}

.section-committee .committee-card-bio {
  margin-top: 0;
  color: var(--color-muted);
}

.section-committee .committee-card-questions {
  display: grid;
  gap: 0.85rem;
  margin-top: 1rem;
}

.section-committee .committee-card-question strong {
  display: block;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}

.section-committee .committee-card-question p {
  margin: 0;
  color: var(--color-muted);
}

.section-committee .committee-card-extra {
  margin-top: 1rem;
  color: var(--color-muted);
}

.section-committee .committee-card-extra p:first-child {
  margin-top: 0;
}

.section-committee .committee-card-extra p:last-child {
  margin-bottom: 0;
}

.section-committee .committee-card-email {
  margin-bottom: 0;
}

/* Light mode */
[data-theme="light"] .section-committee .committee-card-tile {
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.22), transparent 18rem),
    #ffffff;
}

[data-theme="light"] .section-committee .committee-card-bio,
[data-theme="light"] .section-committee .committee-card-question p,
[data-theme="light"] .section-committee .committee-card-extra {
  color: #3f3f3f;
}

[data-theme="light"] .section-committee .committee-card-question strong {
  color: #000000;
}

/* Mobile: one column, tap to expand */
@media (max-width: 760px) {
  .section-committee .committee-card-grid {
    grid-template-columns: 1fr !important;
  }

  .section-committee .committee-card-summary {
    min-height: 78px !important;
  }
}
"""
    css_path.write_text(css)
    print("Appended final committee CSS override")
else:
    print("Final committee CSS override already present")


# ------------------------------------------------------------
# 3. CMS config:
#    Add crop_x/crop_y if not already present.
# ------------------------------------------------------------

config_path = Path("admin/config.yml")
config = config_path.read_text()

# Replace committee block to remove duplicates and include crop controls.
start_marker = "              - name: committee"
end_marker = "              - name: sponsors"

start = config.find(start_marker)
end = config.find(end_marker, start)

if start != -1 and end != -1:
    new_committee_block = """              - name: committee
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
                      - { label: Crop focus horizontal percent, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
                      - { label: Crop focus vertical percent, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false }
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
    config = config[:start] + new_committee_block + config[end:]
    config_path.write_text(config)
    print("Updated admin/config.yml committee block with crop controls")
else:
    print("WARNING: Could not locate committee/sponsors markers in admin/config.yml")

