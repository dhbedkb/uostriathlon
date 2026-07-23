
## 10. Phase 3 addendum: editor UX simplification

Phase 3 did not change the model above — Page → Section → Tile →
Content, four section types, one generic tile renderer — per an
explicit instruction not to. It changed how editors *interact* with
that model:

- `tile.visibility.<field>` now has three states (`always` /
  `hidden_initially` / `hidden`) instead of four (`always` / `hover` /
  `click` / `hidden`). A tile no longer decides *how* hidden content is
  revealed, only whether it starts hidden.
- `section.behavior.expand` (`none`/`hover`/`click`) became
  `section.behavior.expandable` (`true`/`false`), with an optional
  per-tile `tile.behavior.expandable` (`"yes"`/`"no"`) override. The
  hover-vs-click mechanism moved to one global setting:
  `site.data.settings.interactions.expand_trigger`.
- `_data/settings.yml` gained a `design` object (colours, card
  radius/shadow/padding/default image shape, typography, layout) that
  `_layouts/default.html` turns into `:root` CSS custom property
  overrides — a real, editable design system, with no new build step.

See `MIGRATION.md` for the practical before/after table and
`PHASE3-NOTES.md` for what was explicitly *not* attempted and why
(preset-conditional field sets/labels, a fully visual "miniature page"
tile editor, and true collapsible Advanced sections all require a
custom Decap CMS widget — real React/JS with its own state machine, not
a config change).
