#!/usr/bin/env bash
set -e

echo "Ensuring .gitignore entries..."

touch .gitignore

grep -qxF "_site/" .gitignore || echo "_site/" >> .gitignore
grep -qxF ".jekyll-cache/" .gitignore || echo ".jekyll-cache/" >> .gitignore
grep -qxF ".sass-cache/" .gitignore || echo ".sass-cache/" >> .gitignore
grep -qxF ".DS_Store" .gitignore || echo ".DS_Store" >> .gitignore

echo "Stopping Git from tracking _site if it was tracked..."
git rm -r --cached _site >/dev/null 2>&1 || true

echo "Removing macOS .DS_Store files..."
find . -name ".DS_Store" -delete

echo "Creating admin and oauth-worker folders..."
mkdir -p admin oauth-worker

echo "Writing admin/index.html..."
cat > admin/index.html <<'HTML'
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Content Manager · Sheffield Triathlon</title>
</head>
<body>
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
</body>
</html>
HTML

echo "Writing admin/config.yml..."
cat > admin/config.yml <<'YAML'
backend:
  name: github
  repo: dhbedkb/uostriathlon
  branch: main
  base_url: https://TODO-your-worker-subdomain.workers.dev
  auth_endpoint: auth

media_folder: "assets/images/uploads"
public_folder: "/assets/images/uploads"
publish_mode: simple
site_url: https://www.uostriathlon.co.uk

collections:
  - name: "site_pages"
    label: "Pages"
    files:
      - name: "home"
        label: "Home"
        file: "_data/content/home.yml"
        fields: &page_fields
          - label: "Title"
            name: "title"
            widget: "string"
          - label: "Description"
            name: "description"
            widget: "text"
          - label: "Sections"
            name: "sections"
            widget: "list"
            typeKey: "type"
            types:
              - name: "hero"
                label: "Hero"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - { label: "Body", name: "body", widget: "text", required: false }
                  - { label: "Background image", name: "background_image", widget: "image", required: false }
                  - label: "Primary button"
                    name: "primary_button"
                    widget: "object"
                    required: false
                    fields:
                      - { label: "Label", name: "label", widget: "string" }
                      - { label: "URL", name: "url", widget: "string" }
                  - label: "Secondary button"
                    name: "secondary_button"
                    widget: "object"
                    required: false
                    fields:
                      - { label: "Label", name: "label", widget: "string" }
                      - { label: "URL", name: "url", widget: "string" }

              - name: "text"
                label: "Text block"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - { label: "Body", name: "body", widget: "markdown", required: false }

              - name: "stats"
                label: "Stats"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - label: "Items"
                    name: "items"
                    widget: "list"
                    fields:
                      - { label: "Number", name: "number", widget: "string" }
                      - { label: "Label", name: "label", widget: "string" }

              - name: "cards"
                label: "Cards"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - label: "Cards"
                    name: "cards"
                    widget: "list"
                    fields:
                      - { label: "Title", name: "title", widget: "string" }
                      - { label: "Label", name: "label", widget: "string", required: false }
                      - { label: "Description", name: "description", widget: "text", required: false }
                      - { label: "Image", name: "image", widget: "image", required: false }
                      - { label: "URL", name: "url", widget: "string", required: false }
                      - { label: "Schedule", name: "schedule", widget: "string", required: false }
                      - { label: "Location", name: "location", widget: "string", required: false }

              - name: "gallery"
                label: "Gallery"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - label: "Images"
                    name: "images"
                    widget: "list"
                    fields:
                      - { label: "Image", name: "src", widget: "image" }
                      - { label: "Alt text", name: "alt", widget: "string", required: false }
                      - { label: "Caption", name: "caption", widget: "string", required: false }

              - name: "events"
                label: "Events"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - label: "Items"
                    name: "items"
                    widget: "list"
                    fields:
                      - { label: "Title", name: "title", widget: "string" }
                      - { label: "Date", name: "date", widget: "string", required: false }
                      - { label: "Location", name: "location", widget: "string", required: false }
                      - { label: "Type", name: "type", widget: "string", required: false }
                      - { label: "Description", name: "description", widget: "text", required: false }
                      - { label: "URL", name: "url", widget: "string", required: false }

              - name: "committee"
                label: "Committee"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - label: "Members"
                    name: "members"
                    widget: "list"
                    fields:
                      - { label: "Name", name: "name", widget: "string" }
                      - { label: "Role", name: "role", widget: "string", required: false }
                      - { label: "Bio", name: "bio", widget: "text", required: false }
                      - { label: "Email", name: "email", widget: "string", required: false }

              - name: "sponsors"
                label: "Sponsors"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - label: "Sponsors"
                    name: "sponsors"
                    widget: "list"
                    fields:
                      - { label: "Name", name: "name", widget: "string" }
                      - { label: "Description", name: "description", widget: "text", required: false }
                      - { label: "URL", name: "url", widget: "string", required: false }

              - name: "timeline"
                label: "Timeline"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - label: "Items"
                    name: "items"
                    widget: "list"
                    fields:
                      - { label: "Title", name: "title", widget: "string" }
                      - { label: "Description", name: "description", widget: "text", required: false }

              - name: "faq"
                label: "FAQ"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - label: "Items"
                    name: "items"
                    widget: "list"
                    fields:
                      - { label: "Question", name: "question", widget: "string" }
                      - { label: "Answer", name: "answer", widget: "text" }

              - name: "cta"
                label: "Call to action"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Body", name: "body", widget: "text", required: false }
                  - label: "Primary button"
                    name: "primary_button"
                    widget: "object"
                    required: false
                    fields:
                      - { label: "Label", name: "label", widget: "string" }
                      - { label: "URL", name: "url", widget: "string" }
                  - label: "Secondary button"
                    name: "secondary_button"
                    widget: "object"
                    required: false
                    fields:
                      - { label: "Label", name: "label", widget: "string" }
                      - { label: "URL", name: "url", widget: "string" }

              - name: "embed"
                label: "Embed / widget"
                fields:
                  - { label: "ID", name: "id", widget: "string", required: false }
                  - { label: "Eyebrow", name: "eyebrow", widget: "string", required: false }
                  - { label: "Title", name: "title", widget: "string", required: false }
                  - { label: "Subtitle", name: "subtitle", widget: "string", required: false }
                  - { label: "Button label", name: "button_label", widget: "string", required: false }
                  - { label: "URL", name: "url", widget: "string", required: false }

              - name: "socials"
                label: "Socials"

