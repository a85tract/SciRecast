#!/usr/bin/env bash
#
# Install SciRecast's submodule-safety hooks.
#
#   pre-push    -> the superproject: refuses to publish a gitlink that is not
#                  on the submodule's remote
#   post-commit -> every initialized submodule: reminds you to bump the
#                  superproject after you commit inside one
#
# Usage: tools/install-hooks.sh
# Uninstall: rm .git/hooks/pre-push and .git/modules/*/hooks/post-commit
#
# Hooks are symlinked where the filesystem allows, so editing hooks/ updates
# every installed copy.

set -euo pipefail

SUPER="$(git rev-parse --show-toplevel)"
SELF="$(cd "$(dirname "$0")/.." && pwd)"

link() {  # link <source> <destination>
    mkdir -p "$(dirname "$2")"
    ln -sf "$1" "$2" 2>/dev/null || cp "$1" "$2"
    chmod +x "$2" 2>/dev/null || true
}

chmod +x "$SELF/hooks/pre-push" "$SELF/hooks/post-commit" 2>/dev/null || true

SUPER_HOOKS="$(git -C "$SUPER" rev-parse --absolute-git-dir)/hooks"
link "$SELF/hooks/pre-push" "$SUPER_HOOKS/pre-push"
echo "installed  pre-push     -> $SUPER_HOOKS/pre-push"

# Every initialized submodule, at any depth.
git -C "$SUPER" submodule foreach --recursive --quiet '
    hooks="$(git rev-parse --absolute-git-dir)/hooks"
    mkdir -p "$hooks"
    ln -sf "'"$SELF"'/hooks/post-commit" "$hooks/post-commit" 2>/dev/null \
      || cp "'"$SELF"'/hooks/post-commit" "$hooks/post-commit"
    chmod +x "$hooks/post-commit" 2>/dev/null || true
    echo "installed  post-commit  -> $hooks/post-commit"
'

echo
echo "Re-run this after adding or initializing a submodule."
