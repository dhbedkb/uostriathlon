# University of Sheffield Triathlon Club — website

A Jekyll site with a Decap CMS editor. Every page is a list of
**Sections**, and almost everything on the site — cards, photos,
committee members, sponsors, stats, FAQs, events, a call-to-action,
embeds, social links — is one **Card grid** section full of **Tiles**.
See `ARCHITECTURE.md` for the full model and reasoning,
`docs/editor-guide.md` for how to use it day-to-day, and
`PHASE3-NOTES.md` for an honest account of the latest editor-UX pass —
what changed, and what a "real" Notion/Webflow-style builder would still
need (custom Decap CMS widget development, out of scope for a config
change).

- Edit content: see `docs/editor-guide.md`.
- Add a new *preset* (a new kind of card): add it to the `preset`
  select's options in `admin/config.yml` — no rendering code needed.
- Add a genuinely new *section type* (rare — only for things that truly
  aren't a grid of tiles, like Hero or Text): add a field definition in
  `admin/config.yml`, a matching include in `_includes/`, and a
  `{% when %}` branch in `_includes/renderer.html`.
- Images: uploaded through the editor, cropped/zoomed there, then
  automatically compressed to WebP on publish. See `docs/editor-guide.md`
  for how that pipeline works, and `docs/image-pipeline.md` for the
  compression settings behind it.
- Content order (drag-and-drop) and per-field Visibility (Always
  visible / Hidden initially / Hidden) are editor-controlled — see
  `docs/editor-guide.md`. Whether a grid can expand at all, and whether
  that happens on hover or click, are separate: Expandable is set per
  Card grid, hover-vs-click is one site-wide setting under Site
  Settings → Interactions.
- Site Settings is also the site's design system: colours, card
  radius/shadow/padding/default image shape, typography, and layout
  spacing all live there and apply everywhere via CSS custom
  properties — no CSS or code edits needed to reskin the site.

## The tile system, in one rule

Every card-like block on the site is one `.tile`: a single padded box.
If a tile has a photo, the photo sits *inside* that same padding, at a
fixed 1:1 aspect ratio (or round, for icon-style images), with the same
gap above the text that follows it. It never bleeds to the tile's edge
while the text stays indented. `_includes/tile.html` builds every tile
from this system regardless of what preset it was created from, so this
stays true automatically as the site grows — and the editor controls
both which pieces of content appear, what order they render in, and
whether they start visible or hidden.

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
