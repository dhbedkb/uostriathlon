from pathlib import Path

ROOT = Path(".")

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)

# ------------------------------------------------------------
# 1. Fix admin/index.html properly
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
# 2. Fix committee preview URL handling
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

  function stripKnownBase(path, basePath) {
    if (!path) return "";
    if (basePath && path.indexOf(basePath + "/") === 0) {
      return path.slice(basePath.length);
    }
    return path;
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

        // If Decap stores /uostriathlon/assets/..., normalise to /assets/...
        var noBasePath = stripKnownBase(path, basePath);

        // Try Decap's asset resolver first using both possible forms.
        try {
          var asset = getAsset(noBasePath);
          if (asset) {
            var resolved = asset.toString ? asset.toString() : String(asset);
            if (resolved && resolved !== noBasePath) {
              return resolved;
            }
          }
        } catch (e) {}

        try {
          var asset2 = getAsset(path);
          if (asset2) {
            var resolved2 = asset2.toString ? asset2.toString() : String(asset2);
            if (resolved2 && resolved2 !== path) {
              return resolved2;
            }
          }
        } catch (e) {}

        // Browser blob/data/external URL.
        if (
          /^https?:\\/\\//i.test(path) ||
          path.indexOf("blob:") === 0 ||
          path.indexOf("data:") === 0
        ) {
          return path;
        }

        // If already includes the site base, use as-is.
        if (basePath && path.indexOf(basePath + "/") === 0) {
          return path;
        }

        // If root-relative asset path, add site base.
        if (noBasePath.charAt(0) === "/") {
          return basePath + noBasePath;
        }

        return basePath + "/" + noBasePath.replace(/^\\.\\//, "");
      }

      return h("main", { className: "cms-preview-wrap" },
        h("div", { className: "cms-preview-eyebrow" }, committee.eyebrow || "Team"),
        h("h1", { className: "cms-preview-title" }, committee.title || "Current committee."),
        h("p", { className: "cms-preview-subtitle" }, committee.subtitle || ""),
        h("p", { className: "cms-crop-help" },
          "Preview uses Source photo immediately. The yellow square shows the website crop frame. Remove Source photo to remove the image."
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
                  ? h("div", { className: "cms-source-note" }, "Source: " + previewSource)
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
# 3. Fix frontend committee rendering
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

          {% if display_image %}
            {% assign display_image_clean = display_image | remove_first: site.baseurl %}
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
                    {{ display_image_clean | relative_url }}
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
                    {{ member.email }}Email →</a>
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
# 4. Fix config public_folder values for local/GitHub Pages image widget previews
# ------------------------------------------------------------

config_path = ROOT / "admin/config.yml"
config = config_path.read_text()

config = config.replace(
    "public_folder: /assets/images/committee/raw",
    "public_folder: /uostriathlon/assets/images/committee/raw"
)

config = config.replace(
    'public_folder: "/assets/images/uploads"',
    'public_folder: "/uostriathlon/assets/images/uploads"'
)

config_path.write_text(config)

# ------------------------------------------------------------
# 5. Normalize existing committee data enough to keep both editor and frontend happy
# ------------------------------------------------------------

committee_path = ROOT / "_data/content/committee.yml"

if committee_path.exists():
    text = committee_path.read_text()

    # If old image field exists and image_raw/profile do not, keep compatibility.
    # Do not overwrite existing image_raw or image_profile.
    if "image_raw:" not in text and "image:" in text:
        text = text.replace(
            "image: /assets/images/committee/profiles/barnaby-read-secretary.webp",
            "image_raw: /uostriathlon/assets/images/committee/raw/img_9541.jpg\n    image_profile: /assets/images/committee/profiles/barnaby-read-secretary.webp"
        )

    committee_path.write_text(text)

print("Fixed committee preview/frontend image path handling.")
