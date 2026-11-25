#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

tag="$1"

if [[ -z "$tag" && "$GITHUB_REF" == refs/tags/* ]]; then
  tag="$GITHUB_REF"
fi

tag="${tag#refs/tags/}"
tag="${tag#v}"

errors=0

fail() {
  echo "Error: $1" >&2
  errors=$((errors + 1))
}

is_release() {
  [[ "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+(b[0-9]+)?$ ]]
}

is_stable() {
  [[ "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]
}

# The version comes from the tag (setuptools-scm)
if [[ -z "$tag" ]]; then
  echo "Usage: $0 vX.Y.Z[bN]" >&2
  exit 1
fi

if ! is_release "$tag"; then
  fail "Tag 'v$tag' is not a release (expected vX.Y.Z or vX.Y.ZbN)"
fi

if is_stable "$tag" && ! grep -Eq "^## \[${tag//./\\.}\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$" CHANGELOG.md; then
  fail "CHANGELOG.md has no entry for $tag"
fi

if [[ "$errors" -gt 0 ]]; then
  exit 1
fi

echo "Release check passed: $tag"
