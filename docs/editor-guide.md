# Website Editor Guide

This website uses Jekyll, GitHub Pages, and Decap CMS.

Editors should make content and image changes through the CMS, not by editing YAML files directly.

## Editing the live website

Use the live CMS at the website admin page.

Typical workflow:

1. Open the CMS.
2. Edit a page or site setting.
3. Upload or replace images in the relevant image field.
4. Publish the change.
5. Wait for GitHub Pages to finish deploying.
6. Refresh the public page.

## Local CMS testing

Local CMS editing only works properly when the Decap local backend proxy is running.

Use two terminals.

Terminal 1:

    cd ~/Downloads/Github/uostriathlon
    npx decap-server

Terminal 2:

    cd ~/Downloads/Github/uostriathlon
    bundle exec jekyll serve

Then open the local CMS page:

    /uostriathlon/admin/local.html

If uploaded images appear as broken filenames in local editing, check that npx decap-server is still running from the repository root.

## Active pages

The active public pages are:

- Home
- Training
- Races
- Socials
- Our Committee
- Members Area

The Join button links to the Join section on the Home page.

## Image upload rules

Images should be assigned in the CMS editor only.

Do not assign images by editing YAML files manually.

The CMS stores uploaded/source images in folders such as:

- assets/images/source
- assets/images/brand
- assets/images/committee/raw
- assets/images/uploads

The site may also generate optimised images in folders such as:

- assets/images/generated
- assets/images/committee/profiles

Generated images are infrastructure outputs, not files editors should manage manually.

## Committee images

Committee member photos should be uploaded through the member image field in the Committee page editor.

The public site currently prefers the raw editor-uploaded image first. This means newly uploaded committee photos can appear without waiting for generated image output.

The optimiser may still create generated images, but editors do not need to manage those directly.

## Hero images

Hero images should be uploaded through the hero image field in the CMS.

The public site currently prefers the raw uploaded hero image first, then falls back to generated images if needed.

## Preview behaviour

CMS previews may not always show a brand-new image perfectly before publishing.

If an image preview looks broken:

1. Confirm the correct image was selected in the CMS field.
2. Publish the entry.
3. Refresh the editor.
4. Refresh the public page.
5. If testing locally, make sure npx decap-server is running.
6. If testing live, wait for GitHub Pages deployment to finish.

A broken preview before publishing does not always mean the published site is broken.

## Removing or replacing images

When an image is cleared or replaced in the CMS, the page reference changes, but the old uploaded image file may remain in the repository.

This is expected.

Old unused image files are cleaned separately using a safe cleanup script.

Dry-run cleanup:

    python3 scripts/cleanup_unreferenced_images.py

Apply cleanup only after checking the dry-run output:

    python3 scripts/cleanup_unreferenced_images.py --apply

## Optimising images

The optimiser can generate derived WebP images.

Run:

    python3 scripts/optimise_site_images.py

Optional generated-output pruning:

    python3 scripts/optimise_site_images.py --prune-generated

Editors normally do not need to run these commands.

## Safe rule

If something looks wrong, do not manually edit image paths. Ask the site maintainer to check the CMS field, uploaded file, and build output.

## Known behaviour and troubleshooting

### Image previews

The CMS preview may not always show a newly uploaded image immediately before publishing.

This is expected behaviour.

If an image does not show in the preview:

1. Publish the page.
2. Wait for the site deployment to complete.
3. Refresh the editor.
4. Refresh the public page.
5. If using the local CMS, check that `npx decap-server` is still running.

### Image cleanup

When an image is replaced or removed in the CMS, the old file may remain in the repository.

This is expected.

The site maintainer can run a safe dry-run cleanup with:

    python3 scripts/cleanup_unreferenced_images.py

Only after reviewing the dry-run output should cleanup be applied with:

    python3 scripts/cleanup_unreferenced_images.py --apply

### Generated images

The site may create generated WebP images for performance.

Editors should not manage generated images manually.

Maintainers can run:

    python3 scripts/optimise_site_images.py

Optional generated-output pruning is available with:

    python3 scripts/optimise_site_images.py --prune-generated

### Golden rule

If the CMS editor and the public page disagree, trust the public page after publishing and deployment. If the public page is wrong after deployment, ask the site maintainer to check the uploaded file, YAML reference, and build output.
