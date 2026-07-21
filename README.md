# University of Sheffield Triathlon Club — website

A Jekyll site with a Decap CMS editor. Every page is built from a small
set of reusable **sections** (hero, cards, gallery, committee, FAQ, etc.),
each styled by one shared **tile system** in `assets/css/main.css`.

- Edit content: see `docs/editor-guide.md`.
- Add a new kind of section: add a field definition in `admin/config.yml`,
  a matching include in `_includes/`, and a `{% when %}` branch in
  `_includes/renderer.html`.
- Images: uploaded through the editor, cropped/zoomed there, then
  automatically compressed to WebP on publish. See `docs/editor-guide.md`
  for how that pipeline works, and `docs/image-pipeline.md` for the
  compression settings behind it.

## The tile system, in one rule

Every card-like block on the site — cards, events, committee members,
gallery photos, FAQ, CTA — is one `.tile`: a single padded box. If a
tile has a photo, the photo sits *inside* that same padding, at a fixed
1:1 aspect ratio, with the same gap above the text that follows it. It
never bleeds to the tile's edge while the text stays indented — that
mismatch is what used to make image tiles look misaligned. Build new
section types on the same `.tile` / `.tile-frame` / `.tile-body`
classes in `assets/css/main.css` and they'll automatically line up with
everything else on the site.

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
