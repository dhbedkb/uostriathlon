
## Phase 3: editor UX simplification

See `PHASE3-NOTES.md` for the full reasoning, including what was
explicitly out of scope and why. Summary of what changed:

| Before (Phase 2)                                    | After (Phase 3)                                              |
|-------------------------------------------------------|------------------------------------------------------------------|
| Tile visibility: `always` / `hover` / `click` / `hidden`      | Tile visibility: `always` / `hidden_initially` / `hidden`             |
| Section `behavior.expand: none/hover/click`               | Section `behavior.expandable: true/false`                            |
| Hover vs click chosen per section                        | One global setting: Site Settings → Interactions → expand trigger      |
| No per-tile override of a grid's reveal mode               | `tile.behavior.expandable: "yes"/"no"` optional override                |
| Site Settings = branding only                              | Site Settings = branding + a real design system (colours, card radius/shadow/padding/image shape, typography, layout), applied via CSS custom properties in `_layouts/default.html` |
| Content order / Visibility objects always expanded in the editor | Both marked `collapsed: true` in `admin/config.yml` — tucked away by default (closest available approximation of "Advanced" without a custom widget) |

### Migrating existing content by hand

Because this was a key rename on a handful of fields (not a new section
shape), it was applied directly to `_data/content/*.yml` rather than
through `scripts/migrate_content.py` (which still emits the pre-Phase-3
key names — see the note at the top of that script). If you have
content on `main` that predates Phase 3, the rename is mechanical:

- `behavior: {expand: none}` → `behavior: {expandable: false}`
- `behavior: {expand: hover}` or `{expand: click}` → `behavior: {expandable: true}`
- Any `visibility: <field>: hover` or `: click` → `visibility: <field>: hidden_initially`

Nothing about section IDs, page URLs, or the Content fields themselves
(`title`, `body`, `image`, etc) changed.
