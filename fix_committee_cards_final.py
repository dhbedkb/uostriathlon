from pathlib import Path

LT = chr(60)
GT = chr(62)

def write(path, text):
    text = text.replace("[[LT]]", LT).replace("[[GT]]", GT)
    Path(path).write_text(text)

# ------------------------------------------------------------
# 1. Replace committee include with compact expandable grid cards
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
      [[LT]]div class="committee-grid committee-compact-grid"[[GT]]
        {% for member in include.section.members %}
          {% assign image_position = member.image_position | default: "center center" %}
          {% assign has_extra = false %}
          {% if member.image or member.bio or member.email or member.questions or member.extra_details %}
            {% assign has_extra = true %}
          {% endif %}

          [[LT]]details class="committee-tile reveal-card"[[GT]]
            [[LT]]summary class="committee-tile-summary"[[GT]]
              [[LT]]span class="committee-tile-text"[[GT]]
                [[LT]]span class="committee-tile-name"[[GT]]{{ member.name | default: "Committee member" }}[[LT]]/span[[GT]]
                {% if member.role %}
                  [[LT]]span class="committee-tile-role"[[GT]]{{ member.role }}[[LT]]/span[[GT]]
                {% endif %}
              [[LT]]/span[[GT]]

              [[LT]]span class="committee-tile-toggle" aria-hidden="true"[[GT]][[LT]]/span[[GT]]
            [[LT]]/summary[[GT]]

            {% if has_extra %}
              [[LT]]div class="committee-tile-body"[[GT]]
                {% if member.image %}
                  [[LT]]div class="committee-tile-image-wrap" style="--committee-image-position: {{ image_position }};"[[GT]]
                    [[LT]]img
                      class="committee-tile-image"
                      src="{{ member.image | relative_url }}"
                      alt="{{ member.name | default: 'Committee member' }}"
                      loading="lazy"
                    [[GT]]
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.bio %}
                  [[LT]]p class="committee-tile-bio"[[GT]]{{ member.bio }}[[LT]]/p[[GT]]
                {% endif %}

                {% if member.questions %}
                  [[LT]]div class="committee-question-list"[[GT]]
                    {% for item in member.questions %}
                      {% if item.question or item.answer %}
                        [[LT]]div class="committee-question"[[GT]]
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
                  [[LT]]div class="committee-extra-details"[[GT]]
                    {{ member.extra_details | markdownify }}
                  [[LT]]/div[[GT]]
                {% endif %}

                {% if member.email %}
                  [[LT]]p class="committee-email"[[GT]]
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

print("Updated _includes/committee.html with real img tags and compact expandable tiles.")

# ------------------------------------------------------------
# 2. Append final committee CSS override
# ------------------------------------------------------------

css_path = Path("assets/css/main.css")
css = css_path.read_text()

marker = "/* FINAL OVERRIDE: compact committee grid tiles */"

if marker not in css:
    css += """

/* FINAL OVERRIDE: compact committee grid tiles */

/*
  Committee tiles:
  - Desktop/tablet: multi-column grid, compact cards.
  - Initial state: name + role only.
  - Expanded state: card grows vertically to show image and details.
  - Mobile: still tap-to-expand, usually one column.
*/

.committee-compact-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)) !important;
  gap: 1rem !important;
  align-items: start !important;
}

.committee-tile {
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

.committee-tile:hover,
.committee-tile:focus-within {
  transform: translateY(-2px);
  border-color: rgba(247, 211, 93, 0.45);
  box-shadow: 0 20px 70px rgba(0, 0, 0, 0.24);
}

.committee-tile[open] {
  border-color: rgba(247, 211, 93, 0.55);
}

.committee-tile-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.85rem;
  min-height: 76px;
  padding: 1rem 1.1rem;
  cursor: pointer;
  list-style: none;
}

.committee-tile-summary::-webkit-details-marker {
  display: none;
}

.committee-tile-text {
  display: grid;
  gap: 0.25rem;
  min-width: 0;
}

.committee-tile-name {
  font-size: clamp(1.1rem, 2vw, 1.45rem);
  line-height: 1.05;
  font-weight: 900;
}

.committee-tile-role {
  color: var(--color-gold);
  font-size: 0.76rem;
  font-weight: 850;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.committee-tile-toggle {
  position: relative;
  flex: 0 0 auto;
  width: 2rem;
  height: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
}

.committee-tile-toggle::before,
.committee-tile-toggle::after {
  content: "";
  position: absolute;
  inset: 50% auto auto 50%;
  width: 0.8rem;
  height: 2px;
  background: var(--color-gold);
  transform: translate(-50%, -50%);
}

.committee-tile-toggle::after {
  transform: translate(-50%, -50%) rotate(90deg);
}

.committee-tile[open] .committee-tile-toggle {
  background: var(--color-gold);
  border-color: var(--color-gold);
}

.committee-tile[open] .committee-tile-toggle::before,
.committee-tile[open] .committee-tile-toggle::after {
  background: #000000;
}

.committee-tile[open] .committee-tile-toggle::after {
  display: none;
}

.committee-tile-body {
  border-top: 1px solid var(--color-border);
  padding: 1rem 1.1rem 1.15rem;
}

.committee-tile-image-wrap {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 1rem;
  margin-bottom: 1rem;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.24), transparent 14rem),
    #101010;
}

.committee-tile-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: var(--committee-image-position, center center);
}

.committee-tile-bio {
  color: var(--color-muted);
  margin-top: 0;
}

.committee-question-list {
  display: grid;
  gap: 0.85rem;
  margin-top: 1rem;
}

.committee-question strong {
  display: block;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}

.committee-question p {
  margin: 0;
  color: var(--color-muted);
}

.committee-extra-details {
  margin-top: 1rem;
  color: var(--color-muted);
}

.committee-extra-details p:first-child {
  margin-top: 0;
}

.committee-extra-details p:last-child {
  margin-bottom: 0;
}

.committee-email {
  margin-bottom: 0;
}

[data-theme="light"] .committee-tile {
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.22), transparent 18rem),
    #ffffff;
}

[data-theme="light"] .committee-tile-bio,
[data-theme="light"] .committee-question p,
[data-theme="light"] .committee-extra-details {
  color: #3f3f3f;
}

[data-theme="light"] .committee-question strong {
  color: #000000;
}

@media (min-width: 1100px) {
  .committee-compact-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 760px) {
  .committee-compact-grid {
    grid-template-columns: 1fr !important;
  }

  .committee-tile-summary {
    min-height: 70px;
  }
}
"""
    css_path.write_text(css)
    print("Added final committee tile CSS override.")
else:
    print("Final committee tile CSS already present.")

# ------------------------------------------------------------
# 3. Ensure CMS committee member fields are sane and non-duplicated
# ------------------------------------------------------------

config_path = Path("admin/config.yml")
config = config_path.read_text()

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
    config = config[:start] + new_committee_block + config[end:]
    config_path.write_text(config)
    print("Replaced committee block in admin/config.yml.")
else:
    print("WARNING: Could not find committee/sponsors markers in admin/config.yml.")

