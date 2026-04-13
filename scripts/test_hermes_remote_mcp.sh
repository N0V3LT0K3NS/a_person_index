#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  printf 'Usage: %s <user@host> [remote_repo_dir]\n' "$(basename "$0")" >&2
  exit 1
fi

target="$1"
remote_repo_dir="${2:-}"
default_prompt="Use the configured a-person-index MCP tools, not your prior knowledge. Compare MBTI and Big Five in 4-6 bullet points, then name one relevant program pack and one relevant house motif. Be explicit about which parts are source-facing vs house synthesis."

repo_arg="$(printf '%q' "$remote_repo_dir")"
prompt_arg="$(printf '%q' "$default_prompt")"

ssh "$target" "bash -s -- $repo_arg $prompt_arg" <<'EOF'
set -euo pipefail

repo_dir="${1:-}"
if [[ -z "$repo_dir" ]]; then
  repo_dir="$HOME/workspace/a_person_index"
fi
prompt="${2:?missing prompt}"
wrapper_path="$HOME/bin/a-person-index-mcp"
node_bin="$HOME/.hermes/node/bin/node"
npm_bin="$HOME/.hermes/node/bin/npm"

export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

mkdir -p "$(dirname "$repo_dir")" "$HOME/bin"

if [[ ! -d "$repo_dir/.git" ]]; then
  git clone https://github.com/N0V3LT0K3NS/a_person_index.git "$repo_dir"
else
  git -C "$repo_dir" checkout main >/dev/null 2>&1 || true
  git -C "$repo_dir" pull --ff-only
fi

cd "$repo_dir"

python3 -m venv .venv
.venv/bin/pip install --upgrade pip >/dev/null
.venv/bin/pip install -e . >/dev/null

if [[ ! -x "$node_bin" || ! -x "$npm_bin" ]]; then
  printf 'Hermes bundled Node was not found at %s\n' "$HOME/.hermes/node/bin" >&2
  exit 1
fi

PATH="$HOME/.hermes/node/bin:$PATH" "$npm_bin" install >/dev/null

cat >"$wrapper_path" <<WRAPPER
#!/usr/bin/env bash
set -euo pipefail
cd "$repo_dir"
export PATH="$HOME/.hermes/node/bin:\$PATH"
exec "$node_bin" mcp-server/server.mjs
WRAPPER
chmod +x "$wrapper_path"

if ! hermes mcp list 2>/dev/null | grep -q 'a-person-index'; then
  printf 'Y\n' | hermes mcp add a-person-index --command "$wrapper_path"
fi

hermes mcp test a-person-index
hermes chat -Q -q "$prompt"
EOF
