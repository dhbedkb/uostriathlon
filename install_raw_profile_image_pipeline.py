from pathlib import Path
import subprocess
import sys

ROOT = Path(".")

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)

def append_once(path, marker, content):
    p = ROOT / path
    existing = p.read_text() if p.exists() else ""
    if marker not in existing:
        p.write_text(existing + "\n\n" + content)

# ------------------------------------------------------------
# 1. Admin index
# ------------------------------------------------------------

write("admin/index.html", """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Content Manager · Sheffield Triathlon</title>
</head>
<body>
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
  ./committee-preview.jsscript>
</body>
</html>
""")

# ------------------------------------------------------------
# 2. CMS preview stylesheet
# ------------------------------------------------------------

write("admin/committee-preview.css", """body {
  margin: 0;
  padding: 24px;
  background: #0b0b0b;
  color: #ffffff;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.cms-preview-wrap {
  max-width: 1080px;
  margin: 0 auto;
}

.cms-preview-eyebrow {
  color: #F7D35D;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.cms-preview-title {
  margin: 8px 0 10px;
  font-size: clamp(32px, 6vw, 64px);
  line-height: 0.95;
  font-weight: 950;
}

.cms-preview-subtitle,
.cms-crop-help {
  color: #cfcfcf;
}

.cms-crop-help {
  margin-bottom: 28px;
  font-size: 14px;
}

.cms-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

@media (min-width: 950px) {
  .cms-preview-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.cms-card {
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 18px;
  overflow: hidden;
  background:
    radial-gradient(circle at top right, rgba(247,211,93,0.13), transparent 180px),
    #151515;
}

.cms-card-head {
  min-height: 76px;
  padding: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.12);
}

.cms-card-name {
  display: block;
  font-weight: 950;
  font-size: 24px;
  line-height: 1.02;
}

.cms-card-role {
  display: block;
  margin-top: 6px;
  color: #F7D35D;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.cms-card-body {
  padding: 16px;
}

.cms-image-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 14px;
  background: #070707;
  outline: 2px solid rgba(247,211,93,0.9);
  outline-offset: -2px;
  margin-bottom: 12px;
}

.cms-image-frame::before {
  content: "Website crop frame";
  position: absolute;
  z-index: 2;
  top: 8px;
  left: 8px;
  padding: 4px 7px;
  border-radius: 999px;
  background: rgba(0,0,0,0.74);
  color: #F7D35D;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.cms-image-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: var(--crop-x, 50%) var(--crop-y, 50%);
  transform: scale(var(--crop-zoom, 1));
  transform-origin: var(--crop-x, 50%) var(--crop-y, 50%);
  display: block;
}

.cms-no-image {
  display: grid;
  place-items: center;
  width: 100%;
  height: 100%;
  color: #F7D35D;
  font-weight: 900;
  text-align: center;
  padding: 14px;
  box-sizing: border-box;
}

.cms-source-note {
  color: #9e9e9e;
  font-size: 12px;
  margin-top: -4px;
  margin-bottom: 12px;
  word-break: break-word;
}

.cms-card p {
  color: #d0d0d0;
  margin: 0 0 10px;
}

.cms-question {
  margin-top: 12px;
}

.cms-question strong {
  display: block;
  color: #ffffff;
  margin-bottom: 3px;
}
""")

# ------------------------------------------------------------
# 3. CMS preview JavaScript
# ------------------------------------------------------------

write("admin/committee-preview.js", """(function () {
  CMS.registerPreviewStyle("./committee-preview.css");

  function siteBasePath() {
    var path = window.location.pathname || "/";
    var adminIndex = path.indexOf("/admin");
    if (adminIndex > 0) {
      return path.slice(0, adminIndex);
    }
    return "";
  }

  function cleanPath(value) {
    if (!value) return "";
    return String(value).trim();
  }

  var CommitteePreview = createClass({
    render: function () {
      var entry = this.props.entry;
      var getAsset = this.props.getAsset;

      var data = entry.getIn(["data"]).toJS();
      var sections = data.sections || [];
      var committee = sections.find(function (section) {
        return section.type === "committee";
      }) || {};

      var members = committee.members || [];
      var basePath = siteBasePath();

      function assetUrl(path) {
        path = cleanPath(path);

        if (!path) {
          return "";
        }

        try {
          var asset = getAsset(path);
          if (asset) {
            var resolved = asset.toString ? asset.toString() : String(asset);
            if (resolved && resolved !== path) {
              return resolved;
            }
          }
        } catch (e) {}

        if (/^https?:\\/\\//i.test(path) || path.indexOf("blob:") === 0 || path.indexOf("data:") === 0) {
          return path;
        }

        if (path.charAt(0) === "/") {
          return basePath + path;
        }

        return basePath + "/" + path.replace(/^\\.\\//, "");
      }

      return h("main", { className: "cms-preview-wrap" },
        h("div", { className: "cms-preview-eyebrow" }, committee.eyebrow || "Team"),
        h("h1", { className: "cms-preview-title" }, committee.title || "Current committee."),
        h("p", { className: "cms-preview-subtitle" }, committee.subtitle || ""),
        h("p", { className: "cms-crop-help" },
          "Preview uses image_raw immediately. GitHub Actions later creates image_profile as a cropped 900x900 WebP. Remove image_raw to remove the image from the website."
        ),
        h("div", { className: "cms-preview-grid" },
          members.map(function (member, index) {
            var rawImage = cleanPath(member.image_raw || member.image || "");
            var profileImage = cleanPath(member.image_profile || "");
            var previewSource = rawImage || profileImage;
            var img = assetUrl(previewSource);

            var cropX = member.crop_x || 50;
            var cropY = member.crop_y || 50;
            var cropZoom = (member.crop_zoom || 100) / 100;

            return h("article", { className: "cms-card", key: index },
              h("div", { className: "cms-card-head" },
                h("span", { className: "cms-card-name" }, member.name || "Committee member"),
                member.role ? h("span", { className: "cms-card-role" }, member.role) : null
              ),
              h("div", { className: "cms-card-body" },
                h("div", {
                  className: "cms-image-frame",
                  style: {
                    "--crop-x": cropX + "%",
                    "--crop-y": cropY + "%",
                    "--crop-zoom": cropZoom
                  }
                },
                  img
                    ? h("img", { src: img, alt: member.name || "" })
                    : h("div", { className: "cms-no-image" }, "No image selected")
                ),
                previewSource
                  ? h("div", { className: "cms-source-note" }, "Preview source: " + previewSource)
                  : null,
                member.bio ? h("p", null, member.bio) : null,
                member.questions && member.questions.length
                  ? member.questions.map(function (item, qIndex) {
                      return h("div", { className: "cms-question", key: qIndex },
                        item.question ? h("strong", null, item.question) : null,
                        item.answer ? h("p", null, item.answer) : null
                      );
                    })
                  : null
              )
            );
          })
        )
      );
    }
  });

  CMS.registerPreviewTemplate("committee", CommitteePreview);
})();
""")

# ------------------------------------------------------------
# 4. Frontend committee include
# ------------------------------------------------------------

write("_includes/committee.html", """<section id="{{ include.section_id }}" class="section section-committee" data-section-type="committee">
  <div class="container">
    {% include section-heading.html
      eyebrow=include.section.eyebrow
      title=include.section.title
      subtitle=include.section.subtitle
      alignment=include.section.alignment
    %}

    {% if include.section.members %}
      <div class="committee-grid committee-crop-grid">
        {% for member in include.section.members %}
          {% assign raw_image = member.image_raw | default: member.image %}
          {% assign profile_image = member.image_profile %}
          {% assign display_image = nil %}

          {% if raw_image and raw_image != "" %}
            {% if profile_image and profile_image != "" %}
              {% assign display_image = profile_image %}
              {% assign crop_x = 50 %}
              {% assign crop_y = 50 %}
              {% assign crop_zoom = 100 %}
            {% else %}
              {% assign display_image = raw_image %}
              {% assign crop_x = member.crop_x | default: 50 %}
              {% assign crop_y = member.crop_y | default: 50 %}
              {% assign crop_zoom = member.crop_zoom | default: 100 %}
            {% endif %}
          {% endif %}

          {% assign has_extra = false %}
          {% if display_image or member.bio or member.email or member.questions or member.extra_details %}
            {% assign has_extra = true %}
          {% endif %}

          <details class="committee-crop-card reveal-card">
            <summary class="committee-crop-summary">
              <span class="committee-crop-title">
                <span class="committee-crop-name">{{ member.name | default: "Committee member" }}</span>
                {% if member.role %}
                  <span class="committee-crop-role">{{ member.role }}</span>
                {% endif %}
              </span>

              <span class="committee-crop-toggle" aria-hidden="true"></span>
            </summary>

            {% if has_extra %}
              <div class="committee-crop-expanded">
                {% if display_image %}
                  <div
                    class="committee-crop-image-frame"
                    style="--crop-x: {{ crop_x }}%; --crop-y: {{ crop_y }}%; --crop-zoom: {{ crop_zoom | divided_by: 100.0 }};"
                  >
                    {{ display_image | relative_url }}
                  </div>
                {% endif %}

                {% if member.bio %}
                  <p class="committee-crop-bio">{{ member.bio }}</p>
                {% endif %}

                {% if member.questions %}
                  <div class="committee-crop-questions">
                    {% for item in member.questions %}
                      {% if item.question or item.answer %}
                        <div class="committee-crop-question">
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
                  <div class="committee-crop-extra">
                    {{ member.extra_details | markdownify }}
                  </div>
                {% endif %}

                {% if member.email %}
                  <p class="committee-crop-email">
                    {{ member.email }}Email -></a>
                  </p>
                {% endif %}
              </div>
            {% endif %}
          </details>
        {% endfor %}
      </div>
    {% endif %}
  </div>
</section>
""")

# ------------------------------------------------------------
# 5. Frontend CSS
# ------------------------------------------------------------

append_once("assets/css/main.css", "/* FINAL RAW PROFILE IMAGE PIPELINE: committee cards */", """
/* FINAL RAW PROFILE IMAGE PIPELINE: committee cards */

.section-committee .committee-crop-grid {
  display: grid !important;
  gap: 1rem !important;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)) !important;
  align-items: start !important;
  max-width: 1120px;
  margin-inline: auto;
}

@media (min-width: 1050px) {
  .section-committee .committee-crop-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
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
}

.section-committee .committee-crop-card[open] {
  border-color: rgba(247, 211, 93, 0.55);
}

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

.section-committee .committee-crop-expanded {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box;
  border-top: 1px solid var(--color-border);
  padding: 1rem 1.15rem 1.15rem !important;
}

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

.section-committee .committee-crop-image-frame::after {
  content: "";
  position: absolute;
  inset: 0;
  border: 2px solid rgba(247, 211, 93, 0.7);
  border-radius: inherit;
  pointer-events: none;
}

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

.section-committee .committee-crop-bio,
.section-committee .committee-crop-question p,
.section-committee .committee-crop-extra {
  color: var(--color-muted);
}

.section-committee .committee-crop-question strong {
  display: block;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}

@media (max-width: 760px) {
  .section-committee .committee-crop-grid {
    grid-template-columns: 1fr !important;
  }
}
""")

# ------------------------------------------------------------
# 6. Patch admin/config.yml committee block
# ------------------------------------------------------------

config_path = ROOT / "admin/config.yml"
config = config_path.read_text()

start_marker = "              - name: committee"
end_marker = "              - name: sponsors"

start = config.find(start_marker)
end = config.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not find committee/sponsors markers in admin/config.yml")

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
                      - label: Source photo
                        name: image_raw
                        widget: image
                        required: false
                        choose_url: false
                        media_folder: /assets/images/committee/raw
                        public_folder: /assets/images/committee/raw
                        hint: "Upload the original photo here. The preview uses this immediately."
                      - { label: Optimised profile photo, name: image_profile, widget: string, required: false, hint: "Generated automatically after publish. Do not edit manually." }
                      - { label: Crop horizontal focus %, name: crop_x, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false, hint: "0 = left, 50 = centre, 100 = right. Watch the preview pane." }
                      - { label: Crop vertical focus %, name: crop_y, widget: number, default: 50, min: 0, max: 100, value_type: int, required: false, hint: "0 = top, 50 = centre, 100 = bottom. Watch the preview pane." }
                      - { label: Crop zoom %, name: crop_zoom, widget: number, default: 100, min: 100, max: 220, value_type: int, required: false, hint: "100 = normal. Increase to zoom into the face." }
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

config = config[:start] + new_block + config[end:]
config_path.write_text(config)

# ------------------------------------------------------------
# 7. Migration: old image -> image_raw or image_profile
# ------------------------------------------------------------

committee_file = ROOT / "_data/content/committee.yml"

if committee_file.exists():
    data = yaml.safe_load(committee_file.read_text())

    for section in data.get("sections", []):
        if section.get("type") != "committee":
            continue

        for member in section.get("members", []):
            old_image = member.get("image")

            if old_image and not member.get("image_raw") and not member.get("image_profile"):
                if "/assets/images/committee/profiles/" in str(old_image):
                    member["image_profile"] = old_image
                    member["image_raw"] = ""
                else:
                    member["image_raw"] = old_image
                    member["image_profile"] = ""

            if "image" in member:
                del member["image"]

    committee_file.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))

# ------------------------------------------------------------
# 8. Optimiser script
# ------------------------------------------------------------

write("scripts/optimise_site_images.py", """from pathlib import Path
import re
import yaml
from PIL import Image, ImageOps

ROOT = Path(".")
committee_file = ROOT / "_data/content/committee.yml"
output_dir = ROOT / "assets/images/committee/profiles"
output_dir.mkdir(parents=True, exist_ok=True)

def slugify(value):
    value = str(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "committee-member"

def normalise_ref(path):
    if not path:
        return None
    return str(path).lstrip("/")

def crop_square(img, crop_x=50, crop_y=50, crop_zoom=100):
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size

    zoom = max(float(crop_zoom or 100) / 100.0, 1.0)
    side = min(w, h) / zoom

    cx = w * (float(crop_x or 50) / 100.0)
    cy = h * (float(crop_y or 50) / 100.0)

    left = cx - side / 2
    top = cy - side / 2
    right = left + side
    bottom = top + side

    if left < 0:
        right -= left
        left = 0
    if top < 0:
        bottom -= top
        top = 0
    if right > w:
        left -= right - w
        right = w
    if bottom > h:
        top -= bottom - h
        bottom = h

    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    cropped = img.crop((int(left), int(top), int(right), int(bottom)))
    cropped = cropped.resize((900, 900), Image.Resampling.LANCZOS)
    return cropped

if not committee_file.exists():
    raise SystemExit("No committee.yml found")

data = yaml.safe_load(committee_file.read_text())
changed = False

for section in data.get("sections", []):
    if section.get("type") != "committee":
        continue

    for member in section.get("members", []):
        raw_ref = member.get("image_raw")

        if not raw_ref:
            if member.get("image_profile"):
                member["image_profile"] = ""
                changed = True
            continue

        raw_path = ROOT / normalise_ref(raw_ref)

        if not raw_path.exists():
            print(f"Skipping missing raw image: {raw_ref}")
            continue

        name = member.get("name") or raw_path.stem
        role = member.get("role") or ""
        filename = slugify(f"{name}-{role}") + ".webp"
        output_path = output_dir / filename
        public_ref = "/" + str(output_path).replace("\\\\", "/")

        try:
            with Image.open(raw_path) as img:
                processed = crop_square(
                    img,
                    member.get("crop_x", 50),
                    member.get("crop_y", 50),
                    member.get("crop_zoom", 100),
                )
                processed.save(output_path, "WEBP", quality=82, method=6)
        except Exception as exc:
            print(f"Could not process {raw_ref}: {exc}")
            continue

        if member.get("image_profile") != public_ref:
            member["image_profile"] = public_ref
            changed = True

if changed:
    committee_file.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    print("Updated committee.yml with optimised WebP profile references")
else:
    print("No committee profile image changes needed")
""")

# ------------------------------------------------------------
# 9. GitHub Action
# ------------------------------------------------------------

write(".github/workflows/optimise-site-images.yml", """name: Optimise site images

on:
  push:
    paths:
      - "assets/images/committee/raw/**"
      - "_data/content/committee.yml"

permissions:
  contents: write

jobs:
  optimise:
    if: github.actor != 'github-actions[bot]'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: python -m pip install pillow pyyaml

      - name: Optimise images
        run: python scripts/optimise_site_images.py

      - name: Commit optimised images
        run: |
          if [[ -n "$(git status --porcelain)" ]]; then
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add assets/images/committee/profiles _data/content/committee.yml
            git commit -m "Optimise committee profile images"
            git push
          else
            echo "No image optimisation changes."
          fi
""")

print("Installed raw/profile image architecture.")
