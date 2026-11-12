# Code Puppy — Python CLI Coding Agent

**Priority:** Tier 1 user stack, but a lighter integration contract than Codex/Claude SDKs · **Project docs checked:** 2026-11-11.

## Documented features

Code Puppy is a CLI-first, Python-based open-source coding agent with file/shell tools, agent profiles, provider switching, MCP integration and autosaved/resumable sessions.

- Launch interactive CLI with `code-puppy`; official installation via `pip install code-puppy` or `uvx code-puppy`.
- In CLI: `/agent <name>`, `/model <name>`, `/tools`, `/mcp list`, `/session`, `/resume`, `/compact`.
- Project-specific `AGENT.md` may define local instructions; custom agents are JSON-based under `~/.code_puppy/agents/`.
- Custom model definitions/config use `~/.code_puppy/extra_models.json` and app config; actual per-provider API behavior is determined by its adapter and model.

## Backend integration recommendation

**Do not assume a stable programmatic RPC/session protocol solely from the existence of an interactive CLI.** When embedding into a product, inspect exact installed source/docs for noninteractive mode, machine-readable output, session restoration and cancellation flags. If absent, treat it as **interactive-only / experimental subprocess integration** and expose capabilities conservatively.

For a temporary subprocess bridge:

1. Check `code-puppy --help` from installed version for noninteractive input/output modes.
2. Run in an explicit working directory and constrained environment; persist config/model/agent identity.
3. Capture stdout/stderr/exit code separately. Do not parse human-facing colorized output as authoritative structured protocol.
4. Manage approvals; no unattended broad shell access.
5. Resume an autosaved session only via the version's documented session mechanism, after validating the workspace.

## Best extension surface

MCP for external tools and custom agents for structured roles are documented. Different model providers may have different tool function and tool-result behavior; inspect which provider adapter Code Puppy uses before applying raw provider-specific patches.

## Do not assume

- Stable HTTP API, JSON-RPC server, or SDK with Codex-equivalent event types.
- Ability to resume an exact in-flight tool operation from a CLI transcript.
- Global tool support merely because its model catalog lists a model.

**Sources:** [Code Puppy](https://code-puppy.dev/), [Commands](https://code-puppy.dev/pages/commands.html), [Configuration](https://code-puppy.dev/pages/configuration.html), [Custom agents](https://code-puppy.dev/pages/custom-agents.html).
