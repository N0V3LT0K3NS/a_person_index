#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_path="${1:-$repo_root/output/claude-code/a-person-index.mcp.json}"

mkdir -p "$(dirname "$output_path")"

cat >"$output_path" <<EOF
{
  "mcpServers": {
    "a-person-index": {
      "type": "stdio",
      "command": "node",
      "args": ["mcp-server/server.mjs"],
      "cwd": "$repo_root"
    }
  }
}
EOF

printf '%s\n' "$output_path"
