#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config_path="$(mktemp "${TMPDIR:-/tmp}/a-person-index-claude-mcp.XXXXXX.json")"
trap 'rm -f "$config_path"' EXIT

"$repo_root/scripts/write_claude_mcp_config.sh" "$config_path" >/dev/null

prompt="${1:-Use the configured a-person-index MCP tools, not your prior knowledge. Compare MBTI and Big Five in 3 bullets, then name one relevant program pack and one house motif. Explicitly distinguish source-facing vs house-synthesis.}"

cd "$repo_root"
exec npx -y @anthropic-ai/claude-code \
  -p \
  --permission-mode bypassPermissions \
  --output-format json \
  --mcp-config "$config_path" \
  --strict-mcp-config \
  "$prompt"
