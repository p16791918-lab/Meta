"""
Claude CLI helper — routes LLM calls through the `claude` CLI binary
instead of the Anthropic SDK (no ANTHROPIC_API_KEY needed).
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


def extract_json(raw: str):
    """
    Parse JSON from an LLM/CLI response robustly.

    Handles the common ways the model wraps its answer:
      - ```json ... ``` code fences
      - leading prose before the JSON
      - trailing prose AFTER the JSON ("Extra data" errors)
      - multiple values (returns the first complete array/object)
    """
    s = (raw or "").strip()
    s = re.sub(r"^```(?:json)?", "", s).strip()
    s = re.sub(r"```$", "", s).strip()

    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass

    # Scan for the first '[' or '{' and decode a single complete value there,
    # ignoring anything the model appended afterwards.
    decoder = json.JSONDecoder()
    for i, ch in enumerate(s):
        if ch in "[{":
            try:
                obj, _ = decoder.raw_decode(s[i:])
                return obj
            except json.JSONDecodeError:
                continue
    raise json.JSONDecodeError("No JSON value found in response", s, 0)

# Optional explicit override
_CLAUDE_PATH = os.environ.get("CLAUDE_BIN", "")

# VS Code / Codespaces bundle the CLI inside the extension folder, whose version
# number changes on every auto-update — so glob for it rather than hardcoding.
_EXT_GLOBS = [
    os.path.expanduser("~/.vscode-remote/extensions/"
                       "anthropic.claude-code-*/resources/native-binary/claude"),
    os.path.expanduser("~/.vscode-server/extensions/"
                       "anthropic.claude-code-*/resources/native-binary/claude"),
    "/home/codespace/.vscode-remote/extensions/"
    "anthropic.claude-code-*/resources/native-binary/claude",
]


def _find_claude() -> str:
    """Return path to the claude binary, robust to extension version changes."""
    import glob
    import shutil

    # 1) explicit override
    if _CLAUDE_PATH and Path(_CLAUDE_PATH).is_file():
        return _CLAUDE_PATH
    # 2) on PATH
    found = shutil.which("claude")
    if found:
        return found
    # 3) any installed extension version (newest wins)
    for pattern in _EXT_GLOBS:
        matches = sorted(glob.glob(pattern))
        if matches:
            return matches[-1]
    raise FileNotFoundError(
        "claude binary not found. Install Claude Code, put `claude` on PATH, "
        "or set CLAUDE_BIN to its full path."
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
    return extract_json(raw)
