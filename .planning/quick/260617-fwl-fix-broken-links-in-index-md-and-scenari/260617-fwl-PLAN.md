---
quick_id: 260617-fwl
slug: fix-broken-links-in-index-md-and-scenari
description: Fix broken links in index.md table and scenario kill-chain links on GitHub Pages
date: 2026-06-17
status: complete
must_haves:
  truths:
    - SCENARIOS.md kill-chain links use docs/KILL-CHAINS.md#... (repo-relative, correct locally)
    - GitHub Actions was copying docs/KILL-CHAINS.md → _site/KILL-CHAINS.md (flattened, wrong)
    - index.md was linking to KILL-CHAINS.md without docs/ prefix
  artifacts:
    - .github/workflows/publish.yml (fix: preserve docs/ subdir in _site/)
  key_links:
    - .github/workflows/publish.yml
    - SCENARIOS.md
    - SCENARIOS_ES.md
    - docs/KILL-CHAINS.md
    - docs/KILL-CHAINS_ES.md
---

# Quick Task 260617-fwl: Fix broken links in index.md and scenario kill-chain links

## Root Cause

The GitHub Actions workflow flattened the `docs/` directory structure when building `_site/`:
- `cp docs/KILL-CHAINS.md _site/` → kill-chains land at site root, not in `_site/docs/`
- SCENARIOS.md links via `docs/KILL-CHAINS.md#...` — correct in repo, broken on GitHub Pages
- index.md linked to `KILL-CHAINS.md` (no prefix) — consistent with old flat structure

## Fix (single task)

**Task 1: Fix workflow to preserve docs/ structure**

Files: `.github/workflows/publish.yml`

Action:
- Change `mkdir -p _site` → `mkdir -p _site/docs`
- Change `cp docs/KILL-CHAINS.md _site/` → `cp docs/KILL-CHAINS.md _site/docs/`
- Change optional KILL-CHAINS_ES copy to target `_site/docs/` as well
- Update inline index.md links from `KILL-CHAINS.md` → `docs/KILL-CHAINS.md`

No changes needed to SCENARIOS.md, SCENARIOS_ES.md, or README.md — their existing `docs/` prefixes are already correct.

Verify: `grep -n "docs" .github/workflows/publish.yml` should show kill-chain copies going to `_site/docs/` and index links using `docs/KILL-CHAINS*.md`.

Done: workflow file updated and committed.
