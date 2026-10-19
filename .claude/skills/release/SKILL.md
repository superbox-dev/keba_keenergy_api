---
name: release
description: Release or pre-release the library on PyPI (changelog, tag). Use when asked to release, pre-release, tag or bump the version.
---

# Release

- Version from the changelog: breaking → major, `Added`/`Changed` → minor, else patch
- The version comes from the tag (`setuptools-scm`), **never** set it in a file
- `v*` tags publish to PyPI and create the GitHub release
- Ask before pushing, show version, branch and tag

1. `CHANGELOG.md` on `develop`, use the `changelog` skill:
   - pre-release `vX.Y.ZbN`: entries stay under `## [Unreleased]`
   - release `vX.Y.Z`: `## [Unreleased]` becomes `## [X.Y.Z] - YYYY-MM-DD`, a release needs its section
     (the release workflow links the release notes to it)
2. Commit on `develop`, if something changed
3. Pre-release: tag `develop`, push `develop` and the tag
4. Release: merge `develop` into `main`, tag `main`, push `main`, `develop` and the tag
