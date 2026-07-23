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

A Card grid controls *layout* (columns, equal height, scrolling, width,
padding, background) and one behaviour switch, **Expandable**. A Tile
controls *content*: an optional badge, eyebrow, title, subtitle, body
text, image (or an embed instead of an image), some label/value rows,
question & answer pairs, an email address, and buttons. Every one of
those is optional. A tile also controls the **order** those pieces
render in (drag to reorder) and the **visibility** of each one
individually — see below.

**Preset** is a dropdown on a Card grid purely as a label and a reminder
of which fields are worth filling in for that kind of content (see the
table at the bottom of this page). It doesn't hide or add any fields —
you can change it, or set it to "Custom", any time without losing
content. Decap CMS genuinely can't show or hide fields based on this
choice — see `PHASE3-NOTES.md` if you want the technical reason.

## Content order

By default, a tile's content renders in the order it always has —
Image, Eyebrow, Title, Subtitle, Body, Q&A, Meta rows, Email, Buttons.
Override this per tile with **Content order**: it's a drag-and-drop list
— the order you arrange it in *is* the order the website renders in, top
to bottom. Add each piece of content you want, drag it into place.
Leave it empty to keep the default order.

Anything you don't add to Content order simply doesn't render, even if
the field has content filled in elsewhere on the tile — so if you set a
custom order, make sure it includes everything you actually want shown.

Badge (the small tag in the corner, e.g. a date) and the numbered-step
indicator are not part of Content order — they're positioned outside the
tile's content, so they always render exactly as before.

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

## Expandable grids, and visibility

A Card grid can be **Expandable** or not (a single on/off switch, under
the grid's Behaviour settings). When it's off, every tile always shows
everything. When it's on, each tile becomes something you can open —
useful for committee bios or FAQ answers you don't want cluttering the
page up front.

*How* an expandable tile opens — hover or click — is no longer chosen
per section. It's one setting for the whole site:
**Site Settings → Interactions → "How hidden content is revealed."**
Every expandable grid on the site follows it, so the interaction feels
consistent everywhere. (Touch devices always use a tap regardless of
this setting, since there's no such thing as "hover" on a phone.)

Each piece of content on a tile — Eyebrow, Title, Subtitle, Image, Body,
Q&A, Meta rows, Email, Buttons — has its own **Visibility**:

- **Always visible.**
- **Hidden initially** — only shown once the tile is opened. Only has an
  effect if the grid (or this tile) is Expandable.
- **Hidden** — never shown, even if the field has content.

Leave a field on its blank default and it falls back automatically:
Eyebrow/Title/Subtitle/Image are always visible regardless; everything
else follows the grid's Expandable setting (hidden initially if the grid
is expandable, always visible if it isn't).

A single tile can override the grid's Expandable setting under its own
**Advanced → Expandable override**, for the rare case one tile in a grid
needs to behave differently from its neighbours.

**Example** — a committee card showing name and photo up front,
everything else hidden until opened:

```
Title: Always visible
Subtitle: Always visible
Image: Always visible
Body: Hidden initially
Email: Hidden initially
Buttons: Hidden initially
```

Normal state:

```
Alex Smith
President
[Photo]
```

Opened state adds:

```
Runs committee meetings and manages training.
Email →
```

Both fully-visible and expandable tiles are supported on the same site,
grid by grid.

## Preset starting points

| Preset     | Fill in                                         | Suggested Content order |
|------------|--------------------------------------------------|--------------------------|
| Committee  | Title (name), Subtitle (role), Image, Body (bio), Email | Title, Subtitle, Image, Body, Email, Buttons |
| Event      | Badge (date), Title, Image, Body, Meta (Type/Location), Buttons | Title, Image, Meta, Buttons |
| FAQ        | Title (question), Body (answer)                   | Title, Body |
| Sponsor    | Image (logo), Title (organisation), Body, Buttons (website) | Image, Title, Body, Buttons |
| Cards / Gallery / Stats / Custom | whatever fits            | usually all "Always visible" |

## Editing

1. Open `/admin` on the live site (or `/admin/local.html` when testing
   locally).
2. Open a page and add/edit sections. Each section in the list shows its
   type and title in the collapsed view.
3. Publish. GitHub Pages rebuilds automatically — this takes a minute or
   two.

## Site Settings is the design system

Site Settings now controls more than branding. Under **Design system**
you can set the whole site's colours, card corner roundness/shadow/
padding/default image shape, heading weight, body text density, page
width, grid gap, and vertical section spacing — one place, applied
everywhere, no CSS or code involved. Individual sections can still
override background, width, and padding for themselves if a specific
block needs to differ from the site default.

**Interactions** controls the one hover-vs-click setting described
above.

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

A Tile's image has one extra option, **Shape**: leave it blank to use
the site's default image shape (Site Settings → Design system → Cards),
or set it explicitly to `square` (photos) or `round` (icon-style images,
e.g. social platform logos).

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
   / `admin/config.local.yml`, and a row to the table above — this is
   guidance only, not new configuration for the renderer.
2. That's it. `_includes/tile.html` already knows how to render any
   combination of the existing Content fields, in whatever order and
   visibility you configure.

Only build a genuinely new Section type (with its own Liquid include and
a new `{% when %}` branch in `_includes/renderer.html`) if the thing you
need truly isn't "a grid of tiles" — the way Hero and Text aren't.

## What this editor can't do (and why)

See `PHASE3-NOTES.md` for a straight answer on which parts of a
"Notion/Webflow-style" editor are genuinely achievable in Decap CMS
without custom widget code, and which aren't.
