# Phase 3 notes: what's real, what's not, and why

`ARCHITECTURE.md` describes the Page → Section → Tile → Content model
(unchanged, kept exactly as-is per the brief). This file is the honest
account of the Phase 3 "editor UX" work: what changed, what's genuinely
achievable inside stock Decap CMS, and what isn't.

## What Phase 3 actually changed

1. **Visibility simplified.** Each piece of tile content is now
   `Always visible` / `Hidden initially` / `Hidden` — three states,
   plain English. The old model exposed `always` / `hover` / `click` /
   `hidden` per field, which conflated "does this start hidden" with
   "how is it revealed."
2. **Hover vs click is one site-wide setting, not a per-section
   choice.** `Site Settings → Interactions → "How hidden content is
   revealed"` now governs every expandable grid on the site. A Section
   just says `Expandable: yes/no`; a Tile can override that with a
   plain `yes/no/inherit`. Nobody editing a single FAQ block has to
   understand or pick a trigger mechanism.
3. **Site Settings is now a real design system.** Colours, card
   radius/shadow/padding/default image shape, heading weight, body
   text density, page width, grid gap, and vertical section spacing are
   all editable there and take effect across the whole site via CSS
   custom properties set in `_layouts/default.html` — no CSS or code
   edit required to reskin the site.
4. **Drag-and-drop content ordering already existed** (the `content_order`
   field is a Decap `list` widget, which is natively drag-reorderable)
   and is unchanged — it was already the drag-and-drop ordering
   mechanism the brief asks for.
5. The generic Page → Section → Tile → Content model, the single
   `tile.html`/`tile-grid.html` renderer, and the existing migration
   work are all untouched, per the brief's explicit instruction not to
   redo the architecture.

## What the brief asked for that this does NOT deliver, and why

The brief's core ask — presets that change the *actual fields and their
labels/placeholders* shown to the editor ("Full Name" for a committee
member vs. "Organisation Name" for a sponsor), a fully "miniature page"
visual editing surface, and true collapsible `▼ Advanced` sections — run
into one real, structural limitation:

**Decap CMS resolves a collection's field schema once, from static
YAML. It has no built-in way to change which fields appear, what
they're labelled, or what their placeholder text is, based on the value
of a sibling field** (like `preset`). This isn't a config oversight —
it's mentioned explicitly in this repo's own `MIGRATION.md` from before
Phase 3 started, for the same reason: Decap has no "conditional fields"
concept without writing and registering a **custom field widget** — a
hand-built React component with its own state machine, not a schema
change.

That's a real, buildable thing (this repo already proves the general
technique works: `admin/crop-preview.js` registers a custom **preview**
template using Decap's plain-script `createClass`/`h` API, no build
step required) — but a custom *editing* widget that redraws its whole
form per-preset, handles placeholder-vs-value semantics, drag reordering
inside itself, and a collapsible "Advanced" region, is a genuinely
separate, non-trivial piece of software. Writing an untested first draft
of that inside this pass, on top of everything else, risks shipping
something that looks plausible in the config but breaks in the actual
Decap runtime — which is worse than being upfront that it needs its own
dedicated build-and-test cycle.

Concretely, still open if you want to pursue it:

- **#1 Preset-specific fields/labels/placeholders** — needs a custom
  Decap widget.
- **#2 "Miniature page" visual tile editor** — needs a custom widget;
  `admin/crop-preview.js` is the closest existing prior art in this
  repo.
- **#6/#7 True collapsible `▼ Advanced` field groups and a curated
  section-editing workflow** — Decap's `object`/`list` widgets support
  `collapsed: true` (used in `admin/config.yml` for Content order and
  Visibility, so they're tucked away by default), which gets you most
  of the way there without custom code. A true expand/collapse *toggle
  the editor controls at will*, beyond Decap's built-in collapse-on-load
  behaviour, still needs a custom widget.

If any of these are the priority, the right next step is scoping and
building one custom Decap widget at a time, starting with whichever
preset (Committee is probably highest-value) matters most — rather than
guessing at all of them in one pass.
