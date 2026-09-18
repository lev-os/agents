#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
KIT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
IMAGE="${AFK_SMOKE_IMAGE:-debian:bookworm-slim}"

docker info >/dev/null 2>&1 || {
  echo "Docker is required for the smoke test" >&2
  exit 1
}

docker run --rm \
  -v "$KIT_DIR:/kit:ro" \
  "$IMAGE" \
  bash -lc '
    set -euo pipefail
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y sudo curl git ca-certificates npm python3 python3-pip tmux
    /kit/scripts/install.sh --profile core
    source "$HOME/.agent-field-kit/env.sh"
    command -v rg
    command -v tree
    command -v tmux
    command -v npm
    if command -v fd >/dev/null 2>&1; then
      command -v fd
    else
      command -v fdfind
    fi
    echo "agent-field-kit core smoke test passed"
  '
