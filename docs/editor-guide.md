# Website Editor Guide

This site uses Jekyll, GitHub Pages, and Decap CMS.

## The model: Page → Section → Tile → Blocks

Every page is a list of **Sections**. There are only four kinds:

- **Hero** — the big full-photo banner at the top of a page.
- **Text** — a block of prose (About us, an intro paragraph…).
- **Divider bar** — the small swim/bike/run bar on the home page.
- **Card grid** — everything else. Cards, photos, committee members,
  sponsors, FAQs, events, a call-to-action button, embedded widgets,
  social links — all of these are a **Card grid** full of **Tiles**.

A Card grid controls *layout only*: how many columns, whether tiles are
the same height, whether they scroll sideways, how much padding, what
background.

A **Tile** is: an optional Badge (a small fixed tag in the corner, e.g.
a date), an optional Visual style ("Accent" for a highlighted
call-to-action tile), and a single list of **Content blocks**. That
blocks list *is* the tile's content — what it contains, and the order
it renders in, is exactly what you see in that list. There's no
separate "content order" setting to keep in sync with it.

## Content blocks

Click "Add" on a tile's blocks list to add a piece of content:
**Eyebrow**, **Title**, **Subtitle**, **Image**, **Embed**, **Body**,
**Note**, **Email**, **Buttons**, or the special **— Expand from here —**
marker (see below). Drag any block by its handle to reorder — dragging
*is* reordering the tile, since the list you're dragging is the exact
list the site renders.

Delete a block you don't want; there's no separate "hide this" setting
— a block that isn't in the list simply doesn't render.

**Note** covers two things that used to be separate fields: a labelled
fact (e.g. Location: *Sheffield*) and an FAQ question/answer pair. Both
use the same two fields — Heading and Detail — and render the same way
(bold heading, plain text beneath). Add one Note block per fact or per
question.

**Buttons** holds a whole row of buttons at once (label/URL/style each)
— add one Buttons block, then add as many individual buttons inside it
as you need; you don't add a separate Buttons block per button.

**Image** vs **Embed**: use Image for a photo, Embed for an iframe or
widget (a Facebook post, a Strava map, etc). Only add one or the other
where you want a tile's visual to sit.

## The "— Expand from here —" block

Add this block anywhere in a tile's list to split it in two:

- Everything **above** it renders straight away.
- Everything **from it onward** stays hidden until the tile is opened
  (hover or click, depending on the site-wide Interactions setting —
  see below), and is what makes the tile show a small toggle at all.

No expand block → the whole tile is always visible, no toggle. An
expand block with nothing after it behaves the same as no expand block
at all — there's nothing to hide, so nothing collapses.

**Example** — a committee card showing name and photo up front, bio and
contact details on hover:

```
Title       "Alex Smith"
Subtitle    "President"
Image       [photo]
— Expand from here —
Body        "Runs committee meetings and manages training."
Email       "president@..."
```

Normal state: name, role, photo. Hover state adds the bio and email.

Move the Image block below the expand marker instead, and the photo
itself stays hidden until hover too — reordering the expand marker (or
anything else) is just dragging, the same as reordering any other
block.

## Presets

When you click "Add Tile" on a Card grid, you're offered five starting
points: **Committee member**, **FAQ item**, **Sponsor**, **Event**, and
**Blank tile**. Picking one of the first four pre-fills the blocks list
with the content that kind of tile usually needs — a Committee tile
starts with Title/Subtitle/Image/Expand/Body/Email already in place, an
FAQ tile starts with Title/Expand/Body, and so on. **Blank tile** starts
completely empty.

Once inserted, a preset tile is just an ordinary tile — add, remove, or
reorder its blocks exactly as you would a blank one. Nothing about
which preset it started from shows up on the published site, and
nothing prevents you from turning a "Committee member" tile into
something that looks nothing like a committee card.

**Editing what a preset pre-fills** is done from **Site Settings →
Tile presets** — no code change needed. Each preset there has the same
kind of blocks list a tile has; edit it and publish, and the next tile
someone inserts with that preset starts from whatever you saved.
Existing tiles already on a page are untouched — this only changes the
*starting point* for new tiles.

The five preset *names* themselves (which five options show up in the
"Add Tile" list) are fixed in `admin/config.yml` — adding a genuinely
new sixth option, or removing one, is a one-line code change (see
"Adding a new preset" below), because Decap CMS doesn't support a way
for the CMS itself to add a new item to that list at runtime. Editing
what an *existing* preset contains does not have that limitation.

## Interactions

**Site Settings → Interactions → "How hidden content is revealed"** is
one setting for the whole site: hover or click. It applies to every
tile anywhere that has an Expand block with something after it — a
committee bio, an FAQ answer, anything. There's no per-section or
per-tile override any more.

## Editing

1. Open `/admin` on the live site (or `/admin/local.html` when testing
   locally).
2. Open a page and add/edit sections and tiles.
3. Publish. GitHub Pages rebuilds automatically — this takes a minute or
   two.

## Images: upload, crop, compress

Every tile or hero image works the same way:

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

An Image block has one extra option, **Shape**: `square` (the default,
used for photos) or `round` (used for small icon-style images, e.g.
social platform logos).

The live site always loads the small compressed WebP, never the original
upload, so pages stay fast even with high-resolution source photos.

**The brand logo (Site Settings → Brand → Logo) is the one exception.**
It's shown at its own natural proportions, never cropped or masked to a
circle — a transparent-background PNG is the right format, and nothing
about how it's displayed will cut into it. There are no crop controls
for it, because there's nothing to crop.

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

## Adding a new preset

*Editing an existing preset's content* doesn't need this section — see
"Presets" above. This section is for adding a genuinely new preset
**name** to the "Add Tile" list (a sixth option alongside Committee/
FAQ/Sponsor/Event/Blank).

1. In `admin/config.yml`, under `.../tile-grid/fields/.../tiles/types`,
   copy one of the existing entries (Committee is a good template),
   give it a new `name`/`label`. It must reuse `types: *block_types`
   for its own `blocks` field, and can leave off `default:` (or set a
   simple one) — its real defaults will come from step 2.
2. Add a matching entry to `_data/presets.yml` with the same `name`,
   and add a matching type to the `presets` field in the "Tile presets"
   collection at the bottom of `admin/config.yml`, so the new preset is
   editable from Site Settings too.
3. Repeat both edits in `admin/config.local.yml`.

## Adding a new block type

1. Add a new entry under the `block_types` anchor (search for
   `&block_types` in `admin/config.yml`) — this one definition is
   shared by every preset, by Custom, and by Tile presets in Site
   Settings, via YAML's `*block_types` alias, so you only add it once.
2. Add a matching `{% when "yourtype" %}` case in `_includes/tile.html`.
3. If it involves an image, add a matching case in
   `admin/crop-preview.js`'s `renderBlock` function, and check whether
   `scripts/optimise_site_images.py` needs to know about it (it already
   finds any block of `type: image` automatically, wherever it sits).

Everything else — drag ordering, the Expand marker, presets — keeps
working without further changes, because none of it is aware of which
specific block types exist.
