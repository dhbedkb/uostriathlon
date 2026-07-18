from pathlib import Path

# ------------------------------------------------------------
# 1. Fix / replace committee include:
#    - uploaded images render as actual images
#    - automatic square crop
#    - optional image positioning
#    - expandable details
#    - optional arbitrary questions
# ------------------------------------------------------------

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
                <div class="profile-extra profile-extra-desktop" aria-hidden="true">
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

# ------------------------------------------------------------
# 2. Add / replace CSS for committee cards and CMS-friendly boxes
# ------------------------------------------------------------

css_path = Path("assets/css/main.css")
css = css_path.read_text() if css_path.exists() else ""

marker = "/* FINAL: CMS modular committee cards and expandable boxes */"

if marker not in css:
    css += """

/* FINAL: CMS modular committee cards and expandable boxes */

/* Committee grid */
.committee-grid {
  align-items: stretch;
}

/* Committee profile card */
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

/* Uploaded member photos */
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

/* Placeholder if no image uploaded */
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

/* Desktop expandable content */
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

/* Desktop: expand on hover/focus */
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

/* Mobile/touch: tap-to-expand details */
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

/* Light mode fixes */
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

/* Mobile behaviour */
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

/* Make generic card sections clearly useful as add/remove boxes from CMS */
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

# ------------------------------------------------------------
# 3. Rewrite Decap CMS config to:
#    - allow add/remove/reorder sections
#    - make CTA secondary button optional
#    - add committee images
#    - add arbitrary optional questions per committee member
#    - keep Cards section as flexible add/remove boxes
# ------------------------------------------------------------

Path("admin/config.yml").write_text("""backend:
  name: github
  repo: dhbedkb/uostriathlon
  branch: main
  base_url: https://uostriathlon-cms-auth.barnabytri.workers.dev
  auth_endpoint: auth

media_folder: "assets/images/uploads"
public_folder: "/assets/images/uploads"
publish_mode: simple
site_url: https://dhbedkb.github.io/uostriathlon/

collections:
  - name: pages
    label: Pages
    files:
      - name: home
        label: Home
        file: _data/content/home.yml
        fields: &page_fields
          - label: Title
            name: title
            widget: string

          - label: Description
            name: description
            widget: text
            required: false

          - label: Sections
            name: sections
            widget: list
            summary: "{{fields.type}} — {{fields.title}}"
            typeKey: type
            types:
              - name: hero
                label: Hero
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - { label: Body, name: body, widget: text, required: false }
                  - { label: Background image, name: background_image, widget: image, required: false }
                  - label: Primary button
                    name: primary_button
                    widget: object
                    required: false
                    fields:
                      - { label: Label, name: label, widget: string, required: false }
                      - { label: URL, name: url, widget: string, required: false }
                  - label: Secondary button
                    name: secondary_button
                    widget: object
                    required: false
                    fields:
                      - { label: Label, name: label, widget: string, required: false }
                      - { label: URL, name: url, widget: string, required: false }

              - name: text
                label: Text block
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - { label: Body, name: body, widget: markdown, required: false }

              - name: stats
                label: Stats
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Items
                    name: items
                    widget: list
                    fields:
                      - { label: Number, name: number, widget: string, required: false }
                      - { label: Label, name: label, widget: string, required: false }

              - name: cards
                label: Add/remove boxes
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Boxes
                    name: cards
                    widget: list
                    summary: "{{fields.title}}"
                    fields:
                      - { label: Title, name: title, widget: string, required: false }
                      - { label: Label, name: label, widget: string, required: false }
                      - { label: Description, name: description, widget: text, required: false }
                      - { label: Image, name: image, widget: image, required: false }
                      - { label: URL, name: url, widget: string, required: false }
                      - { label: Schedule, name: schedule, widget: string, required: false }
                      - { label: Location, name: location, widget: string, required: false }

              - name: gallery
                label: Gallery
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Images
                    name: images
                    widget: list
                    summary: "{{fields.caption}}"
                    fields:
                      - { label: Image, name: src, widget: image, required: false }
                      - { label: Alt text, name: alt, widget: string, required: false }
                      - { label: Caption, name: caption, widget: string, required: false }

              - name: events
                label: Events list
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Items
                    name: items
                    widget: list
                    summary: "{{fields.title}}"
                    fields:
                      - { label: Title, name: title, widget: string, required: false }
                      - { label: Date, name: date, widget: string, required: false }
                      - { label: Location, name: location, widget: string, required: false }
                      - { label: Type, name: type, widget: string, required: false }
                      - { label: Description, name: description, widget: text, required: false }
                      - { label: URL, name: url, widget: string, required: false }

              - name: committee
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

              - name: sponsors
                label: Sponsors
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Sponsors
                    name: sponsors
                    widget: list
                    summary: "{{fields.name}}"
                    fields:
                      - { label: Name, name: name, widget: string, required: false }
                      - { label: Description, name: description, widget: text, required: false }
                      - { label: URL, name: url, widget: string, required: false }

              - name: timeline
                label: Timeline
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Items
                    name: items
                    widget: list
                    summary: "{{fields.title}}"
                    fields:
                      - { label: Title, name: title, widget: string, required: false }
                      - { label: Description, name: description, widget: text, required: false }

              - name: faq
                label: FAQ
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Items
                    name: items
                    widget: list
                    summary: "{{fields.question}}"
                    fields:
                      - { label: Question, name: question, widget: string, required: false }
                      - { label: Answer, name: answer, widget: markdown, required: false }

              - name: cta
                label: Call to action
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Body, name: body, widget: text, required: false }
                  - label: Primary button
                    name: primary_button
                    widget: object
                    required: false
                    fields:
                      - { label: Label, name: label, widget: string, required: false }
                      - { label: URL, name: url, widget: string, required: false }
                  - label: Secondary button
                    name: secondary_button
                    widget: object
                    required: false
                    fields:
                      - { label: Label, name: label, widget: string, required: false }
                      - { label: URL, name: url, widget: string, required: false }

              - name: embed
                label: Embed or widget
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Provider, name: provider, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - { label: Layout, name: layout, widget: string, required: false }
                  - label: Embeds
                    name: embeds
                    widget: list
                    required: false
                    summary: "{{fields.title}}"
                    fields:
                      - { label: Provider, name: provider, widget: string, required: false }
                      - { label: Title, name: title, widget: string, required: false }
                      - { label: Description, name: description, widget: text, required: false }
                      - { label: URL, name: url, widget: string, required: false }
                      - { label: Button label, name: button_label, widget: string, required: false }
                      - { label: Embed HTML, name: embed_html, widget: text, required: false }

              - name: socials
                label: Social links
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }
                  - { label: Subtitle, name: subtitle, widget: string, required: false }
                  - label: Layout
                    name: layout
                    widget: select
                    required: false
                    options:
                      - logos
                      - cards
                  - label: Items
                    name: items
                    widget: list
                    summary: "{{fields.platform}}"
                    fields:
                      - { label: Platform, name: platform, widget: string, required: false }
                      - { label: Icon, name: icon, widget: image, required: false }
                      - { label: Title, name: title, widget: string, required: false }
                      - { label: Description, name: description, widget: text, required: false }
                      - { label: URL, name: url, widget: string, required: false }
                      - { label: Button, name: button, widget: string, required: false }

              - name: relay-bar
                label: Relay bar
                fields:
                  - { label: ID, name: id, widget: string, required: false }
                  - { label: Eyebrow, name: eyebrow, widget: string, required: false }
                  - { label: Title, name: title, widget: string, required: false }

      - name: training
        label: Training
        file: _data/content/training.yml
        fields: *page_fields

      - name: events
        label: Events
        file: _data/content/events.yml
        fields: *page_fields

      - name: races
        label: Races
        file: _data/content/races.yml
        fields: *page_fields

      - name: socials
        label: Socials
        file: _data/content/socials.yml
        fields: *page_fields

      - name: committee
        label: Committee
        file: _data/content/committee.yml
        fields: *page_fields

      - name: gallery
        label: Gallery
        file: _data/content/gallery.yml
        fields: *page_fields

      - name: about
        label: About
        file: _data/content/about.yml
        fields: *page_fields

      - name: join
        label: Join
        file: _data/content/join.yml
        fields: *page_fields

      - name: members
        label: Members
        file: _data/content/members.yml
        fields: *page_fields

      - name: news
        label: News
        file: _data/content/news.yml
        fields: *page_fields

  - name: settings
    label: Site settings
    files:
      - name: settings
        label: Brand and settings
        file: _data/settings.yml
        fields:
          - label: Brand
            name: brand
            widget: object
            fields:
              - { label: Name, name: name, widget: string, required: false }
              - { label: Short name, name: short_name, widget: string, required: false }
              - { label: Tagline, name: tagline, widget: string, required: false }
              - { label: Email, name: email, widget: string, required: false }
              - { label: Logo, name: logo, widget: image, required: false }

          - label: Theme
            name: theme
            widget: object
            required: false
            fields:
              - { label: Default, name: default, widget: string, required: false }

          - label: Links
            name: links
            widget: object
            required: false
            fields:
              - { label: Training calendar, name: training_calendar, widget: string, required: false }
              - { label: Events calendar, name: events_calendar, widget: string, required: false }
              - { label: Instagram, name: instagram, widget: string, required: false }
              - { label: Strava, name: strava, widget: string, required: false }
              - { label: Facebook, name: facebook, widget: string, required: false }
              - { label: Membership, name: membership, widget: string, required: false }

      - name: navigation
        label: Navigation
        file: _data/navigation.yml
        fields:
          - label: Items
            name: items
            widget: list
            fields:
              - { label: Label, name: label, widget: string, required: false }
              - { label: URL, name: url, widget: string, required: false }

          - label: Join button
            name: cta
            widget: object
            required: false
            fields:
              - { label: Label, name: label, widget: string, required: false }
              - { label: URL, name: url, widget: string, required: false }

      - name: socials_list
        label: Footer social links
        file: _data/socials.yml
        fields:
          - label: Items
            name: items
            widget: list
            fields:
              - { label: Platform, name: platform, widget: string, required: false }
              - { label: Label, name: label, widget: string, required: false }
              - { label: URL, name: url, widget: string, required: false }
""")

print("Implemented modular CMS sections, optional CTA secondary button, committee images, and expandable committee cards.")
