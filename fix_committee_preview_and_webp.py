from pathlib import Path

ROOT = Path(".")

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)

# ---------------------------------------------------------------------
# 1. Fix admin/index.html to load Decap + committee preview JS
# ---------------------------------------------------------------------

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

# ---------------------------------------------------------------------
# 2. Preview CSS
# ---------------------------------------------------------------------

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

# ---------------------------------------------------------------------
# 3. Preview JS with robust asset URL resolution
# ---------------------------------------------------------------------

write("admin/committee-preview.js", """(function () {
  CMS.registerPreviewStyle("./committee-preview.css");

  function siteBasePath() {
    // Works for:
    // /uostriathlon/admin/
    // /uostriathlon/admin/index.html
    // /admin/
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

        // Try Decap's preview asset resolver first.
        try {
          var asset = getAsset(path);
          if (asset) {
            var resolved = asset.toString ? asset.toString() : String(asset);
            if (resolved && resolved !== path) {
              return resolved;
            }
          }
        } catch (e) {}

        // Absolute external URL.
        if (/^https?:\\/\\//i.test(path) || path.indexOf("blob:") === 0 || path.indexOf("data:") === 0) {
          return path;
        }

        // GitHub Pages base path fix.
        // Decap stores /assets/... but the site is /uostriathlon/assets/...
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
          "Use Crop horizontal, Crop vertical and Crop zoom in the editor. The yellow square shows the website frame. If no image is selected, no website image will render."
        ),
        h("div", { className: "cms-preview-grid" },
          members.map(function (member, index) {
            var rawImage = cleanPath(member.image);
            var img = assetUrl(rawImage);
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
                    ? h("img", {
                        src: img,
                        alt: member.name || "",
                        onError: function (event) {
                          console.warn("Committee preview image failed:", img);
                          event.currentTarget.style.display = "none";
                        }
                      })
                    : h("div", { className: "cms-no-image" }, "No image selected")
                ),
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

# ---------------------------------------------------------------------
# 4. Ensure frontend committee include doesn't render an image if empty
# ---------------------------------------------------------------------

committee_path = ROOT / "_includes/committee.html"
if committee_path.exists():
    committee = committee_path.read_text()

    # Make the if check robust against empty strings.
    committee = committee.replace("{% if member.image %}", "{% if member.image and member.image != \"\" %}")

    # If any old broken image-path-only output remains, replace with actual img.
    old = """{{ member.image | relative_url }}"""
    if old in committee and "class=\"committee-crop-image\"" not in committee:
        committee = committee.replace(
            old,
            """{{ member.image | relative_url }}"""
        )

    committee_path.write_text(committee)

# ---------------------------------------------------------------------
# 5. Ensure workflow and optimiser exist
# ---------------------------------------------------------------------

write(".github/workflows/optimise-committee-images.yml", """name: Optimise committee images

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

      - name: Optimise committee images
        run: python scripts/optimise_committee_images.py

      - name: Commit optimised images
        run: |
          if [[ -n "$(git status --porcelain)" ]]; then
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add assets/images/committee _data/content/committee.yml
            git commit -m "Optimise committee images"
            git push
          else
            echo "No image optimisation changes."
          fi
""")

write("scripts/optimise_committee_images.py", """from pathlib import Path
import re
import yaml
from PIL import Image, ImageOps

ROOT = Path(".")
committee_file = ROOT / "_data/content/committee.yml"
output_dir = ROOT / "assets/images/committee/profiles"
output_dir.mkdir(parents=True, exist_ok=True)

def slugify(value):
    value = value.lower()
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
        image_ref = member.get("image")
        if not image_ref:
            continue

        image_path = ROOT / normalise_ref(image_ref)
        if not image_path.exists():
            print(f"Skipping missing image: {image_ref}")
            continue

        if "/assets/images/committee/profiles/" in image_ref:
            continue

        name = member.get("name") or image_path.stem
        role = member.get("role") or ""
        filename = slugify(f"{name}-{role}") + ".webp"
        output_path = output_dir / filename
        public_ref = "/" + str(output_path).replace("\\\\", "/")

        try:
            with Image.open(image_path) as img:
                processed = crop_square(
                    img,
                    member.get("crop_x", 50),
                    member.get("crop_y", 50),
                    member.get("crop_zoom", 100),
                )
                processed.save(output_path, "WEBP", quality=82, method=6)
        except Exception as exc:
            print(f"Could not process {image_ref}: {exc}")
            continue

        member["image"] = public_ref
        member["crop_x"] = 50
        member["crop_y"] = 50
        member["crop_zoom"] = 100
        changed = True

if changed:
    committee_file.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    print("Updated committee.yml with optimised WebP references")
else:
    print("No committee.yml reference changes needed")
""")

print("Fixed committee CMS preview image resolution and ensured WebP optimiser exists.")
