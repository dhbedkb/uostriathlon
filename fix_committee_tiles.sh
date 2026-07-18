#!/usr/bin/env bash
set -e

echo "Writing new committee include..."

cat > _includes/committee.html <<'HTML'
<section id="{{ include.section_id }}" class="section section-committee" data-section-type="committee">
  <div class="container">
    {% include section-heading.html
      eyebrow=include.section.eyebrow
      title=include.section.title
      subtitle=include.section.subtitle
      alignment=include.section.alignment
    %}

    {% if include.section.members %}
      <div class="committee-tile-list">
        {% for member in include.section.members %}
          {% assign image_position = member.image_position | default: "center center" %}
          {% assign has_extra = false %}
          {% if member.image or member.bio or member.email or member.questions or member.extra_details %}
            {% assign has_extra = true %}
          {% endif %}

          <details class="committee-member-tile reveal-card">
            <summary class="committee-tile-summary">
              <span class="committee-tile-main">
                {% if member.name %}
                  <span class="committee-tile-name">{{ member.name }}</span>
                {% else %}
                  <span class="committee-tile-name">Committee member</span>
                {% endif %}

                {% if member.role %}
                  <span class="committee-tile-role">{{ member.role }}</span>
                {% endif %}
              </span>

              <span class="committee-tile-action" aria-hidden="true">More</span>
            </summary>

            {% if has_extra %}
              <div class="committee-tile-expanded">
                <div class="committee-expanded-grid">
                  <div class="committee-expanded-image-wrap" style="--committee-image-position: {{ image_position }};">
                    {% if member.image %}
                      {{ member.image | relative_url }}
                    {% else %}
                      <div class="committee-expanded-placeholder" aria-hidden="true">
                        <span>{{ member.name | default: '?' | slice: 0 }}</span>
                      </div>
                    {% endif %}
                  </div>

                  <div class="committee-expanded-content">
                    {% if member.bio %}
                      <p class="committee-expanded-bio">{{ member.bio }}</p>
                    {% endif %}

                    {% if member.questions %}
                      <div class="committee-question-list">
                        {% for item in member.questions %}
                          {% if item.question or item.answer %}
                            <div class="committee-question">
                              {% if item.question %}
                                <strong>{{ item.question }}</strong>
                              {% endif %}
                              {% if item.answer %}
                                <p>{{ item.answer }}</p>
                              {% endif %}
                            </div>
                          {% endif %}
                        {% endfor %}
                      </div>
                    {% endif %}

                    {% if member.extra_details %}
                      <div class="committee-extra-details">
                        {{ member.extra_details | markdownify }}
                      </div>
                    {% endif %}

                    {% if member.email %}
                      <p class="committee-email">
                        {{ member.email }}Email →</a>
                      </p>
                    {% endif %}
                  </div>
                </div>
              </div>
            {% endif %}
          </details>
        {% endfor %}
      </div>
    {% endif %}
  </div>

  <script>
    (function () {
      if (!window.matchMedia || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
        return;
      }

      document.querySelectorAll("#{{ include.section_id }} .committee-member-tile").forEach(function (tile) {
        tile.addEventListener("mouseenter", function () {
          if (!tile.open) {
            tile.dataset.hoverOpened = "true";
            tile.open = true;
          }
        });

        tile.addEventListener("mouseleave", function () {
          if (tile.dataset.hoverOpened === "true") {
            tile.open = false;
            delete tile.dataset.hoverOpened;
          }
        });

        tile.addEventListener("toggle", function () {
          if (tile.open && tile.dataset.hoverOpened !== "true") {
            delete tile.dataset.hoverOpened;
          }
        });
      });
    })();
  </script>
</section>
HTML

echo "Appending committee tile CSS if needed..."

if ! grep -q "FINAL: compact expandable committee tiles" assets/css/main.css; then
cat >> assets/css/main.css <<'CSS'

/* FINAL: compact expandable committee tiles */

.committee-tile-list {
  display: grid;
  gap: 0.9rem;
  max-width: 980px;
  margin-inline: auto;
}

.committee-member-tile {
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

.committee-member-tile:hover,
.committee-member-tile:focus-within {
  transform: translateY(-2px);
  border-color: rgba(247, 211, 93, 0.45);
  box-shadow: 0 24px 72px rgba(0, 0, 0, 0.24);
}

.committee-member-tile[open] {
  border-color: rgba(247, 211, 93, 0.5);
}

.committee-tile-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
  min-height: 72px;
  padding: 1rem 1.25rem;
  cursor: pointer;
  list-style: none;
}

.committee-tile-summary::-webkit-details-marker {
  display: none;
}

.committee-tile-main {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
}

.committee-tile-name {
  font-size: clamp(1.2rem, 2.4vw, 1.75rem);
  font-weight: 900;
  line-height: 1.05;
}

.committee-tile-role {
  color: var(--color-gold);
  font-size: 0.82rem;
  font-weight: 850;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.committee-tile-action {
  flex: 0 0 auto;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  padding: 0.45rem 0.75rem;
  color: var(--color-gold);
  font-size: 0.8rem;
  font-weight: 850;
}

.committee-member-tile[open] .committee-tile-action {
  background: var(--color-gold);
  color: #000000;
}

.committee-tile-expanded {
  border-top: 1px solid var(--color-border);
  padding: clamp(1rem, 3vw, 1.5rem);
}

.committee-expanded-grid {
  display: grid;
  grid-template-columns: minmax(160px, 220px) minmax(0, 1fr);
  gap: clamp(1rem, 3vw, 1.5rem);
  align-items: start;
}

.committee-expanded-image-wrap {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 1rem;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.24), transparent 14rem),
    #101010;
}

.committee-expanded-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: var(--committee-image-position, center center);
}

.committee-expanded-placeholder {
  display: grid;
  width: 100%;
  height: 100%;
  place-items: center;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.28), transparent 14rem),
    linear-gradient(135deg, #000000, #1a1a1a);
}

.committee-expanded-placeholder span {
  display: grid;
  width: 76px;
  height: 76px;
  place-items: center;
  border-radius: 50%;
  background: var(--color-gold);
  color: #000000;
  font-size: 2.25rem;
  font-weight: 950;
}

.committee-expanded-content {
  color: var(--color-muted);
}

.committee-expanded-bio {
  margin-top: 0;
  font-size: 1.03rem;
}

.committee-question-list {
  display: grid;
  gap: 0.9rem;
  margin-top: 1rem;
}

.committee-question strong {
  display: block;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}

.committee-question p {
  margin: 0;
}

.committee-extra-details {
  margin-top: 1rem;
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

[data-theme="light"] .committee-member-tile {
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.24), transparent 18rem),
    #ffffff;
}

[data-theme="light"] .committee-expanded-content {
  color: #3f3f3f;
}

[data-theme="light"] .committee-question strong {
  color: #000000;
}

@media (max-width: 720px) {
  .committee-tile-summary {
    align-items: flex-start;
    flex-direction: column;
  }

  .committee-tile-action {
    align-self: flex-start;
  }

  .committee-expanded-grid {
    grid-template-columns: 1fr;
  }

  .committee-expanded-image-wrap {
    max-width: 260px;
  }
}
CSS
fi

echo "Patching CMS config committee section..."

cat > patch_committee_config.py <<'PY'
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
PY

python3 patch_committee_config.py

echo "Validating..."

ruby -e 'require "yaml"; YAML.load_file("admin/config.yml", aliases: true); puts "CMS config valid"'
ruby -e 'require "yaml"; YAML.load_file("_data/content/committee.yml"); puts "Committee YAML valid"'

rm -rf _site
bundle exec jekyll build

echo "Done. Run: bundle exec jekyll serve"
