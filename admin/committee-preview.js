(function () {
  CMS.registerPreviewStyle("./committee-preview.css");

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

      function assetUrl(path) {
        if (!path) return "";
        try {
          var asset = getAsset(path);
          return asset && asset.toString ? asset.toString() : path;
        } catch (e) {
          return path;
        }
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
            var img = assetUrl(member.image);
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
