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

  function assetToString(asset) {
    if (!asset) return "";
    var resolved = asset.toString ? asset.toString() : String(asset);
    if (!resolved || resolved.indexOf("[object") !== -1) return "";
    return resolved;
  }

  // Decap CMS's getAsset() is synchronous on some backends (e.g. the local
  // dev backend) but returns a Promise on others (e.g. the GitHub backend,
  // which has to fetch the blob). AssetImage handles both cases and
  // re-renders once the real URL is known.
  var AssetImage = createClass({
    getInitialState: function () {
      return { status: "idle", url: "" };
    },

    componentDidMount: function () {
      this.resolve(this.props.src);
    },

    componentDidUpdate: function (prevProps) {
      if (prevProps.src !== this.props.src || prevProps.getAsset !== this.props.getAsset) {
        this.resolve(this.props.src);
      }
    },

    resolve: function (rawSrc) {
      var value = clean(rawSrc);

      if (!value) {
        this.setState({ status: "empty", url: "" });
        return;
      }

      if (value.indexOf("blob:") === 0 || value.indexOf("data:") === 0 || /^https?:\/\//i.test(value)) {
        this.setState({ status: "ready", url: previewUrl(value) });
        return;
      }

      this.setState({ status: "loading", url: "" });

      var self = this;
      var getAsset = this.props.getAsset;
      var result;

      try {
        result = getAsset(value);
      } catch (error) {
        self.setState({ status: "ready", url: previewUrl(value) });
        return;
      }

      if (result && typeof result.then === "function") {
        result
          .then(function (asset) {
            var resolved = assetToString(asset);
            self.setState({ status: "ready", url: previewUrl(resolved || value) });
          })
          .catch(function () {
            self.setState({ status: "ready", url: previewUrl(value) });
          });
        return;
      }

      var resolved = assetToString(result);
      self.setState({ status: "ready", url: previewUrl(resolved || value) });
    },

    render: function () {
      if (this.state.status === "loading" || this.state.status === "idle") {
        return h("div", { className: "crop-frame-empty" }, "Loading preview…");
      }
      if (!this.state.url) {
        return h("div", { className: "crop-frame-empty" }, "No image selected");
      }
      return h("img", { src: this.state.url, alt: "" });
    }
  });

  // A crop frame renders the raw uploaded image inside a box shaped like the
  // published output (square, wide hero, round icon…), positioned and
  // zoomed using the same crop_x / crop_y / crop_zoom values the live
  // site's CSS uses.
  function cropFrame(rawSrc, getAsset, cropX, cropY, cropZoom, shape) {
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
      h(AssetImage, { src: rawSrc, getAsset: getAsset }),
      h("span", { className: "crop-frame-label" }, "Crop preview")
    );
  }

  function heading(title, label, subtitle) {
    return [
      h("p", { className: "cp-tag" }, label || "Section"),
      h("h2", { className: "cp-title" }, title || "Untitled"),
      subtitle ? h("p", { className: "cp-subtitle" }, subtitle) : null
    ];
  }

  // --- Hero: the one section type that still gets bespoke preview
  // treatment, because it's a full-bleed background photo rather than a
  // tile — everything else below is generic block rendering. ---
  function renderHero(section, getAsset, key) {
    var source = section.background_image_raw || "";
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section.title, "Hero", section.subtitle),
      source
        ? cropFrame(source, getAsset, section.background_crop_x, section.background_crop_y, section.background_crop_zoom, "wide")
        : h("p", { className: "cp-muted" }, "No hero image selected")
    );
  }

  // --- Tile-grid: the rendering engine. This function has no idea what
  // "committee" or "sponsor" mean — it only walks tile.blocks in order,
  // splitting on the first "expand" block, exactly like
  // _includes/tile.html does on the live site. A brand-new block type
  // never requires touching this file's structure, only one more
  // switch case below (mirroring one more {% when %} in tile.html). ---

  function renderBlock(block, getAsset) {
    switch (block.type) {
      case "image": {
        var hasImage = !!(block.src_raw || block.src);
        if (!hasImage) return null;
        var shape = block.shape === "round" ? "round" : "square";
        return cropFrame(block.src_raw || block.src, getAsset, block.crop_x, block.crop_y, block.crop_zoom, shape);
      }
      case "embed":
        return block.embed_html ? h("p", { className: "cp-muted" }, "Embed") : null;
      case "eyebrow":
        return block.text ? h("p", { className: "cp-tag" }, block.text) : null;
      case "title":
        return h("strong", null, block.text || "Tile");
      case "subtitle":
        return block.text ? h("p", { className: "cp-muted" }, block.text) : null;
      case "body":
        return block.text ? h("p", null, block.text) : null;
      case "note":
        return (block.heading || block.detail)
          ? h("p", { className: "cp-muted" }, [block.heading, block.detail].filter(Boolean).join(" — "))
          : null;
      case "email":
        return block.value ? h("p", { className: "cp-muted" }, block.value) : null;
      case "buttons":
        return (block.items && block.items.length)
          ? h("p", { className: "cp-muted" }, block.items.map(function (b) { return b.label; }).filter(Boolean).join(" / "))
          : null;
      default:
        return null;
    }
  }

  function renderTile(tile, getAsset, key) {
    var blocks = tile.blocks || [];
    var nodes = [];
    var pastExpand = false;

    blocks.forEach(function (block, i) {
      if (block.type === "expand") {
        pastExpand = true;
        nodes.push(h("div", { key: "expand-" + i, className: "cp-badge", style: { position: "static", display: "block", marginBlock: "6px" } }, "— expands from here —"));
        return;
      }

      var content = renderBlock(block, getAsset);
      if (!content) return;

      var reveal = pastExpand
        ? h("span", { className: "cp-badge", style: { position: "static", display: "inline-block", marginBottom: "4px" } }, "revealed")
        : null;

      nodes.push(h("div", { key: block.type + "-" + i }, reveal, content));
    });

    return h(
      "article",
      { className: "cp-card", key: key },
      tile.badge ? h("span", { className: "cp-badge" }, tile.badge) : null,
      nodes
    );
  }

  function renderTileGrid(section, getAsset, key) {
    var tiles = section.tiles || [];
    return h(
      "section",
      { className: "cp-section", key: key },
      heading(section.title, "Card grid", section.subtitle),
      h(
        "div",
        { className: "cp-grid" },
        tiles.map(function (tile, i) {
          return renderTile(tile, getAsset, i);
        })
      )
    );
  }

  function renderGeneric(section, key) {
    return h("section", { className: "cp-section", key: key }, heading(section.title, section.type));
  }

  function renderSection(section, getAsset, index) {
    if (!section || !section.type) return null;

    switch (section.type) {
      case "hero": return renderHero(section, getAsset, index);
      case "tile-grid": return renderTileGrid(section, getAsset, index);
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
