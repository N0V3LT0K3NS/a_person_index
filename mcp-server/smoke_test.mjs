import path from "node:path";
import { fileURLToPath } from "node:url";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

const transport = new StdioClientTransport({
  command: "node",
  args: ["mcp-server/server.mjs"],
  cwd: repoRoot,
  stderr: "pipe",
});

if (transport.stderr) {
  transport.stderr.on("data", (chunk) => {
    process.stderr.write(chunk);
  });
}

const client = new Client({
  name: "personality-registry-smoke-test",
  version: "0.1.0",
});

await client.connect(transport);

const tools = await client.listTools();
if (!tools.tools.some((tool) => tool.name === "fetch_protocol_pack")) {
  throw new Error("Expected fetch_protocol_pack tool in MCP surface.");
}

const manifest = await client.readResource({ uri: "registry://manifest" });
if (!manifest.contents?.[0]?.text?.includes("personality-instrument-registry")) {
  throw new Error("Expected registry manifest content.");
}

const prompt = await client.getPrompt({ name: "registry-arrival" });
if (!prompt.messages?.length) {
  throw new Error("Expected registry-arrival prompt messages.");
}

const protocolPack = await client.callTool({
  name: "fetch_protocol_pack",
  arguments: {
    ref: "ILENS",
    frameworks: ["MBTI", "Enneagram"],
  },
});

if (protocolPack.isError) {
  throw new Error(`Protocol pack tool returned error: ${protocolPack.content?.[0]?.text ?? "unknown error"}`);
}

const structured = protocolPack.structuredContent;
if (!structured?.pack || structured.pack.protocol_id !== "proto_ilens") {
  throw new Error("Expected ILENS protocol pack response.");
}

await transport.close();
console.log("MCP smoke test passed.");
