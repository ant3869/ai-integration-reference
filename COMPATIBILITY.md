# Compatibility Matrix — Wire Contracts, Not Marketing Labels

**Interpreting this table:** a documented surface exists; individual model/route feature support is **probe required**. A dash is not proof that an implementation cannot support a feature—it means this reference does not affirm it.

| Target | Primary surface | Client tool declaration | Model requests tool | Return tool result | Context continuation |
|---|---|---|---|---|---|
| OpenAI Responses | `POST /v1/responses` | `tools: [{type:function,name,parameters,...}]` | `output[]` item `type:function_call`, `call_id`, JSON-string `arguments` | `input[]:{type:function_call_output,call_id,output}` | `previous_response_id` or full item replay |
| OpenAI Chat | `POST /v1/chat/completions` | `tools:[{type:function,function:{name,parameters}}]` | `choices[].message.tool_calls[]` with `id`,`function.arguments` JSON string | `role:tool,tool_call_id,content` | Client resends `messages` |
| Anthropic Claude Messages | `POST /v1/messages` | `tools:[{name,description,input_schema}]` | assistant `content[]` `type:tool_use,id,input` object | next **user** message with `type:tool_result,tool_use_id` | Re-send history; optional **beta message threads** with TTL/replay |
| Gemini Interactions | `/v1beta/interactions` | `tools:[{type:function,name,parameters,...}]` | `steps[]` `type:function_call,id,arguments` | `input:[{type:function_result,call_id,name,result:[...]}]` | `previous_interaction_id` or exact history replay |
| Gemini generateContent (legacy, supported) | `models/*:generateContent` | `tools:functionDeclarations` | `candidates[].content.parts[].functionCall` | `functionResponse` parts | Full `contents`; preserve `thoughtSignature` on manual replay |
| Meta Model API Responses | `/v1/responses` | OpenAI-Responses-shaped | `function_call` + `call_id` | `function_call_output` | `previous_response_id` or encrypted replay |
| Meta Model API Chat | `/v1/chat/completions` | Chat-shaped | Chat `tool_calls` | Chat `role:tool` | Client history |
| OpenRouter Chat / Responses | OpenRouter APIs | OpenAI-style, depending on endpoint | Contract depends on selected endpoint and upstream | Endpoint-specific | History / route-specific; probe failover |
| Ollama native | `/api/chat` | Chat-style tools | `message.tool_calls[].function.arguments` **object** | `role:tool,tool_name,content` | Client history |
| LM Studio OpenAI-compatible | `/v1/chat/completions`; `/v1/responses` | Supported compatibility subset | Parsed model output/tool call events | Match selected endpoint | Endpoint- and model-dependent |
| Codex harness | SDK / app-server / `codex exec` | Harness-provided + configured tools | Harness events | Harness owns execution | Codex thread ID |
| Claude Code harness | Agent SDK / `claude -p` | Harness tools + MCP | SDK messages / structured events | Harness owns execution / SDK custom MCP | Agent SDK session ID |
| Hermes harness | REST session API / ACP / TUI RPC / Chat-compatible | Harness tools + MCP | `tool.started` etc in stream | Harness owns execution | Hermes session ID / gateway session key |
| OpenClaw harness | Gateway RPC / opt-in HTTP Chat/Responses / tools invoke | Configured agent tools | Gateway agent events | Gateway / `tools/invoke` | Gateway session key / `user` routing |

## Different meanings of 'state'

| Token | Object | Scope | Gotcha |
|---|---|---|---|
| `call_id`, `tool_call_id`, `tool_use_id` | Tool **invocation** | One model tool request | NEVER substitute another call ID; parallel calls differ |
| `previous_response_id` | Prior Responses turn | Provider API conversation | Not a Codex thread/session |
| `previous_interaction_id` | Prior Gemini Interaction | Gemini Interactions | Repeat interaction-level `tools`/instructions/config on new turns |
| Claude Message `thread.previous_message_id` | Short-lived beta Message thread | Claude API | Expires; keep full replay history |
| Codex `thread.id` | Harness conversation | Local Codex | SDK/app-server or CLI should own thread persistence |
| Claude Agent SDK `session_id` | Harness conversation | Locally stored Claude Code session | Not Anthropic Messages API state |
| Hermes `session_id` | Harness conversation | Hermes SessionDB | Keep distinct from gateway conversation key |
| OpenClaw `sessionKey` | Agent conversation | Gateway | `model` can select agent, not underlying LLM |
| `Mcp-Session-Id` | MCP transport/session | MCP connection | Does NOT resume model history |

## Tool execution truth table

| Tool class | Who runs it? | Who owes a tool result? |
|---|---|---|
| OpenAI/Claude/Gemini/Meta **custom function** | Your application (or explicit configured executor) | Your application via native protocol |
| Provider-managed web search, code execution etc | Provider | Usually provider; exceptions and pause states are provider-specific |
| Harness built-in shell, edit, browser, delegated subagent | Harness | Harness internally; integrate events and approval boundary |
| MCP server tool | MCP server, invoked by a capable client/host | MCP client/host; bridge if using it as an LLM-defined function |
| OpenClaw direct `/tools/invoke` | OpenClaw Gateway | HTTP JSON result to invoking client |

## Capability matrix: never use binary shortcuts

Track these per **target+model+protocol+version+config**:

`tools.client`, `tools.server`, `tools.parallel`, `tools.stream_arguments`, `structured_output.strict`, `reasoning.preserves_state`, `input.image`, `input.pdf`, `input.audio`, `input.video`, `streaming`, `session.resume`, `session.fork`, `approval.interactive`, `tool.mcp`, `cancellation`.

Use `unknown` until docs and a runtime probe establish support. Reference documentation is not a live feature certification. See [VALIDATION.md](VALIDATION.md).
