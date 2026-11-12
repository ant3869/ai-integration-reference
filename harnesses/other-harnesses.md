# Other Major Harnesses — Orientation (Not Exhaustive)

This keeps the reference broad without sprawling into forks and niche derivatives. **Full integration specifications should be added only when the harness becomes an actual target.**

## Gemini CLI

Google's open-source terminal coding assistant is distinct from Gemini native inference APIs. It provides an agent/harness experience with tools and sessions. For integration, inspect the official CLI's installed `--help`, headless/JSON output interface and any supported SDK/ACP interface; do not assume raw Gemini Interactions endpoints expose the CLI's filesystem tools. [Project](https://github.com/google-gemini/gemini-cli).

## Muse Code

Meta describes a coding-agent CLI (`muse`) as a separate execution system backed by Meta Model API (Muse Spark, and some other model variants), with sandbox and approval functions. Raw Model API calls do **not** automatically gain Muse Code's shell/file tools. Inspect current Muse Code CLI docs for headless/session mode before wiring into a product. [Meta overview](https://dev.meta.ai/docs/overview).

## OpenAI Agents SDK / hosted agents

These are **additional layers** beyond OpenAI Responses and beyond Codex; avoid treating an Agents SDK run or hosted Agents API session as a Codex SDK thread. Agent orchestration/observability, built-in tools and hosted sandbox support are feature- and product-specific. [OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents), [OpenAI Agents SDK Python](https://openai.github.io/openai-agents-python/).

## GitHub Copilot CLI / IDE agent

Treat as its own agent harness, potentially mediated by IDE/auth and repo/organization policies. Do not borrow CLI args, tool schemas or event formats from Claude Code or Codex without verification. [GitHub Copilot](https://docs.github.com/en/copilot).

## When to promote a harness to Tier 1

Document a stable programmatic interface, actual tool ownership and permission rules, session IDs and resume semantics, lifecycle event mapping, cancellation, error semantics and live contract tests. Avoid adding a provider merely because it has a popular CLI.
