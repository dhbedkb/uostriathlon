# Website Editor Guide

This site uses Jekyll, GitHub Pages, and Decap CMS.

## The model: Page → Section → Tile → Content

Every page is a list of **Sections**. There are only four kinds:

- **Hero** — the big full-photo banner at the top of a page.
- **Text** — a block of prose (About us, an intro paragraph…).
- **Divider bar** — the small swim/bike/run bar on the home page.
- **Card grid** — everything else. Cards, photos, committee members,
  sponsors, statistics, events, FAQs, a call-to-action button, embedded
  widgets, social links — all of these are a **Card grid** with different
  content in its **Tiles**.

A Card grid controls *layout only*: how many columns, whether tiles are
the same height, whether they scroll sideways, how much padding, what
background. A Tile controls *content*: an optional badge, eyebrow,
title, subtitle, body text, image (or an embed instead of an image),
some label/value rows, question & answer pairs, an email address, and
buttons. Every one of those is optional — a tile can be just a title and
image, or just a title and a Q&A list, or all of the above. As of Phase
2, a tile also controls the **order** those pieces render in and the
**visibility** of each one individually — see below.

**Preset** is a dropdown on a Card grid purely to help you: pick
"Committee" and the block gets labelled "Committee" in the list below so
it's easy to find later. It doesn't hide or add any fields — you can
change it, or set it to "Custom", any time without losing content.

**Reveal extra detail** (on a Card grid, or per-tile as an override)
controls the default for any field a tile marks "Reveal on hover" or
"Reveal on click" below — always shown, only shown on hover (used for
committee bios), or only shown when clicked (used for FAQs).

## Content order

By default, a tile's content renders in the order it always has —
Image, Eyebrow, Title, Subtitle, Body, Q&A, Meta rows, Email, Buttons.
You can override this per tile with **Content order**: add each piece
of content you want, drag them into the order you want, and the site
renders exactly that order. Leave it empty to keep the default.

Anything you don't add to Content order simply doesn't render, even if
the field has content filled in elsewhere on the tile — so if you add a
custom order, make sure it includes everything you actually want shown.

Badge (the small tag in the corner, e.g. a date) and the numbered-step
indicator are not part of Content order — they're positioned outside
the tile's content, not something that meaningfully "reorders" with the
rest, so they always render exactly as before.

**Example** — editor configuration:

```yaml
content_order:
  - type: image
  - type: title
  - type: buttons
  - type: body
```

Renders as: Image, Title, Buttons, Body — in that order, exactly as
configured.

## Visibility

Each content type on a tile — Eyebrow, Title, Subtitle, Image, Body,
Q&A, Meta rows, Email, Buttons — can be set individually to:

- **Always** — always shown.
- **Reveal on hover** / **Reveal on click** — hidden until the tile is
  opened. Both mean the same thing (shown once the tile opens); which
  one you pick just documents your intent, since a tile can only have
  one open gesture. Whichever appears anywhere on the tile becomes that
  tile's trigger, unless you set Reveal extra detail explicitly.
- **Hidden** — never shown, even if the field has content.

Leave a field on its blank default and it falls back to the grid's
Reveal extra detail setting (Eyebrow/Title/Subtitle/Image always fall
back to Always, regardless).

**Example** — a committee card showing name and photo up front,
everything else on hover:

```
Title: Always
Subtitle: Always
Image: Always
Body: Reveal on hover
Email: Reveal on hover
Buttons: Reveal on hover
```

Normal state:

```
Alex Smith
President
[Photo]
```

Hover state adds:

```
Runs committee meetings and manages training.
Email →
```

**Example** — a committee card that hides the photo until hover too:

```
Title: Always
Subtitle: Always
Image: Reveal on hover
Body: Reveal on hover
```

Normal state:

```
Alex Smith
President
```

Hover state adds:

```
[Photo]
Runs committee meetings and manages training.
```

Both approaches are fully supported on the same site, tile by tile.

## Preset starting points

Presets only set a label — Decap can't vary Content order or Visibility
by preset automatically (there's no way to make a shared field's default
depend on a sibling field's value without a custom widget plugin, which
would reintroduce the kind of per-type special-casing this system exists
to avoid). So instead, here's what each preset is designed to look like
once you set Content order and Visibility manually — the preset
dropdown's hint text repeats this as a reminder:

| Preset     | Content order                                | Visibility |
|------------|-----------------------------------------------|------------|
| Committee  | Title, Subtitle, Image, Body, Email, Buttons   | Title/Subtitle/Image = Always, rest = Hover |
| FAQ        | Title, Body                                     | Title = Always, Body = Click |
| Sponsors   | Image, Title, Body, Buttons                      | All = Always |
| Events     | Title, Image, Meta, Buttons (Badge is set directly on the tile and always shows) | All = Always |
| Cards / Gallery / Stats / Custom | as needed | usually all Always |

## Editing

1. Open `/admin` on the live site (or `/admin/local.html` when testing
   locally).
2. Open a page and add/edit sections. Each section in the list shows its
   type and title in the collapsed view.
3. Publish. GitHub Pages rebuilds automatically — this takes a minute or
   two.

## Images: upload, crop, compress

Every image field in the editor works the same way, whether it's a Hero
background or a Tile's image:

1. **Upload** the original photo in the "Source image" field. The editor
   preview shows it immediately, inside a frame shaped like where it will
   actually appear.
2. **Reframe and zoom** using the crop horizontal %, crop vertical %, and
   crop zoom % fields next to it. The preview frame updates live.
3. **Publish.** On every publish, a build step reads the source photo and
   your crop settings, produces a compressed WebP at the correct size,
   and updates the page automatically to use it. You never edit the
   "Optimised image" field yourself — it's generated. See
   `docs/image-pipeline.md` for what that compression step actually does.

A Tile's image has one extra option, **Shape**: `square` (the default,
used for photos) or `round` (used for small icon-style images, e.g.
social platform logos).

The live site always loads the small compressed WebP, never the original
upload, so pages stay fast even with high-resolution source photos.

## Removing or replacing images

When you clear or replace an image in the editor, the old raw upload can
be left behind in the repository. This is expected — it means you can
always re-crop from the original later. A maintainer can clear out
genuinely unused uploads with:

```
python3 scripts/cleanup_unreferenced_images.py          # dry run
python3 scripts/cleanup_unreferenced_images.py --apply  # actually delete
```

Or trigger the "Clean up unreferenced source images" GitHub Action.

## Local CMS testing

Local editing needs the Decap local backend proxy running.

```
cd <repo root>
npx decap-server        # terminal 1
bundle exec jekyll serve   # terminal 2
```

Then open `http://127.0.0.1:4000/uostriathlon/admin/local.html`.

## Adding a new page

1. Create `<page>.md` at the repo root with front matter:
   ```yaml
   ---
   layout: page
   title: My Page
   content_file: my-page
   permalink: /my-page/
   ---
   ```
2. Create `_data/content/my-page.yml` with `title`, `description`, and a
   `sections` list.
3. Add an entry to `admin/config.yml` (and `admin/config.local.yml`)
   under `collections > pages > files`, and to `_data/navigation.yml` if
   it should appear in the menu.

## Adding a genuinely new kind of content

Almost everything should be a Card grid preset, not a new section type.
Adding a new preset means:

1. Add it to the `preset` select's `options` list in `admin/config.yml`
   / `admin/config.local.yml` — this is guidance only, not new
   configuration for the renderer.
2. That's it. `_includes/tile.html` already knows how to render any
   combination of the existing Content fields, in whatever order and
   visibility you configure.

Only build a genuinely new Section type (with its own Liquid include and
a new `{% when %}` branch in `_includes/renderer.html`) if the thing you
need truly isn't "a grid of tiles" — the way Hero and Text aren't. Before
doing that, check whether it could instead be expressed as a Card grid
with an unusual `layout` (e.g. `numbered`, `chip_style`, `align_center`
already exist for exactly this reason), or an unusual Content order /
Visibility combination on its tiles.
