---
quick_id: 260617-fwl
slug: fix-broken-links-in-index-md-and-scenari
status: complete
completed: 2026-06-17
commit: 32560d4
---

# Summary

Fixed broken kill-chain links on GitHub Pages caused by path flattening in the CI workflow.

## Root cause

`publish.yml` was copying `docs/KILL-CHAINS.md` → `_site/KILL-CHAINS.md` (no `docs/` subdirectory). SCENARIOS.md and SCENARIOS_ES.md use 40 kill-chain links with the form `docs/KILL-CHAINS.md#anchor`, which are correct relative paths in the repo but resolved to a nonexistent path once deployed to GitHub Pages at site root.

The same flattening affected the generated `index.md`, which linked to `KILL-CHAINS.md` without the `docs/` prefix.

## What changed

- `.github/workflows/publish.yml`:
  - `mkdir -p _site` → `mkdir -p _site/docs`
  - `cp docs/KILL-CHAINS.md _site/` → `cp docs/KILL-CHAINS.md _site/docs/`
  - `cp docs/KILL-CHAINS_ES.md _site/` → `cp docs/KILL-CHAINS_ES.md _site/docs/`
  - index.md table links: `KILL-CHAINS.md` → `docs/KILL-CHAINS.md` (both EN and ES)

No changes to SCENARIOS.md, SCENARIOS_ES.md, README.md, or any kill-chain file — their existing `docs/` prefixes were already correct for the repo layout.

## Effect

After next push to main, the GitHub Actions workflow will deploy kill-chain files to `_site/docs/KILL-CHAINS.md` and `_site/docs/KILL-CHAINS_ES.md`, matching the `docs/` prefix that scenario files already use. All 40 kill-chain anchor links will resolve correctly on GitHub Pages.
