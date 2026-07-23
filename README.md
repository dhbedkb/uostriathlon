# University of Sheffield Triathlon Club — website

A Jekyll site with a Decap CMS editor. Every page is a list of
**Sections**, and almost everything on the site — cards, photos,
committee members, sponsors, FAQs, events, a call-to-action, embeds,
social links — is one **Card grid** section full of **Tiles**, each
built from a single ordered list of **Content blocks**. See
`ARCHITECTURE.md` for the full model and reasoning, and
`docs/editor-guide.md` for how to use it day-to-day.

- Edit content: see `docs/editor-guide.md`.
- Add a new *preset* (a pre-filled starting point for a new tile, e.g.
  Committee/FAQ/Sponsor/Event): see "Adding a new preset" in
  `docs/editor-guide.md` — a config change, not new rendering code.
- Add a new *block type* (a new kind of content a tile can contain):
  see "Adding a new block type" in `docs/editor-guide.md`.
- Add a genuinely new *section type* (rare — only for things that truly
  aren't a grid of tiles, like Hero or Text): add a field definition in
  `admin/config.yml`, a matching include in `_includes/`, and a
  `{% when %}` branch in `_includes/renderer.html`.
- Images: uploaded through the editor, cropped/zoomed there, then
  automatically compressed to WebP on publish. See `docs/editor-guide.md`
  for how that pipeline works, and `docs/image-pipeline.md` for the
  compression settings behind it.
- Content order is just the order of blocks in a tile's list — drag to
  reorder. Visibility is a single "— Expand from here —" block you can
  drag into place, not a separate setting. See `docs/editor-guide.md`.

## The tile system, in one rule

Every card-like block on the site is one `.tile`: a single padded box.
If a tile has a photo, the photo sits *inside* that same padding, at a
fixed 1:1 aspect ratio (or round, for icon-style images), with the same
gap above the text that follows it. It never bleeds to the tile's edge
while the text stays indented. `_includes/tile.html` builds every tile
by walking its `blocks` list in order and splitting it on the first
"expand" marker — nothing about which preset created the tile, or what
kind of content it holds, is special-cased anywhere in that file.

## Local development

```
bundle install
bundle exec jekyll serve
```

Site runs at `http://127.0.0.1:4000/uostriathlon/`.

## Local CMS editing

```
./bin/local-cms.sh
```
