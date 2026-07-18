(function () {
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

    if (!path) {
      return "";
    }

    // Data/blob/external URLs can be used directly.
    if (
      /^https?:\/\//i.test(path) ||
      path.indexOf("blob:") === 0 ||
      path.indexOf("data:") === 0
    ) {
      return path;
    }

    var basePath = siteBasePath();

    // Try Decap's resolver first, useful for newly selected draft assets.
    try {
      var asset = getAsset(path);
      if (asset) {
        var resolved = asset.toString ? asset.toString() : String(asset);
        if (resolved) {
          return resolved;
        }
      }
    } catch (e) {}

    // If path already includes /uostriathlon, use it as-is.
    if (basePath && path.indexOf(basePath + "/") === 0) {
      return path;
    }

    // If path starts /assets/..., prefix /uostriathlon.
    if (path.charAt(0) === "/") {
      return basePath + path;
    }

    return basePath + "/" + path.replace(/^\.\//, "");
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

      return h("main", { className: "cms-preview-wrap" },
        h("div", { className: "cms-preview-eyebrow" }, committee.eyebrow || "Team"),
        h("h1", { className: "cms-preview-title" }, committee.title || "Current committee."),
        h("p", { className: "cms-preview-subtitle" }, committee.subtitle || ""),
        h("p", { className: "cms-crop-help" },
          "This editor preview uses Source photo only. Optimised profile photo is generated later and is deliberately ignored here."
        ),

        h("div", { className: "cms-preview-grid" },
          members.map(function (member, index) {
            // IMPORTANT:
            // Do NOT fallback to image_profile or legacy image here.
            // The editor preview should reflect the source image field only.
            var source = cleanPath(member.image_raw || "");
            var img = assetUrl(source, getAsset);

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
                    : h("div", { className: "cms-no-image" }, "No Source photo selected")
                ),

                source
                  ? h("div", { className: "cms-source-note" }, "Source photo: " + source)
                  : h("div", { className: "cms-source-note" }, "No Source photo selected. The editor preview intentionally ignores Optimised profile photo."),

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
