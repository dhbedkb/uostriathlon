# Website Editor Guide

This site uses Jekyll, GitHub Pages, and Decap CMS.

## Editing

1. Open `/admin` on the live site (or `/admin/local.html` when testing locally).
2. Open a page and add/edit sections.
3. Publish. GitHub Pages rebuilds automatically — this takes a minute or two.

## Images: upload, crop, compress

Every image field in the editor works the same way:

1. **Upload** the original photo in the "Source image" field. The editor
   preview shows it immediately, inside a frame shaped like where it will
   actually appear (square card, wide hero banner, etc).
2. **Reframe and zoom** using the crop horizontal %, crop vertical %, and
   crop zoom % fields next to it. The preview frame updates live — drag
   the horizontal/vertical sliders to move the visible area, and increase
   zoom % to move in closer.
3. **Publish.** On every publish, a build step reads the source photo and
   your crop settings, produces a compressed WebP at the correct size, and
   updates the page automatically to use it. You never edit the
   "Optimised image" field yourself — it's generated.

The live site always loads the small compressed WebP, never the original
upload, so pages stay fast even with high-resolution source photos.

### Why the editor preview and the live site can look slightly different at first

Before the first publish, there's no compressed WebP yet, so the editor
preview shows the *raw* upload with the crop applied live in the browser.
After publishing, the real compressed image is generated and the site uses
that instead. The crop math is identical in both places, so the framing
should match — if it doesn't, publish again and refresh.

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
3. Add an entry to `admin/config.yml` under `collections > pages > files`
   pointing at that content file, and to `_data/navigation.yml` if it
   should appear in the menu.
