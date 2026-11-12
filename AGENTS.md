# Instructions for coding agents

This repository is a **read-only reference** unless the current user explicitly asks you to improve it. It is not itself a model gateway or runtime.

## Efficient lookup

1. Read [SKILL.md](SKILL.md) first.
2. Choose the integration layer using [DECISION_GUIDE.md](DECISION_GUIDE.md).
3. Read only the matching provider or harness page, plus the relevant protocol page.
4. Refer to [COMPATIBILITY.md](COMPATIBILITY.md) for migrations and [GOTCHAS.md](GOTCHAS.md) for failures.
5. Consult [VALIDATION.md](VALIDATION.md) before claiming a runtime supports a feature.

Do **not** ingest the entire library into the prompt by default. Treat examples as examples, not live-tested deployment proofs. Check current upstream docs and the actual installed versions whenever behavior is version-specific.

## Editing this reference

- Prefer small, source-backed edits to the individual Markdown contract.
- Clearly distinguish documented API claims, local test results, and recommendations.
- Never publish credentials, access tokens, private project configuration, live conversation transcripts, or personal data.
- Preserve relative Markdown links. Run `python -m unittest discover -s tests -v` before committing.
- Do not assert that OpenAI-compatible endpoints, underlying models, and coding harnesses have identical capabilities.
