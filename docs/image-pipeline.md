# Image pipeline

`scripts/optimise_site_images.py` runs on every publish (see
`.github/workflows/deploy.yml`). It reads each content file, finds the
Hero's background image and every **image block** inside any tile's
`blocks` list, applies the crop/zoom recorded by the editor, resizes to
the size that kind of image needs, and writes a compressed WebP into
`assets/images/generated` (or `assets/images/committee/profiles`, kept
as a separate folder for backwards compatibility with existing
committee photo uploads). The raw upload stays in the repo so it can be
re-cropped later; the live site never loads it.

Because an image block always lives at the same place in the data —
somewhere in `sections[].tiles[].blocks[]`, tagged `type: image` — this
script has one code path for every tile, regardless of preset, and
regardless of how many image blocks a single tile happens to contain
(each is found and processed independently). Sizing is chosen by the
image's **shape** (`square` or `round`), not by what preset it happens
to sit in:

| Use                                   | Output size | WebP quality |
|-----------------------------------------|------------|-------------|
| Hero background                          | 2000×1125  | 76          |
| Tile image, shape = square (the default) | 1000×1000  | 80          |
| Tile image, shape = round                 | 512×512    | 88          |
| Brand logo                                | 240×240    | 92          |

## Why WebP, and why these settings

WebP at a moderate quality is currently the best size-for-quality
trade-off broadly supported without extra tooling: for photographic
content it typically produces 25–35% smaller files than an
equivalent-quality JPEG, with no extra build dependency. AVIF can
compress a little further again, but Pillow needs an additional native
plugin to write it — an extra thing to keep working in CI for a modest
additional saving on a site this size — so WebP is the better trade-off
here.

Two things matter most for actual page-load speed, and both are handled
in the pipeline rather than left to chance:

- **Serve the size it's shown at.** Every image maps to one fixed output
  size — never the original upload resolution. A resize before
  compression saves far more than compression settings ever can.
- **Compress each shape for how it's actually used.** A large hero photo
  is seen for a second while text and buttons load in front of it, so it
  can tolerate a lower quality than a small, sharp-edged round icon that
  sits on screen at full attention.

All resizing uses Lanczos resampling (the highest-quality resize filter
Pillow offers) and `method=6`, WebP's slowest-but-smallest compression
effort setting — the build only runs on publish, so there's no reason not
to spend the extra CPU time for a smaller file.

## Markup-level loading

Compression only controls file size; the templates control *when* the
browser fetches each file:

- Every `<img>` on the site carries explicit `width`/`height` attributes
  matching its generated size, so the browser can reserve the right space
  before the image loads and the page doesn't jump around as photos come
  in (this is the single biggest lever on Cumulative Layout Shift).
- Every tile image is `loading="lazy" decoding="async"`, so the browser
  doesn't fetch it until it's about to scroll into view.
- Tile images render as real `<img>` elements rather than CSS
  `background-image`s, so the browser can lazy-load and prioritise them
  the same way it does any other image.
- The layout preloads the first hero photo on a page
  (`<link rel="preload" as="image" fetchpriority="high">`), since that's
  normally the largest single image on the page and the one that decides
  Largest Contentful Paint. Nothing else is preloaded, so this doesn't
  compete with it for bandwidth.

## Running it locally

```
python3 scripts/optimise_site_images.py
```
