# Page builder refactor: analysis & architecture

## 1. How the current builder is structured

- `_data/content/*.yml` holds one file per page, each a flat list of
  **sections**. `admin/config.yml` defines a Decap CMS "type" per section
  (`hero`, `text`, `stats`, `cards`, `tile_grid`, `gallery`, `events`,
  `committee`, `sponsors`, `timeline`, `faq`, `cta`, `embed`, `socials`,
  `relay-bar` — 15 types).
- `_includes/renderer.html` is a 15-branch `{% case %}` that maps
  `section.type` to one `_includes/<type>.html` file.
- Every one of those 15 includes independently:
  - renders the same `section-heading.html`
  - builds a `.tile-grid` of `.tile` elements (11 of the 15 do this)
  - re-derives crop/zoom CSS vars for an image
  - re-implements "is this an optimised or a raw/fallback image" logic
- `admin/crop-preview.js` mirrors this again: one `render<Type>()` function
  per section type, each manually walking that type's specific fields to
  build a crop preview.
- `scripts/optimise_site_images.py` mirrors it a **third** time: one
  `elif stype == "..."` branch per type, each hand-coding which fields
  hold `*_raw` uploads and what output size/quality they need.

So every new "kind of card" (committee, sponsors, gallery, stats, events,
FAQ, CTA, embeds, social links) has been implemented **four times**: once
in the CMS schema, once in the Liquid renderer, once in the CMS preview,
once in the image pipeline. That's the core maintenance problem — the
four layers can and do drift out of sync (e.g. `cards` uses
`crop_x`/`crop_y`/`crop_zoom` at the top level of each card, `hero` uses
`background_crop_x`, `committee` uses the same crop fields but a
different image key — three naming conventions for the same concept).

## 2. What's already reusable

- The **tile system** in `assets/css/main.css` (`.tile`, `.tile-frame`,
  `.tile-body`, `.tile-title`, `.tile-grid`) is already a single, well
  designed visual contract used by 11 of the 15 section types. This is
  the part worth keeping and building the whole system around.
- `section-heading.html` (eyebrow/title/subtitle/alignment) is already
  shared correctly.
- The crop math (`--crop-x` / `--crop-y` / `--crop-zoom` CSS custom
  properties, consumed identically by `object-position` + `transform:
  scale`) is identical everywhere it appears — it's just re-declared with
  different field names each time.
- `app.js`'s hover/click reveal logic (`[data-reveal-mode="hover"]` on a
  `<details>`) is generic already and only used by `committee.html`
  today, but nothing about it is committee-specific.

## 3. Which components duplicate each other

`cards`, `gallery`, `events`, `committee`, `sponsors`, `stats`, `faq` are
all: *a heading, a grid of tiles, each tile with an optional image, a
title, some text, and sometimes a link.* `timeline` is the same thing
with a number badge instead of a grid. `cta` is the same tile shape
rendered as a single, centred, accent-coloured tile. `socials` (cards
layout) is the same tile shape again. `embed` is the same tile shape with
an iframe/`embed_html` in place of the image. `socials` (logos layout) is
a compact variant of the same tile with the image round instead of
square. That's **11 of the 15 types being one component wearing 11 name
tags.**

## 4. Which abstractions should remain

- `hero` — genuinely unique: full-viewport background photo with
  overlay gradient, no grid, no repeated content. Kept as its own
  section type.
- `text` — genuinely unique: a two-column markdown prose layout, not a
  collection of anything. Kept as its own section type.
- `relay-bar` — a small bespoke decorative widget (swim/bike/run
  proportion bar). Not built from tiles, unlikely to grow. Kept as-is.
- The tile visual system (`.tile`/`.tile-frame`/`.tile-body`) — this is
  the thing the whole redesign is built on top of.
- The crop/zoom editing UX — kept, but standardised into one `image`
  object shape used everywhere instead of being re-declared per type.
- The hover/click reveal pattern — kept and generalised (was
  committee-only, now available to any tile grid).

## 5. Which abstractions should disappear

`stats`, `cards`, `gallery`, `events`, `committee`, `sponsors`,
`timeline`, `faq`, `cta`, `embed`, `socials` — eleven section types,
eleven Liquid includes, eleven CMS preview branches, eleven image
pipeline branches — collapse into **one** section type: `tile-grid`.
What used to distinguish them (a committee member has a bio and email; a
stat has a big number; an FAQ item expands on click) is now just which
**content fields** a tile happens to use, and a `preset` that exists
*purely* to give the CMS editor sensible field labels and defaults for
that content (per the brief: presets are editor sugar, not new data
shapes or renderers).

The result matches the four-concept model:

```
Page → Section → Tile → Content
```

Only four section *types* now exist: `hero`, `text`, `relay-bar`,
`tile-grid`. Layout (columns, equal height, scrolling, width, padding,
background, numbering) lives on the Section. Content (eyebrow, title,
subtitle, body, image, embed, badge, meta rows, buttons, email, Q&A
pairs) lives on the Tile, all optional. Behaviour (always
visible/hover-expand/click-expand) can be set on the Section and
overridden per Tile only for the rare case a single tile needs it
(e.g. one FAQ item you want open by default).

## 6. Technical debt this removes

- Three incompatible crop-field naming conventions → one `image` object.
- Four separate implementations of "which fields are raw uploads for the
  image pipeline to compress" → the pipeline now just recurses through
  `sections[].tiles[].image` uniformly, so a brand-new preset never needs
  a pipeline change.
- `unknown-section.html` / `missing-content.html` fallbacks kept as-is —
  cheap safety net, not worth removing.
- `admin/crop-preview.js` shrinks from ~230 lines of per-type React-ish
  branches to one generic tile renderer plus a thin hero special-case.

## 7. Migration strategy

All six existing `_data/content/*.yml` files are mechanically transformed
by `scripts/migrate_content.py` (kept in the repo as a record of the
migration, safe to delete after it's run once):

| Old type                | New shape                                                          |
|--------------------------|---------------------------------------------------------------------|
| `stats`                  | `tile-grid`, 4 columns, tiles with `title`=number, `subtitle`=label |
| `cards`                   | `tile-grid`, 3 columns, tiles with image/title/body/meta/button    |
| `gallery`                 | `tile-grid`, 3 columns, image-led tiles, no title                  |
| `events`                  | `tile-grid`, 3 columns, `badge`=date, `meta`=[type, location]      |
| `committee`                | `tile-grid`, 3 columns, `behavior.expand: hover`, `qa` list         |
| `sponsors`                 | `tile-grid`, 4 columns, text-only tiles + button                    |
| `timeline`                 | `tile-grid`, 1 column, `layout.numbered: true`                      |
| `faq`                      | `tile-grid`, 1 column, `behavior.expand: click`                     |
| `cta`                       | `tile-grid`, 1 column, single accent tile, centred                  |
| `embed`                     | `tile-grid`, tiles carry `embed` content instead of `image`         |
| `socials`                   | `tile-grid`, `layout.chip_style` for the old "logos" row layout      |

No field is dropped silently — the migration script prints anything it
can't map so it can be checked by hand. Front matter, permalinks, and
`content_file` keys on the six top-level `.md` pages are untouched, so
no URLs change.

## 8. What an editor sees now

Instead of 15 block types in the "Add section" list, they see 4:
**Hero**, **Text**, **Card grid**, **Divider bar**. Adding a "Card grid"
prompts for a **preset** (Cards / Gallery / Committee / Sponsors /
Statistics / Events / FAQ / Call to action / Social links / Embed /
Timeline / Custom) purely to pre-fill sensible labels and defaults —
picking "Custom" or deleting the preset never removes any content, it
just stops suggesting field names.

## 9. Phase 2 addendum: content order & per-field visibility

The Section/Tile/Content model didn't need to change to support this —
only `_includes/tile.html` did. Two new optional Tile-level fields:

- `content_order`: a list of `{type: "..."}` entries. `tile.html`
  builds its render loop from this (falling back to the same order it
  has always used when the field is absent), instead of hard-coding
  eyebrow → title → subtitle → image → body → … as separate `{% if %}`
  blocks in a fixed sequence.
- `visibility`: an object mapping each content type to
  always/hover/click/hidden, read per item inside that same loop. The
  existing single `behavior.expand` (none/hover/click) still exists and
  still governs the tile's one open/close mechanism; visibility just
  decides which fields sit inside that expandable region versus outside
  it (or are dropped entirely).

Nothing about the CMS schema, the renderer, or the image pipeline grew
a second per-type branch — `content_order` and `visibility` are generic
Content-level metadata, the same as `meta` or `qa` already were, so a
brand-new content field added to a tile in future only ever needs one
new `{% when %}` case in the loop and one new option in the two select
lists — not a new component.

A deliberate scoping decision: badge and the numbered-index badge stay
fixed, non-orderable overlay elements. They're absolutely positioned in
CSS, not flow content, so making them draggable inside `content_order`
would be cosmetic-only (nothing would visually change) while adding a
rendering special case for no real benefit.

Another deliberate scoping decision: Decap CMS has no way to make one
field's default vary based on a sibling field's value (e.g. "when preset
= Committee, default Content order to X") without a custom widget
plugin. Building one would reintroduce exactly the kind of per-type
special-casing this whole refactor exists to remove, for a benefit
(pre-filled defaults) that's fully covered by the recommended-values
table in `docs/editor-guide.md` and the preset dropdown's hint text.
See `MIGRATION.md` for the practical summary of this change.
