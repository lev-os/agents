#!/usr/bin/env bash
# dispatch — Unified CLI+API model dispatch. Send a prompt to any provider.
# Part of agent-field-kit. Sources model-cache.sh for provider discovery.
#
# Usage:
#   dispatch <provider> <model> <prompt> <outfile>
#   dispatch anthropic claude-sonnet-4-6 "What is 2+2?" /tmp/out.md
#   dispatch claude-cli claude "Fix the bug" /tmp/out.md
#
# API providers use curl. CLI providers use timeout + runner binary.

set -euo pipefail

DISPATCH_TIMEOUT="${DISPATCH_TIMEOUT:-120}"

# ═══════════════════════════════════════════════════════════════
# API Dispatchers (curl-based, zero SDK dependency)
# ═══════════════════════════════════════════════════════════════

dispatch_anthropic() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.content[0].text // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_openai() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://api.openai.com/v1/chat/completions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.choices[0].message.content // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_google() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s "https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=$GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" '{
      contents: [{parts: [{text: $p}]}]
    }')" | jq -r '.candidates[0].content.parts[0].text // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_xai() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://api.x.ai/v1/chat/completions \
    -H "Authorization: Bearer $XAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.choices[0].message.content // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_openrouter() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.choices[0].message.content // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_groq() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://api.groq.com/openai/v1/chat/completions \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.choices[0].message.content // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_deepseek() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://api.deepseek.com/chat/completions \
    -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.choices[0].message.content // .error.message // "ERROR"' > "$outfile" 2>&1
}

dispatch_perplexity() {
  local prompt="$1" model="$2" outfile="$3"
  curl -s https://api.perplexity.ai/chat/completions \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --arg m "$model" '{
      model: $m, max_tokens: 4096,
      messages: [{role: "user", content: $p}]
    }')" | jq -r '.choices[0].message.content // .error.message // "ERROR"' > "$outfile" 2>&1
}

# ═══════════════════════════════════════════════════════════════
# CLI Dispatchers
# ═══════════════════════════════════════════════════════════════

dispatch_cli_claude() {
  local prompt="$1" outfile="$2"
  timeout "$DISPATCH_TIMEOUT" claude -p --output-format text "$prompt" > "$outfile" 2>&1 || echo "TIMEOUT/ERROR (exit $?)" >> "$outfile"
}

dispatch_cli_codex() {
  local prompt="$1" outfile="$2"
  timeout "$DISPATCH_TIMEOUT" codex -q "$prompt" > "$outfile" 2>&1 || echo "TIMEOUT/ERROR (exit $?)" >> "$outfile"
}

dispatch_cli_gemini() {
  local prompt="$1" outfile="$2"
  timeout "$DISPATCH_TIMEOUT" gemini "$prompt" > "$outfile" 2>&1 || echo "TIMEOUT/ERROR (exit $?)" >> "$outfile"
}

dispatch_cli_agent() {
  local prompt="$1" outfile="$2"
  timeout "$DISPATCH_TIMEOUT" agent -p --yolo --trust "$prompt" > "$outfile" 2>&1 || echo "TIMEOUT/ERROR (exit $?)" >> "$outfile"
}

# ═══════════════════════════════════════════════════════════════
# Unified Dispatcher
# ═══════════════════════════════════════════════════════════════

dispatch() {
  local provider="$1" model="$2" prompt="$3" outfile="$4"

  case "$provider" in
    anthropic)    dispatch_anthropic "$prompt" "$model" "$outfile" ;;
    openai)       dispatch_openai "$prompt" "$model" "$outfile" ;;
    google)       dispatch_google "$prompt" "$model" "$outfile" ;;
    xai)          dispatch_xai "$prompt" "$model" "$outfile" ;;
    openrouter)   dispatch_openrouter "$prompt" "$model" "$outfile" ;;
    groq)         dispatch_groq "$prompt" "$model" "$outfile" ;;
    deepseek)     dispatch_deepseek "$prompt" "$model" "$outfile" ;;
    perplexity)   dispatch_perplexity "$prompt" "$model" "$outfile" ;;
    fireworks)    dispatch_openai "$prompt" "$model" "$outfile" ;;  # OpenAI-compatible
    claude-cli)   dispatch_cli_claude "$prompt" "$outfile" ;;
    codex-cli)    dispatch_cli_codex "$prompt" "$outfile" ;;
    gemini-cli)   dispatch_cli_gemini "$prompt" "$outfile" ;;
    cursor-cli)   dispatch_cli_agent "$prompt" "$outfile" ;;
    *) echo "Unknown provider: $provider" > "$outfile"; return 1 ;;
  esac
}

# ═══════════════════════════════════════════════════════════════
# CLI Entry
# ═══════════════════════════════════════════════════════════════

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  if [[ $# -lt 4 ]]; then
    echo "dispatch — Send a prompt to any AI provider"
    echo ""
    echo "Usage: dispatch <provider> <model> <prompt> <outfile>"
    echo ""
    echo "API:  dispatch anthropic claude-sonnet-4-6 'Hello' /tmp/out.md"
    echo "CLI:  dispatch claude-cli claude 'Fix bug' /tmp/out.md"
    echo ""
    echo "Env: DISPATCH_TIMEOUT (default 120s)"
    exit 1
  fi
  dispatch "$@"
fi
