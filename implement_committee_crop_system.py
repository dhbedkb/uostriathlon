from pathlib import Path

LT = chr(60)
GT = chr(62)

def write(path, text):
    text = text.replace("[[LT]]", LT).replace("[[GT]]", GT)
    Path(path).write_text(text)

# ============================================================
# 1. Replace committee include
# ============================================================

write("_includes/committee.html", """[[LT]]section id="{{ include.section_id }}" class="section section-committee" data-section-type="committee"[[GT]]
  [[LT]]div class="container"[[GT]]
    {% include section-heading.html
      eyebrow=include.section.eyebrow
      title=include.section.title
      subtitle=include.section.subtitle
      alignment=include.section.alignment
    %}

    {% if include.section.members %}
      [[LT]]div class="committee-grid committee-crop-grid"[[GT]]
        {% for member in include.section.members %}
          {% assign crop_x = member.crop_x | default: 50 %}
          {% assign crop_y = member.crop_y | default: 50 %}
          {% assign crop_zoom = member.crop_zoom | default: 100 %}

          {% assign has_extra = false %}
          {% if member.image or member.bio or member.email or member.questions or member.extra_details %}
            {% assign has_extra = true %}
          {% endif %}

          [[LT]]details class="committee-crop-card reveal-card"[[GT]]
            [[LT]]summary class="committee-crop-summary"[[GT]]
              [[LT]]span class="committee-crop-title"[[GT]]
                [[LT]]span class="committee-crop-name"[[GT]]{{ member.name | default: "Committee member" }}[[LT]]/span[[GT]]
                {% if member.role %}
                  [[LT]]span class="committee-crop-role"[[GT]]{{ member.role }}[[LT]]/span[[GT]]
                {% endif %}
              [[LT]]/span[[GT]]

              [[LT]]span class="committee-crop-toggle" aria-hidden="true"[[GT]][[LT]]/span[[GT]]
            [[LT]]/summary[[GT]]

            {% if has_extra %}
              [[LT]]div class="committee-crop-expanded"[[GT]]
                {% if member.image %}
                  [[LT]]div
                    class="committee-crop-image-frame"
                    style="--crop-x: {{ crop_x }}%; --crop-y: {{ crop_y }}%; --crop-zoom: {{ crop_zoom | divided_by: 100.0 }};"
                  [[GT]]
                    [[LT]]img
                      class="committee-crop-image"
                      src="{{ member.image | relative_url }}"
                      alt="{{ member.name | default: 'Committee member' }}"
                      loading="lazy"
                    [[GT]]
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.bio %}
                  [[LT]]p class="committee-crop-bio"[[GT]]{{ member.bio }}[[LT]]/p[[GT]]
                {% endif %}

                {% if member.questions %}
                  [[LT]]div class="committee-crop-questions"[[GT]]
                    {% for item in member.questions %}
                      {% if item.question or item.answer %}
                        [[LT]]div class="committee-crop-question"[[GT]]
                          {% if item.question %}
                            [[LT]]strong[[GT]]{{ item.question }}[[LT]]/strong[[GT]]
                          {% endif %}
                          {% if item.answer %}
                            [[LT]]p[[GT]]{{ item.answer }}[[LT]]/p[[GT]]
                          {% endif %}
                        [[LT]]/div[[GT]]
                      {% endif %}
                    {% endfor %}
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.extra_details %}
                  [[LT]]div class="committee-crop-extra"[[GT]]
                    {{ member.extra_details | markdownify }}
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.email %}
                  [[LT]]p class="committee-crop-email"[[GT]]
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
""")

print("Updated _includes/committee.html")


# ============================================================
# 2. Add final CSS override
# ============================================================

css_path = Path("assets/css/main.css")
css = css_path.read_text()

marker = "/* FINAL OVERRIDE V3: committee crop card system */"

if marker not in css:
    css += """

/* FINAL OVERRIDE V3: committee crop card system */

/*
  Committee card behaviour:
  - Desktop: compact multi-column cards.
  - Initial state: name + role only.
  - Expanded state: card grows vertically.
  - Image never exceeds card width.
  - Crop controls come from CMS: crop_x, crop_y, crop_zoom.
*/

.section-committee .committee-crop-grid {
  display: grid !important;
  gap: 1rem !important;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)) !important;
  align-items: start !important;
  max-width: 1120px;
  margin-inline: auto;
}

/* Desktop should not collapse to one column */
@media (min-width: 1050px) {
  .section-committee .committee-crop-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

/* Defensive overrides against older list/tile styles */
.section-committee .committee-grid,
.section-committee .committee-card-grid,
.section-committee .committee-compact-grid,
.section-committee .committee-tile-list {
  max-width: 1120px !important;
}

.section-committee .committee-crop-card {
  display: block !important;
  width: 100% !important;
  max-width: none !important;
  overflow: hidden !important;
  border: 1px solid var(--color-border);
  border-radius: 1.25rem;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.12), transparent 18rem),
    var(--color-surface);
  box-shadow: var(--shadow-soft);
  transition:
    transform 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.section-committee .committee-crop-card:hover,
.section-committee .committee-crop-card:focus-within {
  transform: translateY(-2px);
  border-color: rgba(247, 211, 93, 0.45);
  box-shadow: 0 22px 72px rgba(0, 0, 0, 0.25);
}

.section-committee .committee-crop-card[open] {
  border-color: rgba(247, 211, 93, 0.55);
}

/* Compact initial card */
.section-committee .committee-crop-summary {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 1rem !important;
  min-height: 86px !important;
  padding: 1rem 1.15rem !important;
  cursor: pointer;
  list-style: none;
}

.section-committee .committee-crop-summary::-webkit-details-marker {
  display: none;
}

.section-committee .committee-crop-title {
  display: grid !important;
  gap: 0.32rem !important;
  min-width: 0;
}

.section-committee .committee-crop-name {
  display: block !important;
  color: var(--color-text);
  font-size: clamp(1.18rem, 2.2vw, 1.62rem) !important;
  line-height: 1.05 !important;
  font-weight: 950 !important;
}

.section-committee .committee-crop-role {
  display: block !important;
  color: var(--color-gold) !important;
  font-size: 0.78rem !important;
  font-weight: 900 !important;
  letter-spacing: 0.08em !important;
  line-height: 1.25 !important;
  text-transform: uppercase !important;
}

/* Plus/minus button */
.section-committee .committee-crop-toggle {
  position: relative;
  flex: 0 0 auto;
  width: 2rem;
  height: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
}

.section-committee .committee-crop-toggle::before,
.section-committee .committee-crop-toggle::after {
  content: "";
  position: absolute;
  inset: 50% auto auto 50%;
  width: 0.78rem;
  height: 2px;
  background: var(--color-gold);
  transform: translate(-50%, -50%);
}

.section-committee .committee-crop-toggle::after {
  transform: translate(-50%, -50%) rotate(90deg);
}

.section-committee .committee-crop-card[open] .committee-crop-toggle {
  background: var(--color-gold);
  border-color: var(--color-gold);
}

.section-committee .committee-crop-card[open] .committee-crop-toggle::before,
.section-committee .committee-crop-card[open] .committee-crop-toggle::after {
  background: #000000;
}

.section-committee .committee-crop-card[open] .committee-crop-toggle::after {
  display: none;
}

/* Expanded body is constrained to card */
.section-committee .committee-crop-expanded {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box;
  border-top: 1px solid var(--color-border);
  padding: 1rem 1.15rem 1.15rem !important;
}

/* Image frame: strict square crop within card width */
.section-committee .committee-crop-image-frame {
  position: relative;
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

/*
  object-position performs the framing.
  transform scale provides the zoom.
*/
.section-committee .committee-crop-image {
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  object-fit: cover !important;
  object-position: var(--crop-x, 50%) var(--crop-y, 50%) !important;
  transform: scale(var(--crop-zoom, 1));
  transform-origin: var(--crop-x, 50%) var(--crop-y, 50%);
}

.section-committee .committee-crop-bio {
  margin-top: 0;
  color: var(--color-muted);
}

.section-committee .committee-crop-questions {
  display: grid;
  gap: 0.85rem;
  margin-top: 1rem;
}

.section-committee .committee-crop-question strong {
  display: block;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}

.section-committee .committee-crop-question p {
  margin: 0;
  color: var(--color-muted);
}

.section-committee .committee-crop-extra {
  margin-top: 1rem;
  color: var(--color-muted);
}

.section-committee .committee-crop-extra p:first-child {
  margin-top: 0;
}

.section-committee .committee-crop-extra p:last-child {
  margin-bottom: 0;
}

.section-committee .committee-crop-email {
  margin-bottom: 0;
}

/* Light mode */
[data-theme="light"] .section-committee .committee-crop-card {
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.22), transparent 18rem),
    #ffffff;
}

[data-theme="light"] .section-committee .committee-crop-bio,
[data-theme="light"] .section-committee .committee-crop-question p,
[data-theme="light"] .section-committee .committee-crop-extra {
  color: #3f3f3f;
}

[data-theme="light"] .section-committee .committee-crop-question strong {
  color: #000000;
}

/* Mobile: single column */
@media (max-width: 760px) {
  .section-committee .committee-crop-grid {
    grid-template-columns: 1fr !important;
  }

  .section-committee .committee-crop-summary {
    min-height: 78px !important;
  }
}
"""
    css_path.write_text(css)
    print("Appended final committee crop CSS")
else:
    print("Final committee crop CSS already present")


# ============================================================
# 3. Patch CMS config committee block with visible crop controls
# ============================================================

config_path = Path("admin/config.yml")
config = config_path.read_text()

start_marker = "              - name: committee"
end_marker = "              - name: sponsors"

start = config.find(start_marker)
end = config.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not find committee/sponsors markers in admin/config.yml")

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
                      - { label: Crop horizontal focus %, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false, hint: "0 = left, 50 = centre, 100 = right" }
                      - { label: Crop vertical focus %, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false, hint: "0 = top, 50 = centre, 100 = bottom" }
                      - { label: Crop zoom %, name: crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false, hint: "100 = normal. Increase to zoom in on the face." }
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

# Ensure CTA secondary button is optional.
config = config.replace(
    """name: secondary_button
                    widget: object
                    fields:""",
    """name: secondary_button
                    widget: object
                    required: false
                    fields:"""
)

config = config.replace(
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

config_path.write_text(config)
print("Updated admin/config.yml committee block with crop controls")

