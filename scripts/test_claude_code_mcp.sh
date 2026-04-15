#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/a-person-index-claude-mcp.XXXXXX")"
config_path="$temp_dir/config.json"
trap 'rm -rf "$temp_dir"' EXIT

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
