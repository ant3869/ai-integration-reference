# Files & Multimodal — Payload Format Is Provider/Endpoint Specific

**Rule:** A file path on the agent machine is not automatically visible to a cloud model, and a tool named `read_file` is not the same as a model-native PDF/image input. Plan each upload/reference/transport route independently.

## File transfer checklist

1. **Content kind:** text, image, PDF, audio, video or binary artifact.
2. **Where bytes live:** local harness filesystem, browser, object storage URI, provider Files API, base64 inline, MCP resource.
3. **Accepted request shape:** endpoint-specific typed parts, file ID, upload URI, public URL, etc.
4. **Limits:** size, page/frame duration/count, MIME, resolution, retention, download network rules, cost and feature tiers.
5. **Security:** private URLs/SSRF, signed URI expiration, secrets embedded in documents, upload retention and Contributor/data-use settings.
6. **Response handling:** textual model answer versus returned file/artifact ID; metadata vs bytes; missing/failed frames.

## Quick protocol orientation

| Target | Supported strategy classes to inspect | Do **not** assume |
|---|---|---|
| OpenAI Responses | typed `input_image`/`input_file` content, provider file uploads and references | Chat-style content parts identical to Responses |
| Anthropic Messages | typed image/document blocks, file inputs per API | Raw URL pasted in text means provider fetched it |
| Gemini Interactions | native multimodal input/file service; typed content steps | OpenAI-compat shim exposes all Gemini Files features |
| Gemini generateContent | `inlineData`, `fileData`, File API/URI by supported mode | Can reuse Interactions step schema |
| Meta Model API | endpoint-specific image/video/audio/PDF input; variant support | All Muse versions treat audio with same quality |
| OpenRouter | model/provider file handling or routing plugins; may transform uploads | Every upstream model gets same bytes and citations |
| LM Studio/Ollama | local server/model capabilities; model-specific vision support | Server accepting HTTP JSON implies PDF/video native support |
| Codex/Claude Code/Hermes/OpenClaw harness | file path may be read by authorized built-in filesystem tools | Agent has permission to arbitrary file on caller's computer |
| MCP | `resources/read`, tool results, structured resource content | MCP resources magically become provider file IDs |

## Design recommendation: represent media in app metadata

Use separate logical descriptors:

```json
{
  "kind":"image",
  "source_kind":"local_path|blob|provider_file_id|remote_url|mcp_resource",
  "media_type":"image/png",
  "size_bytes":2048,
  "sha256":"<actual-hash-when-available>",
  "retention_policy":"application-defined",
  "authorization_scope":"application-defined"
}
```

This is an **internal proposed descriptor**; never pass it unchanged as a vendor API payload. Only add a verified remote upload step when the chosen endpoint requires it. The example values are illustrative, not a real uploaded file.

## On failed inputs

Return `unsupported_media_type`, `file_unavailable`, `expired_reference`, `file_too_large`, `permission_denied` or `upload_failed` as distinct errors. Do not silently replace video analysis with a text-only prompt and claim the model viewed frames. If applying frame extraction/transcription as a fallback, label it as a different capability with expected loss and test it.

**Sources:** [OpenAI file inputs](https://developers.openai.com/api/docs/guides/file-inputs), [Anthropic PDF](https://platform.claude.com/docs/en/build-with-claude/pdf-support), [Gemini files](https://ai.google.dev/gemini-api/docs/file-inputs), [Meta models](https://dev.meta.ai/docs/models), [OpenRouter files](https://openrouter.ai/docs/guides/features/files), [MCP resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).
