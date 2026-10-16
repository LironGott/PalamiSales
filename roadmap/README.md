# PALAMI Roadmap (shared)

Live: https://claude.ai/artifact/4Lza8QRCXbvVQeDmWdK4Dr (claude.ai artifact, private by default; access is managed in the artifact's Share menu).

| Path | What |
|---|---|
| `index.html` | The app: a Monday-style board (default: table grouped by track, inline editing, "+ add" row per group, details drawer) plus the original timeline as a second tab, now reading and writing a shared artifact database (`db` capability). |
| `source/palami-roadmap-drag.html` | The original file, unchanged (sha256 checked by `tools/extract_seed.py`). |
| `seed/seed.json` | Data extracted from the original: 15 phases, 4 agencies, texts (sales plan etc.). New fields start as "proposal" / empty progress. |
| `tools/extract_seed.py` | Re-extracts `seed/seed.json` from the source file. |

Database layout: `tasks/<id>`, `agencies/<id>`, `plan/texts`, `history/<id>`. Each record has `rev`; the page takes a short lease, re-reads, and writes only if `rev` is unchanged, otherwise it opens a conflict dialog. Deletes are soft (`deleted: true`), so history can restore them.

Permissions are enforced by claude.ai: people invited as Editor can write; Viewers and public-link visitors read only (and only when signed in to claude.ai).
