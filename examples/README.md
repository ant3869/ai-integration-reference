# Runnable Integration Examples

These are **small, functional model-tool loops**, not fake tool-call simulations. They use a safe local `multiply(a,b)` function and return one result per model-requested call. Running the live scripts requires an installed SDK, credentials, network access and a model with function calling enabled. **No paid network tests were run during document authoring.**

| File | SDK | Environment needed | Purpose |
|---|---|---|---|
| `openai_responses_loop.py` | `pip install openai` | `OPENAI_API_KEY`, `OPENAI_MODEL` | Native Responses function loop |
| `anthropic_messages_loop.py` | `pip install anthropic` | `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Native Claude content-block tool loop |
| `gemini_interactions_loop.py` | `pip install google-genai` | `GEMINI_API_KEY`, `GEMINI_MODEL` | Native Gemini interaction step loop |
| `chat_compatible_loop.py` | `pip install openai` | `MODEL_BASE_URL`, `MODEL_ID`, plus `MODEL_API_KEY` for authenticated endpoints | OpenAI-compatible Chat loop: OpenRouter/LM Studio/Meta Chat etc |
| `codex_thread.ts` | `npm install @openai/codex-sdk` | Working Codex auth/config | Codex harness thread run+resume; run with TS runner |
| `claude_agent_sdk.py` | `pip install claude-agent-sdk` | Working Claude Code / Anthropic auth environment | Agent SDK local harness run+final result |
| `normalizer.py` | Python 3.10+ standard library | none | Deterministic **nonstreaming** response normalization |
| `../tests/test_normalizer.py` | Python 3.10+ `unittest` | none | Offline tests for parser/correlator |

**Run Python examples:** `python examples/<name>.py` from the package root after setting variables and installing the correct SDK. Examples intentionally refuse to run when model ID and required API keys aren't provided. For local LM Studio `MODEL_API_KEY` defaults to a harmless local value; if authenticated, set a real key. For Meta Chat, set `MODEL_BASE_URL` to `https://api.meta.ai/v1`, `MODEL_API_KEY` to your Meta Model API credential, and `MODEL_ID` to an enabled Meta model such as `muse-spark-1.3`. Never commit API keys. For OpenRouter: `MODEL_BASE_URL=https://openrouter.ai/api/v1` and its API key.

For the TypeScript Codex example, install a TypeScript runner such as `tsx` (`npm install --save-dev tsx`), then run `npx tsx examples/codex_thread.ts` in a properly authenticated workspace.

**Safety:** the local multiply tool does not write files or invoke shell commands. Adapt the tool registry only after adding schema validation, authorization and idempotent execution as specified in [adapter contract](../architecture/adapter-contract.md).

**Examples are version-sensitive:** run `python -m compileall -q examples tests` and the offline unit suite, then live-probe the installed SDK/models before production use.
