from __future__ import annotations

import subprocess


def test_mcp_smoke(repo_root):
    result = subprocess.run(
        ["npm", "run", "mcp:smoke"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "MCP smoke test passed." in result.stdout
