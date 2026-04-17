"""
Claude CLI helper — routes LLM calls through the `claude` CLI binary
instead of the Anthropic SDK (no ANTHROPIC_API_KEY needed).
"""
from __future__ import annotations
import json
import os
import subprocess
import tempfile
from pathlib import Path

# Locate the claude binary
_CLAUDE_PATH = os.environ.get(
    "CLAUDE_BIN",
    "/home/codespace/.vscode-remote/extensions/"
    "anthropic.claude-code-2.1.109-linux-x64/resources/native-binary/claude"
)


def _find_claude() -> str:
    """Return path to claude binary, raising if not found."""
    if Path(_CLAUDE_PATH).is_file():
        return _CLAUDE_PATH
    # Try PATH
    import shutil
    found = shutil.which("claude")
    if found:
        return found
    raise FileNotFoundError(
        f"claude binary not found at {_CLAUDE_PATH}. "
        "Set CLAUDE_BIN env var or ensure the binary is on PATH."
    )


def call_claude(prompt: str, system: str = "", model: str = "claude-sonnet-4-6",
                max_tokens: int = 4096) -> str:
    """
    Call the claude CLI with `-p` (print mode) and return the response text.

    Args:
        prompt:     User message / prompt text
        system:     Optional system prompt (prepended to prompt if provided)
        model:      Model identifier (ignored by CLI but kept for signature compat)
        max_tokens: Max tokens hint (ignored by CLI)

    Returns:
        Response text from Claude
    """
    binary = _find_claude()

    full_prompt = prompt
    if system:
        full_prompt = f"[SYSTEM INSTRUCTIONS]\n{system}\n\n[USER]\n{prompt}"

    # Write prompt to a temp file to avoid shell quoting issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8") as tf:
        tf.write(full_prompt)
        tmp_path = tf.name

    try:
        result = subprocess.run(
            [binary, "-p", full_prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0 and result.stderr:
            raise RuntimeError(f"claude CLI error: {result.stderr.strip()}")
        return result.stdout.strip()
    finally:
        os.unlink(tmp_path)


def call_claude_json(prompt: str, system: str = "", **kwargs) -> dict | list:
    """
    Like call_claude() but strips markdown fences and JSON-parses the response.
    """
    raw = call_claude(prompt, system=system, **kwargs)
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)
