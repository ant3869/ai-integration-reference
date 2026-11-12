import { Codex } from "@openai/codex-sdk";

const codex = new Codex();
const thread = codex.startThread();
const first = await thread.run("Inspect the project and identify the highest-priority failing test.");
console.log(first.finalResponse);

const id = thread.id;
if (!id) throw new Error("Codex did not return a thread ID");
const resumed = codex.resumeThread(id);
const second = await resumed.run("Summarize your findings without modifying any files.");
console.log(second.finalResponse);
