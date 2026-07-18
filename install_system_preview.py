from pathlib import Path

lt = chr(60)
gt = chr(62)

# ------------------------------------------------------------
# 1. Fix admin/index.html
# ------------------------------------------------------------

html = f"""<!doctype html>
{lt}html{gt}
{lt}head{gt}
  {lt}meta charset="utf-8"{gt}
  {lt}meta name="viewport" content="width=device-width, initial-scale=1"{gt}
  {lt}title{gt}Content Manager · Sheffield Triathlon{lt}/title{gt}
{lt}/head{gt}
{lt}body{gt}
  {lt}script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"{gt}{lt}/script{gt}
  {lt}script src="./committee-preview.js?v=system-preview-1"{gt}{lt}/script{gt}
{lt}/body{gt}
{lt}/html{gt}
"""

Path("admin/index.html").write_text(html)

# ------------------------------------------------------------
# 2. Replace preview CSS
# ------------------------------------------------------------

Path("admin/committee-preview.css").write_text("""body {
  margin: 0;
  padding: 24px;
  background: #0b0b0b;
  color: #ffffff;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.cms-page-preview {
  max-width: 1120px;
  margin: 0 auto;
}

.cms-section {
  margin-bottom: 28px;
  padding: 22px;
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 22px;
  background:
    radial-gradient(circle at top right, rgba(247,211,93,0.11), transparent 240px),
    #151515;
}

.cms-section-label {
  color: #F7D35D;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.cms-section-title {
  margin: 8px 0 8px;
  font-size: clamp(28px, 5vw, 58px);
  line-height: 0.95;
  font-weight: 950;
}

.cms-section-subtitle,
.cms-section-body,
.cms-muted {
  color: #cfcfcf;
}

.cms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin-top: 18px;
}

@media (min-width: 920px) {
  .cms-grid.cms-grid-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.cms-card {
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 18px;
  overflow: hidden;
  background: #101010;
}

.cms-card-head {
  padding: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.12);
}

.cms-card-name,
.cms-card-title {
  display: block;
  font-weight: 950;
  font-size: 22px;
  line-height: 1.05;
}

.cms-card-role,
.cms-card-label {
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

.cms-image-frame.cms-wide {
  aspect-ratio: 16 / 9;
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

.cms-question {
  margin-top: 12px;
}

.cms-question strong {
  display: block;
  color: #ffffff;
  margin-bottom: 3px;
}

.cms-faq-item,
.cms-timeline-item {
  border-top: 1px solid rgba(255,255,255,0.12);
  padding-top: 12px;
  margin-top: 12px;
}
""")

# ------------------------------------------------------------
# 3. Replace preview JS
# ------------------------------------------------------------

Path("admin/committee-preview.js").write_text(r'''(function () {
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

  function assetUrl(path, getAsset) {
    path = cleanPath(path);

    if (!path) return "";

    if (
      /^https?:\/\//i.test(path) ||
      path.indexOf("blob:") === 0 ||
      path.indexOf("data:") === 0
    ) {
      return path;
    }

    var basePath = siteBasePath();

    try {
      var asset = getAsset(path);
      if (asset) {
        var resolved = asset.toString ? asset.toString() : String(asset);
        if (resolved) return resolved;
      }
    } catch (e) {}

    if (basePath && path.indexOf(basePath + "/") === 0) {
      return path;
    }

    if (path.charAt(0) === "/") {
      return basePath + path;
    }

    return basePath + "/" + path.replace(/^\.\//, "");
  }

  function imageFrame(src, cropX, cropY, cropZoom, getAsset, wide) {
    var img = assetUrl(src, getAsset);
    var zoom = (cropZoom || 100) / 100;

    return h("div", {
      className: wide ? "cms-image-frame cms-wide" : "cms-image-frame",
      style: {
        "--crop-x": (cropX || 50) + "%",
        "--crop-y": (cropY || 50) + "%",
        "--crop-zoom": zoom
      }
    },
      img
        ? h("img", { src: img, alt: "" })
        : h("div", { className: "cms-no-image" }, "No image selected")
    );
  }

  function sectionHeading(section, fallbackType) {
    return [
      h("div", { className: "cms-section-label" }, section.eyebrow || fallbackType || section.type || "Section"),
      h("h2", { className: "cms-section-title" }, section.title || section.platform || section.type || "Untitled section"),
      section.subtitle ? h("p", { className: "cms-section-subtitle" }, section.subtitle) : null,
      section.body ? h("p", { className: "cms-section-body" }, section.body) : null
    ];
  }

  function renderHero(section, getAsset) {
    return h("section", { className: "cms-section" },
      sectionHeading(section, "Hero"),
      section.background_image
        ? imageFrame(
            section.background_image,
            section.background_crop_x,
            section.background_crop_y,
            section.background_crop_zoom,
            getAsset,
            true
          )
        : null
    );
  }

  function renderText(section) {
    return h("section", { className: "cms-section" },
      sectionHeading(section, "Text")
    );
  }

  function renderCards(section, getAsset) {
    var cards = section.cards || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "Cards / boxes"),
      h("div", { className: "cms-grid cms-grid-3" },
        cards.map(function (card, index) {
          return h("article", { className: "cms-card", key: index },
            card.image
              ? h("div", { className: "cms-card-body" },
                  imageFrame(card.image, card.crop_x, card.crop_y, card.crop_zoom, getAsset, false)
                )
              : null,
            h("div", { className: "cms-card-head" },
              h("span", { className: "cms-card-title" }, card.title || "Box"),
              card.label ? h("span", { className: "cms-card-label" }, card.label) : null
            ),
            h("div", { className: "cms-card-body" },
              card.description ? h("p", null, card.description) : null,
              card.location ? h("p", { className: "cms-muted" }, card.location) : null,
              card.schedule ? h("p", { className: "cms-muted" }, card.schedule) : null
            )
          );
        })
      )
    );
  }

  function renderGallery(section, getAsset) {
    var images = section.images || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "Gallery"),
      h("div", { className: "cms-grid cms-grid-3" },
        images.map(function (item, index) {
          return h("article", { className: "cms-card", key: index },
            h("div", { className: "cms-card-body" },
              imageFrame(item.src, item.crop_x, item.crop_y, item.crop_zoom, getAsset, false),
              item.caption ? h("p", null, item.caption) : null
            )
          );
        })
      )
    );
  }

  function renderCommittee(section, getAsset) {
    var members = section.members || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "Committee"),
      h("div", { className: "cms-grid cms-grid-3" },
        members.map(function (member, index) {
          var source = cleanPath(member.image_raw || "");

          return h("article", { className: "cms-card", key: index },
            h("div", { className: "cms-card-head" },
              h("span", { className: "cms-card-name" }, member.name || "Committee member"),
              member.role ? h("span", { className: "cms-card-role" }, member.role) : null
            ),
            h("div", { className: "cms-card-body" },
              imageFrame(source, member.crop_x, member.crop_y, member.crop_zoom, getAsset, false),
              source
                ? h("div", { className: "cms-source-note" }, "Source photo: " + source)
                : h("div", { className: "cms-source-note" }, "No Source photo selected"),
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

  function renderStats(section) {
    var items = section.items || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "Stats"),
      h("div", { className: "cms-grid" },
        items.map(function (item, index) {
          return h("article", { className: "cms-card", key: index },
            h("div", { className: "cms-card-head" },
              h("span", { className: "cms-card-name" }, item.number || ""),
              item.label ? h("span", { className: "cms-card-role" }, item.label) : null
            )
          );
        })
      )
    );
  }

  function renderTimeline(section) {
    var items = section.items || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "Timeline"),
      items.map(function (item, index) {
        return h("div", { className: "cms-timeline-item", key: index },
          h("strong", null, item.title || "Timeline item"),
          item.description ? h("p", null, item.description) : null
        );
      })
    );
  }

  function renderFAQ(section) {
    var items = section.items || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "FAQ"),
      items.map(function (item, index) {
        return h("div", { className: "cms-faq-item", key: index },
          h("strong", null, item.question || "Question"),
          item.answer ? h("p", null, item.answer) : null
        );
      })
    );
  }

  function renderSocials(section, getAsset) {
    var items = section.items || [];

    return h("section", { className: "cms-section" },
      sectionHeading(section, "Socials"),
      h("div", { className: "cms-grid" },
        items.map(function (item, index) {
          return h("article", { className: "cms-card", key: index },
            item.icon
              ? h("div", { className: "cms-card-body" },
                  imageFrame(item.icon, item.crop_x, item.crop_y, item.crop_zoom, getAsset, false)
                )
              : null,
            h("div", { className: "cms-card-head" },
              h("span", { className: "cms-card-title" }, item.platform || item.title || "Social link")
            )
          );
        })
      )
    );
  }

  function renderCTA(section) {
    return h("section", { className: "cms-section" },
      sectionHeading(section, "Call to action")
    );
  }

  function renderGeneric(section) {
    return h("section", { className: "cms-section" },
      sectionHeading(section, section.type || "Section")
    );
  }

  function renderSection(section, getAsset, index) {
    if (!section || !section.type) {
      return null;
    }

    switch (section.type) {
      case "hero":
        return h("div", { key: index }, renderHero(section, getAsset));
      case "text":
        return h("div", { key: index }, renderText(section));
      case "cards":
        return h("div", { key: index }, renderCards(section, getAsset));
      case "gallery":
        return h("div", { key: index }, renderGallery(section, getAsset));
      case "committee":
        return h("div", { key: index }, renderCommittee(section, getAsset));
      case "stats":
        return h("div", { key: index }, renderStats(section));
      case "timeline":
        return h("div", { key: index }, renderTimeline(section));
      case "faq":
        return h("div", { key: index }, renderFAQ(section));
      case "socials":
        return h("div", { key: index }, renderSocials(section, getAsset));
      case "cta":
        return h("div", { key: index }, renderCTA(section));
      default:
        return h("div", { key: index }, renderGeneric(section));
    }
  }

  var PagePreview = createClass({
    render: function () {
      var entry = this.props.entry;
      var getAsset = this.props.getAsset;
      var data = entry.getIn(["data"]).toJS();
      var sections = data.sections || [];

      return h("main", { className: "cms-page-preview" },
        h("section", { className: "cms-section" },
          h("div", { className: "cms-section-label" }, "Page"),
          h("h1", { className: "cms-section-title" }, data.title || "Untitled page"),
          data.description ? h("p", { className: "cms-section-subtitle" }, data.description) : null
        ),
        sections.map(function (section, index) {
          return renderSection(section, getAsset, index);
        })
      );
    }
  });

  [
    "home",
    "training",
    "events",
    "races",
    "socials",
    "committee",
    "gallery",
    "about",
    "join",
    "members",
    "news"
  ].forEach(function (name) {
    CMS.registerPreviewTemplate(name, PagePreview);
  });
})();
''')

print("Installed system-wide page section preview.")
