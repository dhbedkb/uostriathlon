(function () {
  CMS.registerPreviewStyle("./crop-preview.css");

  function clean(value) {
    return value ? String(value).trim() : "";
  }

  function siteBasePath() {
    var path = window.location.pathname || "/";
    var adminIndex = path.indexOf("/admin");
    return adminIndex > 0 ? path.slice(0, adminIndex) : "";
  }

  function previewUrl(value) {
    if (!value) return "";
    var url = String(value);

    if (url.indexOf("blob:") === 0 || url.indexOf("data:") === 0 || /^https?:\/\//i.test(url)) {
      return url;
    }

    var base = siteBasePath();
    if (base && url.indexOf(base + "/") === 0) return url;
    if (base && url.indexOf("/assets/") === 0) return base + url;
    return url;
  }

  function assetUrl(src, getAsset) {
    var value = clean(src);
    if (!value) return "";

    try {
      var asset = getAsset(value);
      if (asset) {
        var resolved = asset.toString ? asset.toString() : String(asset);
        if (resolved && resolved.indexOf("[object") === -1) return previewUrl(resolved);
      }
    } catch (error) {
      // fall through to raw value
    }

    return previewUrl(value);
  }

  // A crop frame renders the raw uploaded image inside a box shaped like the
  // published output (square, wide hero, etc), positioned and zoomed using
  // the same crop_x / crop_y / crop_zoom values the live site's CSS uses.
  function cropFrame(rawSrc, getAsset, cropX, cropY, cropZoom, shape) {
    var url = assetUrl(rawSrc, getAsset);

    return h(
      "div",
      {
        className: "crop-frame crop-frame-" + (shape || "square"),
        style: {
          "--crop-x": (cropX || 50) + "%",
          "--crop-y": (cropY || 50) + "%",
          "--crop-zoom": (cropZoom || 100) / 100
        }
      },
      url
        ? h("img", { src: url, alt: "" })
        : h("div", { className: "crop-frame-empty" }, "No image selected"),
      h("span", { className: "crop-frame-label" }, "Crop preview")
    );
  }

  function heading(section, label) {
    return [
      h("p", { className: "cp-tag" }, label || section.type || "Section"),
      h("h2", { className: "cp-title" }, section.title || section.platform || "Untitled"),
      section.subtitle ? h("p", { className: "cp-subtitle" }, section.subtitle) : null,
      section.body ? h("p", { className: "cp-body" }, section.body) : null
    ];
  }

  function renderHero(section, getAsset, key) {
    var source = section.background_image_raw || "";
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section, "Hero"),
      source
        ? cropFrame(source, getAsset, section.background_crop_x, section.background_crop_y, section.background_crop_zoom, "wide")
        : h("p", { className: "cp-muted" }, "No hero image selected")
    );
  }

  function renderCards(section, getAsset, key) {
    var cards = section.cards || [];
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section, "Cards"),
      h(
        "div",
        { className: "cp-grid" },
        cards.map(function (card, i) {
          return h(
            "article",
            { className: "cp-card", key: i },
            card.image_raw ? cropFrame(card.image_raw, getAsset, card.crop_x, card.crop_y, card.crop_zoom, "square") : null,
            h("strong", null, card.title || "Card"),
            card.description ? h("p", null, card.description) : null
          );
        })
      )
    );
  }

  function renderGallery(section, getAsset, key) {
    var images = section.images || [];
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section, "Gallery"),
      h(
        "div",
        { className: "cp-grid" },
        images.map(function (item, i) {
          return h(
            "article",
            { className: "cp-card", key: i },
            cropFrame(item.src_raw, getAsset, item.crop_x, item.crop_y, item.crop_zoom, "square"),
            item.caption ? h("p", null, item.caption) : null
          );
        })
      )
    );
  }

  function renderSocials(section, getAsset, key) {
    var items = section.items || [];
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section, "Socials"),
      h(
        "div",
        { className: "cp-grid" },
        items.map(function (item, i) {
          return h(
            "article",
            { className: "cp-card", key: i },
            item.icon_raw ? cropFrame(item.icon_raw, getAsset, item.crop_x, item.crop_y, item.crop_zoom, "square") : null,
            h("strong", null, item.platform || "Social link")
          );
        })
      )
    );
  }

  function renderCommittee(section, getAsset, key) {
    var members = section.members || [];
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section, "Committee"),
      h(
        "div",
        { className: "cp-grid" },
        members.map(function (member, i) {
          var source = clean(member.image_raw);
          return h(
            "article",
            { className: "cp-card", key: i },
            h("strong", null, member.name || "Committee member"),
            member.role ? h("p", { className: "cp-muted" }, member.role) : null,
            cropFrame(source, getAsset, member.crop_x, member.crop_y, member.crop_zoom, "square"),
            member.bio ? h("p", null, member.bio) : null
          );
        })
      )
    );
  }

  function renderGeneric(section, key) {
    return h("section", { className: "cp-section", key: key }, heading(section, section.type));
  }

  function renderSection(section, getAsset, index) {
    if (!section || !section.type) return null;

    switch (section.type) {
      case "hero": return renderHero(section, getAsset, index);
      case "cards": return renderCards(section, getAsset, index);
      case "gallery": return renderGallery(section, getAsset, index);
      case "socials": return renderSocials(section, getAsset, index);
      case "committee": return renderCommittee(section, getAsset, index);
      default: return renderGeneric(section, index);
    }
  }

  var PagePreview = createClass({
    render: function () {
      var data = this.props.entry.getIn(["data"]).toJS();
      var sections = data.sections || [];
      var getAsset = this.props.getAsset;

      return h(
        "main",
        { className: "cp-page" },
        h(
          "section",
          { className: "cp-section" },
          h("p", { className: "cp-tag" }, "Page"),
          h("h1", { className: "cp-title" }, data.title || "Untitled page"),
          data.description ? h("p", { className: "cp-subtitle" }, data.description) : null
        ),
        sections.map(function (section, index) {
          return renderSection(section, getAsset, index);
        })
      );
    }
  });

  ["home", "training", "races", "socials", "committee", "members"].forEach(function (name) {
    CMS.registerPreviewTemplate(name, PagePreview);
  });
})();
