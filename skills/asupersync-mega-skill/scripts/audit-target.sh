#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 /path/to/rust-project" >&2
  exit 1
fi

target="$1"

if [[ ! -d "$target" ]]; then
  echo "error: target directory does not exist: $target" >&2
  exit 1
fi

echo "== Asupersync Migration Inventory =="
echo "target: $target"
echo

echo "== Cargo manifests =="
find "$target" -name Cargo.toml -type f | sort
echo

echo "== Direct source references to Tokio ecosystem =="
rg -n --glob '!*target/*' --glob '!*.lock' \
  '\b(tokio|hyper|axum|reqwest|tower|tower-http|tonic|tokio-util|tokio-stream|sqlx|tokio-postgres|mysql_async|deadpool|bb8|quinn|h3|async-std|smol)\b' \
  "$target" || true
echo

echo "== Dependency declarations in Cargo.toml files =="
rg -n \
  'tokio|hyper|axum|reqwest|tower|tower-http|tonic|tokio-util|tokio-stream|sqlx|tokio-postgres|mysql_async|deadpool|bb8|quinn|h3|async-std|smol' \
  "$target" --glob 'Cargo.toml' || true
echo

if [[ -f "$target/Cargo.toml" ]]; then
  echo "== cargo tree -i tokio (transitive pullers) =="
  (
    cd "$target"
    cargo tree -e normal -i tokio || true
  )
  echo
fi

echo "== Common migration hotspots =="
echo "-- spawn and task ownership --"
rg -n --glob '!*.lock' 'tokio::spawn|spawn_blocking|JoinSet|select!' "$target" || true
echo
echo "-- sync and channels --"
rg -n --glob '!*.lock' 'tokio::sync|mpsc::|oneshot::|broadcast::|watch::|Mutex|RwLock|Semaphore|Notify|Barrier|OnceCell' "$target" || true
echo
echo "-- time and cancellation --"
rg -n --glob '!*.lock' 'tokio::time|sleep\(|timeout\(|interval\(|CancellationToken|abort' "$target" || true
echo
echo "-- web, grpc, db --"
rg -n --glob '!*.lock' 'Router|axum|tonic|reqwest|sqlx|tokio-postgres|mysql_async|deadpool|bb8' "$target" || true
echo

echo "== Suggested next step =="
echo "Pick a lane with /cs/asupersync-mega-skill/references/ADOPTION-LANES.md"

