from pathlib import Path

# ============================================================
# 1. Replace committee include with proper images + expandable cards
# ============================================================

Path("_includes/committee.html").write_text("""<section id="{{ include.section_id }}" class="section section-committee" data-section-type="committee">
  <div class="container">
    {% include section-heading.html
      eyebrow=include.section.eyebrow
      title=include.section.title
      subtitle=include.section.subtitle
      alignment=include.section.alignment
    %}

    {% if include.section.members %}
      <div class="committee-grid">
        {% for member in include.section.members %}
          {% assign has_extra = false %}
          {% if member.email or member.questions or member.extra_details %}
            {% assign has_extra = true %}
          {% endif %}

          <article class="profile-card committee-profile-card reveal-card">
            <div class="profile-image-wrap">
              {% if member.image %}
                {{ member.image | relative_url }}
              {% else %}
                <div class="profile-placeholder" aria-hidden="true">
                  <span>{{ member.name | default: '?' | slice: 0 }}</span>
                </div>
              {% endif %}
            </div>

            <div class="profile-card-main">
              {% if member.name %}
                <h3>{{ member.name }}</h3>
              {% endif %}

              {% if member.role %}
                <p class="card-label">{{ member.role }}</p>
              {% endif %}

              {% if member.bio %}
                <p class="profile-bio">{{ member.bio }}</p>
              {% endif %}

              {% if has_extra %}
                <div class="profile-extra profile-extra-desktop">
                  {% if member.questions %}
                    {% for item in member.questions %}
                      {% if item.question or item.answer %}
                        <p>
                          {% if item.question %}
                            <strong>{{ item.question }}</strong>
                          {% endif %}
                          {% if item.answer %}
                            <span>{{ item.answer }}</span>
                          {% endif %}
                        </p>
                      {% endif %}
                    {% endfor %}
                  {% endif %}

                  {% if member.extra_details %}
                    <div class="profile-extra-markdown">
                      {{ member.extra_details | markdownify }}
                    </div>
                  {% endif %}

                  {% if member.email %}
                    <p>
                      {{ member.email }}Email →</a>
                    </p>
                  {% endif %}
                </div>

                <details class="profile-details">
                  <summary>More</summary>

                  <div class="profile-extra profile-extra-mobile">
                    {% if member.questions %}
                      {% for item in member.questions %}
                        {% if item.question or item.answer %}
                          <p>
                            {% if item.question %}
                              <strong>{{ item.question }}</strong>
                            {% endif %}
                            {% if item.answer %}
                              <span>{{ item.answer }}</span>
                            {% endif %}
                          </p>
                        {% endif %}
                      {% endfor %}
                    {% endif %}

                    {% if member.extra_details %}
                      <div class="profile-extra-markdown">
                        {{ member.extra_details | markdownify }}
                      </div>
                    {% endif %}

                    {% if member.email %}
                      <p>
                        {{ member.email }}Email →</a>
                      </p>
                    {% endif %}
                  </div>
                </details>
              {% endif %}
            </div>
          </article>
        {% endfor %}
      </div>
    {% endif %}
  </div>
</section>
""")

print("Updated _includes/committee.html")


# ============================================================
# 2. Add CSS for cropped images + hover/tap expansion
# ============================================================

css_path = Path("assets/css/main.css")
css = css_path.read_text()

marker = "/* FINAL: expandable committee cards with uploaded images */"

if marker not in css:
    css += """

/* FINAL: expandable committee cards with uploaded images */

.committee-profile-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0 !important;
  min-height: 100%;
  transition:
    transform 220ms ease,
    border-color 220ms ease,
    box-shadow 220ms ease;
}

.committee-profile-card:hover,
.committee-profile-card:focus-within {
  transform: translateY(-4px);
  border-color: rgba(247, 211, 93, 0.45);
  box-shadow: 0 28px 90px rgba(0, 0, 0, 0.28);
}

.profile-image-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.24), transparent 14rem),
    #101010;
}

.profile-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: var(--profile-image-position, center center);
}

.profile-placeholder {
  display: grid;
  width: 100%;
  height: 100%;
  place-items: center;
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.28), transparent 14rem),
    linear-gradient(135deg, #000000, #1a1a1a);
}

.profile-placeholder span {
  display: grid;
  width: 84px;
  height: 84px;
  place-items: center;
  border-radius: 50%;
  background: var(--color-gold);
  color: #000000;
  font-size: 2.5rem;
  font-weight: 950;
}

.profile-card-main {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 1.35rem;
}

.profile-card-main h3 {
  margin-top: 0;
}

.profile-bio {
  color: var(--color-muted);
}

.profile-extra {
  color: var(--color-muted);
}

.profile-extra strong {
  display: block;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}

.profile-extra p {
  margin: 0 0 0.85rem;
}

.profile-extra p:last-child {
  margin-bottom: 0;
}

.profile-extra-markdown p:first-child {
  margin-top: 0;
}

.profile-extra-markdown p:last-child {
  margin-bottom: 0;
}

/* Desktop: hover/focus expansion */
.profile-extra-desktop {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  margin-top: 0;
  transition:
    max-height 280ms ease,
    opacity 220ms ease,
    margin-top 220ms ease;
}

.committee-profile-card:hover .profile-extra-desktop,
.committee-profile-card:focus-within .profile-extra-desktop {
  max-height: 560px;
  opacity: 1;
  margin-top: 1rem;
}

/* Mobile/touch: tap to expand */
.profile-details {
  display: none;
  margin-top: auto;
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
}

.profile-details summary {
  cursor: pointer;
  color: var(--color-gold);
  font-weight: 850;
  list-style: none;
}

.profile-details summary::-webkit-details-marker {
  display: none;
}

.profile-details summary::after {
  content: " +";
}

.profile-details[open] summary::after {
  content: " −";
}

.profile-extra-mobile {
  margin-top: 1rem;
}

[data-theme="light"] .profile-placeholder {
  background:
    radial-gradient(circle at top right, rgba(247, 211, 93, 0.36), transparent 14rem),
    #ffffff;
}

[data-theme="light"] .profile-bio,
[data-theme="light"] .profile-extra {
  color: #3f3f3f;
}

[data-theme="light"] .profile-extra strong {
  color: #000000;
}

@media (max-width: 820px), (hover: none) {
  .committee-grid {
    grid-template-columns: 1fr !important;
  }

  .committee-profile-card:hover {
    transform: none;
  }

  .profile-extra-desktop {
    display: none;
  }

  .profile-details {
    display: block;
  }

  .profile-card-main {
    padding: 1.1rem;
  }
}

/* Make generic card sections work clearly as add/remove boxes */
.section-cards .content-card {
  min-height: 100%;
}

.section-cards .card-grid {
  align-items: stretch;
}

.section-cards .content-card-body {
  display: flex;
  min-height: 100%;
  flex-direction: column;
}

.section-cards .content-card-body .text-link {
  margin-top: auto;
}
"""
    css_path.write_text(css)
    print("Appended committee card CSS")
else:
    print("Committee card CSS already present")


# ============================================================
# 3. Patch admin/config.yml safely, not by replacing the whole file
# ============================================================

config_path = Path("admin/config.yml")
config = config_path.read_text()

# Make secondary CTA optional anywhere it appears.
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

# Rename Cards label to make it clearer in CMS.
config = config.replace(
    """- name: "cards"
                label: "Cards\"""",
    """- name: "cards"
                label: "Add/remove boxes\""""
)

config = config.replace(
    """- name: cards
                label: Cards""",
    """- name: cards
                label: Add/remove boxes"""
)

# Add committee member fields if they are not already present.
if "Optional questions" not in config:
    old_block = """                      - { label: Name, name: name, widget: string }
                      - { label: Role, name: role, widget: string, required: false }
                      - { label: Bio, name: bio, widget: text, required: false }
                      - { label: Email, name: email, widget: string, required: false }"""

    new_block = """                      - { label: Photo, name: image, widget: image, required: false }
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
                      - { label: Extra details, name: extra_details, widget: markdown, required: false }"""

    if old_block in config:
        config = config.replace(old_block, new_block, 1)
        print("Patched committee member fields in admin/config.yml")
    else:
        print("WARNING: Could not find old committee member block in admin/config.yml")
else:
    print("Committee optional questions already present in admin/config.yml")

config_path.write_text(config)


# ============================================================
# 4. Clean existing committee.yml from old favourite_place fields
#    Do not remove any actual people; just leave future generic questions.
# ============================================================

committee_path = Path("_data/content/committee.yml")
if committee_path.exists():
    text = committee_path.read_text()

    # Leave old fields alone if they have data; only remove empty placeholders.
    text = text.replace("        favourite_place:\n", "")
    text = text.replace("        favourite_place_description:\n", "")
    text = text.replace("        extra_details:\n        image:\n", "        image:\n        extra_details:\n")

    committee_path.write_text(text)
    print("Tidied committee.yml empty favourite_place placeholders if present")

print("Patch complete")
