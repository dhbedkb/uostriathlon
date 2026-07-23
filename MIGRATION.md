# Migration notes & summary of improvements

See `ARCHITECTURE.md` for the full analysis and reasoning. This file is
the practical "what changed and how to apply it" summary.

## How to apply this to your checkout

1. Copy over: `_includes/`, `_layouts/`, `_data/content/*.yml`,
   `admin/`, `assets/css/main.css`, `assets/js/app.js`, `scripts/`,
   `docs/`, and the six top-level `.md` pages, from this delivery into
   your repository (all included in this zip).
2. The six `_data/content/*.yml` files here are **already migrated** —
   they were produced by running `scripts/migrate_content.py` against
   your existing content, so no further action is needed for them.
   `scripts/migrate_content.py` is included so the mapping is auditable,
   and so you can re-run it (with `--check` first) if you have content
   changes on `main` that aren't reflected in what's migrated here.
3. Commit and push. `.github/workflows/deploy.yml` is unchanged — it
   still runs `scripts/optimise_site_images.py` before every Jekyll
   build, which now walks the new schema (see below).
4. Nothing about `_config.yml`, `oauth-worker/`, the GitHub Actions
   workflows, `.gitignore`, permalinks, or page URLs changed — this is a
   templating/CMS-schema refactor, not a hosting or routing change.

## What changed, in one table

| Before                                     | After                                                        |
|-----------------------------------------------|-----------------------------------------------------------------|
| 15 section types                                | 4 section types: `hero`, `text`, `relay-bar`, `tile-grid`      |
| 11 separate `_includes/*.html` renderers         | 1 renderer (`tile-grid.html` + `tile.html`) for all 11         |
| 3 incompatible image-crop field-naming schemes     | 1 `image` object (`src_raw`/`src`/`crop_x`/`crop_y`/`crop_zoom`/`shape`) |
| Per-type CMS preview branches (`admin/crop-preview.js`, ~230 lines) | 1 generic tile renderer + hero special-case (~230 → ~140 lines, and flat rather than growing per preset) |
| Per-type image-pipeline branches (`optimise_site_images.py`) | 1 code path keyed on image *shape*, not section type            |
| Hover-reveal (`data-reveal-mode="hover"`) hardcoded to committee only | Available to any tile-grid via `behavior.expand: hover`          |
| Section background implicit (odd/even striping)     | Explicit `layout.background: default/surface/accent`             |

## Known trade-offs / things worth knowing

- **Presets are guidance-only**, as specified — a select field with a
  hint, not conditional field visibility. Decap CMS doesn't support
  showing/hiding fields based on a sibling field's value without a
  custom widget plugin. That means every tile always shows every
  content field (image, embed, meta, qa, buttons, email) regardless of
  preset. This was judged the right trade-off: building and maintaining
  a custom Decap widget to hide fields is exactly the kind of extra
  moving part this refactor is trying to remove, for a benefit
  (slightly shorter forms) that's cosmetic. If Decap ships native
  conditional fields in future, this is the one place to revisit.
- **FAQ tiles gained a small circular toggle icon** they didn't have
  before (committee tiles already had one). This was a deliberate
  consistency call rather than an oversight — both are now the same
  "expand" tile variant.
- **Gallery images shrank slightly** (1200×1200 → 1000×1000, matching
  the tile-frame's actual on-screen size) and **all square tile
  images now share one size/quality setting** instead of gallery,
  cards, and committee each having their own. Visually this is
  unnoticeable at typical tile sizes; the win is not needing a new
  image pipeline branch for every future preset.
- **Section background no longer auto-stripes** for `tile-grid`
  sections (odd/even automatic surface-colour alternation). It's now
  explicit per section (`layout.background`), which the migration set
  to `default` everywhere, matching each section's previous computed
  background. `hero`/`text`/`relay-bar` keep the old implicit striping,
  since there are only three of them and they're not growing.
- Old `_includes/*.html` files for the removed types (`cards.html`,
  `gallery.html`, `events.html`, `committee.html`, `sponsors.html`,
  `timeline.html`, `faq.html`, `cta.html`, `embed.html`, `socials.html`,
  `stats.html`, `tile-grid.html` (the old generic-tiles one, now
  replaced by the new file of the same name)) should be deleted from
  the repo — they're not referenced by the new `renderer.html` and are
  simply omitted from this delivery.

## Phase 2: content order & per-field visibility

See the new section at the end of `ARCHITECTURE.md` and the "Content
order", "Visibility" and "Preset starting points" sections in
`docs/editor-guide.md` for the full explanation. In short:

- `_includes/tile.html` was rewritten to loop through a configurable
  `content_order` list instead of rendering eyebrow/title/subtitle/
  image/body/etc as separate hard-coded `{% if %}` blocks in a fixed
  sequence.
- A new `visibility` object lets each content field independently be
  Always / Reveal on hover / Reveal on click / Hidden, instead of the
  old all-or-nothing `behavior.expand` applying to the whole bottom
  half of a tile.
- Both are optional. Existing tiles with neither field render exactly
  as before — the fallback order matches the site's current visual
  output (Image, Eyebrow, Title, Subtitle, Body, Q&A, Meta, Email,
  Buttons), and fallback visibility reproduces the old
  always-visible/hidden-until-reveal split exactly.
- `admin/config.yml` / `admin/config.local.yml` gained two new fields
  on the tile schema (`content_order`, `visibility`); no new section
  types, no new Liquid includes, no per-preset renderer branches.
- `admin/crop-preview.js`'s `renderTile` now walks the same
  `content_order` (with the same fallback) so the CMS preview matches
  what the live site will render.

## Phase 3: content blocks replace content_order & visibility

See the new section at the end of `ARCHITECTURE.md` for the full
reasoning. Practical summary:

| Before (Phase 2)                                    | After (Phase 3)                                              |
|-------------------------------------------------------|------------------------------------------------------------------|
| Named tile fields (`eyebrow`, `title`, `image`, `body`, `qa`, `meta`, `email`, `buttons`) + separate `content_order` list + separate `visibility` object | One `blocks` list per tile — order, content, and visibility are all the same list |
| Visibility: `always` / `hover` / `click` / `hidden` per field | One `expand` marker block splits the list into "always" (before it) and "revealed" (from it onward); no `hidden` state — a block not in the list is simply absent |
| Meta rows and Q&A pairs were two different structures rendered two different ways | Merged into one block type, `note` (`heading` + `detail`), one rendering |
| Hover-vs-click resolvable per-tile (inferred from field visibility choices) | One site-wide setting again: `site.data.settings.interactions.expand_trigger` |
| `preset` lived on the Section (whole grid picks one preset) | `preset` lives on each Tile (`typeKey: preset` on the Tiles list) — a grid can mix presets |
| Presets were label-only; Content order/Visibility defaults had to be set by hand per the table in `docs/editor-guide.md` | Presets are real Decap typed-list variants with working `default: blocks: [...]` — picking "Committee member" actually pre-fills the tile |

### Migrating existing content

Applied automatically by `scripts/migrate_blocks.py` (run once against
all six `_data/content/*.yml` files, kept in the repo as a record, same
convention as `scripts/migrate_content.py` from Phase 1). If you have
content on `main` that predates Phase 3, running
`python3 scripts/migrate_blocks.py --check` first will print a diff of
exactly what it would change, safe to review before applying.

The script:
- builds each tile's `blocks` list in the order:
  eyebrow → title → subtitle → image (or embed) → **[expand, if the
  section's old `behavior.expand` was `hover` or `click`]** → body →
  one `note` per old Q&A pair → one `note` per old meta row → email →
  buttons — matching the exact order and always/revealed split the site
  has rendered since Phase 2, so migrated content looks identical once
  rebuilt;
- maps each section's old `preset` onto every tile inside it:
  `committee` → `committee`, `faq` → `faq`, `sponsors` → `sponsor`,
  `events` → `event`, anything else (`cards`/`gallery`/`stats`/
  `timeline`/`cta`/`embed`/`socials`/`custom`) → `custom`;
- removes `preset` and `behavior` from the section itself, since
  neither means anything at that level any more;
- is idempotent — re-running it against already-migrated content (a
  tile that already has a `blocks` key) makes no changes.

Nothing about section IDs, page URLs, front matter, or the `_data/`
file names changed in either phase.
