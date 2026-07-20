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
  for how that pipeline works.

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
