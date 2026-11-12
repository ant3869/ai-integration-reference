"""Generate a single-file reading copy from the modular Markdown reference."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = [
    "README.md", "SKILL.md", "AGENTS.md", "DECISION_GUIDE.md",
    "COMPATIBILITY.md", "GOTCHAS.md", "VALIDATION.md",
    "architecture/adapter-contract.md", "architecture/session-and-events.md",
    "protocols/tool-calls.md", "protocols/mcp.md",
    "protocols/files-and-multimodal.md", "protocols/streaming-and-output.md",
    "providers/openai.md", "providers/anthropic.md", "providers/gemini.md",
    "providers/meta.md", "providers/openrouter.md", "providers/local.md",
    "providers/secondary.md", "harnesses/codex.md", "harnesses/claude-code.md",
    "harnesses/hermes.md", "harnesses/openclaw.md",
    "harnesses/code-puppy.md", "harnesses/other-harnesses.md",
    "examples/README.md", "SOURCES.md",
]


def anchor(path: str) -> str:
    return path.lower().replace("/", "-").replace(".", "")


def render() -> str:
    parts = [
        "# AI Integration Reference — Single-File Edition\n\n",
        "> As of **2026-11-11**. This is an all-in-one reading copy. "
        "For agent workloads, prefer `SKILL.md` and load selected modular pages. "
        "Relative links inside embedded pages refer to their original paths.\n\n",
        "## Contents\n",
    ]
    parts.extend(f"- [{path}](#{anchor(path)})\n" for path in ORDER)
    for path in ORDER:
        page = ROOT / path
        if not page.is_file():
            raise FileNotFoundError(page)
        parts.append(
            f'\n---\n\n<a id="{anchor(path)}"></a>\n'
            f'<!-- SOURCE FILE: {path} -->\n## {path}\n\n'
            + page.read_text(encoding="utf-8").rstrip() + "\n"
        )
    return "".join(parts)


def main() -> None:
    (ROOT / "AI_INTEGRATION_MASTER_REFERENCE.md").write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
