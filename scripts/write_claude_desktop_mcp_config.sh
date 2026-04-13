#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_path="${1:-$HOME/Library/Application Support/Claude/claude_desktop_config.json}"
node_bin="${2:-$(command -v node)}"

if [[ -z "${node_bin}" ]]; then
  printf 'Could not find node on PATH.\n' >&2
  exit 1
fi

mkdir -p "$(dirname "$target_path")"

python3 - "$target_path" "$repo_root" "$node_bin" <<'PY'
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

target = Path(sys.argv[1])
repo_root = sys.argv[2]
node_bin = sys.argv[3]

if target.exists():
    backup = target.with_suffix(target.suffix + f".bak.{datetime.now().strftime('%Y%m%d%H%M%S')}")
    shutil.copy2(target, backup)
    data = json.loads(target.read_text(encoding="utf-8"))
else:
    data = {}

data.setdefault("mcpServers", {})
data["mcpServers"]["a-person-index"] = {
    "command": node_bin,
    "args": ["mcp-server/server.mjs"],
    "cwd": repo_root,
}
data.setdefault("preferences", {})

target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print(target)
PY
