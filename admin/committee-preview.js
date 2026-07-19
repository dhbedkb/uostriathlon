(function () {
  CMS.registerPreviewStyle("./committee-preview.css");

  function cleanPath(value) {
    if (!value) return "";
    return String(value).trim();
  }

  function siteBasePath() {
    var path = window.location.pathname || "/";
    var adminIndex = path.indexOf("/admin");
    if (adminIndex > 0) {
      return path.slice(0, adminIndex);
    }
    return "";
  }
function previewUrl(value) {
    if (!value) return "";

    var url = String(value);

    if (
      url.indexOf("blob:") === 0 ||
      url.indexOf("data:") === 0 ||
      /^https?:\/\//i.test(url)
    ) {
      return url;
    }

    var base = siteBasePath();

    if (base && url.indexOf(base + "/") === 0) {
      return url;
    }

    if (base && url.indexOf("/assets/") === 0) {
      return base + url;
    }

    return url;
  }

  function assetUrl(src, getAsset) {
    var value = cleanPath(src);

    if (!value) {
      return "";
    }

    try {
      var asset = getAsset(value);

      if (asset) {
        var resolved = asset.toString ? asset.toString() : String(asset);

        if (resolved && resolved.indexOf("[object Object]") === -1) {
          console.log("[cms-preview] asset resolved", {
            value: value,
            resolved: resolved
          });
          return resolved;
        }
      }
    } catch (error) {
      console.warn("[cms-preview] getAsset failed", {
        value: value,
        error: error
      });
    }

    if (
      /^https?:\/\//i.test(value) ||
      value.indexOf("blob:") === 0 ||
      value.indexOf("data:") === 0
    ) {
      return value;
    }

    var basePath = siteBasePath();
    var clean = value.indexOf(basePath + "/") === 0
      ? value.slice(basePath.length)
      : value;

    if (value.indexOf("/uostriathlon/assets/") === 0) {
      return value;
    }

    if (value.indexOf("/assets/") === 0) {
      return "/uostriathlon" + value;
    }

    return basePath + (clean.charAt(0) === "/" ? clean : "/" + clean);
  }

  function imageFrame(src, getAsset, cropX, cropY, cropZoom, wide, field) {
    var url = assetUrl(src, getAsset);

    return h(
      "div",
      {
        className: wide ? "cms-image-frame cms-wide" : "cms-image-frame",
        style: {
          "--crop-x": (cropX || 50) + "%",
          "--crop-y": (cropY || 50) + "%",
          "--crop-zoom": ((cropZoom || 100) / 100)
        }
      },
      url
        ? h("img", { src: url, alt: "" })
        : h("div", { className: "cms-no-image" }, "No image selected")
    );
  }

  function heading(section, label) {
    return [
      h("div", { className: "cms-tag" }, label || section.type || "Section"),
      h("h2", { className: "cms-title" }, section.title || section.platform || section.type || "Untitled"),
      section.subtitle ? h("p", { className: "cms-subtitle" }, section.subtitle) : null,
      section.body ? h("p", { className: "cms-body" }, section.body) : null
    ];
  }

  function renderHero(section, getAsset, key) {
    
var source = section.background_image_raw || "";
    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Hero"),
      source
        ? imageFrame(
            source,
            getAsset,
            section.background_crop_x,
            section.background_crop_y,
            section.background_crop_zoom,
            true
          )
        : h("p", { className: "cms-muted" }, "No hero image selected")
    );
  }

  function renderStats(section, key) {
    var items = section.items || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Stats"),
      h(
        "div",
        { className: "cms-grid" },
        items.map(function (item, i) {
          return h(
            "article",
            { className: "cms-card", key: i },
            h("div", { className: "cms-card-body" },
              h("span", { className: "cms-card-name" }, item.number || ""),
              item.label ? h("span", { className: "cms-card-role" }, item.label) : null
            )
          );
        })
      )
    );
  }

  function renderCards(section, getAsset, key) {
    var cards = section.cards || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Cards / boxes"),
      h(
        "div",
        { className: "cms-grid cms-grid-3" },
        cards.map(function (card, i) {
          var source = card.image_raw || "";

          return h(
            "article",
            { className: "cms-card", key: i },
            source
              ? h("div", { className: "cms-card-body" },
                  imageFrame(source, getAsset, card.crop_x, card.crop_y, card.crop_zoom, false)
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

  function renderGallery(section, getAsset, key) {
    var images = section.images || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Gallery"),
      h(
        "div",
        { className: "cms-grid cms-grid-3" },
        images.map(function (item, i) {
          var source = item.src_raw || "";

          return h(
            "article",
            { className: "cms-card", key: i },
            h("div", { className: "cms-card-body" },
              imageFrame(source, getAsset, item.crop_x, item.crop_y, item.crop_zoom, false),
              item.caption ? h("p", null, item.caption) : null
            )
          );
        })
      )
    );
  }

  function renderCommittee(section, getAsset, key) {
    var members = section.members || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Committee"),
      h(
        "div",
        { className: "cms-grid cms-grid-3" },
        members.map(function (member, i) {
          
var source = cleanPath(member.image_raw || "");
          return h(
            "article",
            { className: "cms-card", key: i },
            h("div", { className: "cms-card-head" },
              h("span", { className: "cms-card-name" }, member.name || "Committee member"),
              member.role ? h("span", { className: "cms-card-role" }, member.role) : null
            ),
            h("div", { className: "cms-card-body" },
              imageFrame(source, getAsset, member.crop_x, member.crop_y, member.crop_zoom, false),
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

  function renderTimeline(section, key) {
    var items = section.items || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Timeline"),
      items.map(function (item, i) {
        return h("div", { className: "cms-timeline-item", key: i },
          h("strong", null, item.title || "Timeline item"),
          item.description ? h("p", null, item.description) : null
        );
      })
    );
  }

  function renderFAQ(section, key) {
    var items = section.items || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "FAQ"),
      items.map(function (item, i) {
        return h("div", { className: "cms-faq-item", key: i },
          h("strong", null, item.question || "Question"),
          item.answer ? h("p", null, item.answer) : null
        );
      })
    );
  }

  function renderCTA(section, key) {
    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Call to action")
    );
  }

  function renderSocials(section, getAsset, key) {
    var items = section.items || [];

    return h(
      "section",
      { className: "cms-section", key: key },
      heading(section, "Socials"),
      h(
        "div",
        { className: "cms-grid" },
        items.map(function (item, i) {
          var source = item.icon_raw || "";

          return h(
            "article",
            { className: "cms-card", key: i },
            source
              ? h("div", { className: "cms-card-body" },
                  imageFrame(source, getAsset, item.crop_x, item.crop_y, item.crop_zoom, false)
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

  function renderGeneric(section, key) {
    return h("section", { className: "cms-section", key: key }, heading(section, section.type));
  }

  function renderSection(section, getAsset, index) {
    if (!section || !section.type) {
      return null;
    }

    switch (section.type) {
      case "hero":
        return renderHero(section, getAsset, index);
      case "stats":
        return renderStats(section, index);
      case "cards":
        return renderCards(section, getAsset, index);
      case "gallery":
        return renderGallery(section, getAsset, index);
      case "committee":
        return renderCommittee(section, getAsset, index);
      case "timeline":
        return renderTimeline(section, index);
      case "faq":
        return renderFAQ(section, index);
      case "cta":
        return renderCTA(section, index);
      case "socials":
        return renderSocials(section, getAsset, index);
      default:
        return renderGeneric(section, index);
    }
  }

  var PagePreview = createClass({
    render: function () {
      var data = this.props.entry.getIn(["data"]).toJS();
      var sections = data.sections || [];
      var getAsset = this.props.getAsset;
      if (brand.logo) {
        console.log("[cms-preview] settings logo raw:", brand.logo);
        console.log("[cms-preview] settings logo resolved:", assetUrl(brand.logo, getAsset));
      }
return h(
        "main",
        { className: "cms-page-preview" },
        h("section", { className: "cms-section" },
          h("div", { className: "cms-tag" }, "Page"),
          h("h1", { className: "cms-title" }, data.title || "Untitled page"),
          data.description ? h("p", { className: "cms-subtitle" }, data.description) : null
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

  /* settings logo preview:start */
  var SettingsPreview = createClass({
    render: function () {
      var data = this.props.entry.getIn(["data"]).toJS();
      var brand = data.brand || {};
      var getAsset = this.props.getAsset;

      return h(
        "main",
        { className: "cms-page-preview" },
        h(
          "section",
          { className: "cms-section" },
          h("div", { className: "cms-tag" }, "Site settings"),
          h("h1", { className: "cms-title" }, brand.short_name || brand.name || "Brand"),
          brand.tagline ? h("p", { className: "cms-subtitle" }, brand.tagline) : null,
          brand.logo
            ? imageFrame(
                brand.logo,
                getAsset,
                brand.logo_crop_x || 50,
                brand.logo_crop_y || 50,
                brand.logo_crop_zoom || 100,
                false
              )
            : h("p", { className: "cms-muted" }, "No logo selected"),
          h("div", { className: "cms-source-note" }, "Logo path: " + (brand.logo || "none")),
          h("p", { className: "cms-muted" }, "Logo crop: X " + (brand.logo_crop_x || 50) + "%, Y " + (brand.logo_crop_y || 50) + "%, zoom " + (brand.logo_crop_zoom || 100) + "%")
        )
      );
    }
  });

  CMS.registerPreviewTemplate("settings", SettingsPreview);
  /* settings logo preview:end */

})();
