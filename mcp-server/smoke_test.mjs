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
  name: "a-person-index-smoke-test",
  version: "0.1.0",
});

await client.connect(transport);

const tools = await client.listTools();
if (!tools.tools.some((tool) => tool.name === "fetch_protocol_pack")) {
  throw new Error("Expected fetch_protocol_pack tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "fetch_curated_protocol_pack")) {
  throw new Error("Expected fetch_curated_protocol_pack tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "fetch_research_promotion_policy")) {
  throw new Error("Expected fetch_research_promotion_policy tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "list_actualization_protocols")) {
  throw new Error("Expected list_actualization_protocols tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "list_capabilities")) {
  throw new Error("Expected list_capabilities tool in MCP surface.");
}

const manifest = await client.readResource({ uri: "registry://manifest" });
const manifestPayload = JSON.parse(manifest.contents?.[0]?.text ?? "{}");
if (manifestPayload.repository?.name !== "a-person-index") {
  throw new Error("Expected registry manifest content.");
}

const curatedPackIndex = await client.readResource({ uri: "registry://protocol-packs" });
if (!curatedPackIndex.contents?.[0]?.text?.includes("ppk_ilens_core_trait_motive_stack")) {
  throw new Error("Expected protocol-pack catalog content.");
}

const researchPromotion = await client.readResource({ uri: "registry://research-promotion" });
if (!researchPromotion.contents?.[0]?.text?.includes("research_promotion_v0_1")) {
  throw new Error("Expected research promotion resource content.");
}

const actualizationResource = await client.readResource({ uri: "registry://actualization-protocols" });
if (!actualizationResource.contents?.[0]?.text?.includes("A Person Index is often most powerful")) {
  throw new Error("Expected actualization protocol resource content.");
}

const capabilityResource = await client.readResource({ uri: "registry://capability-model" });
if (!capabilityResource.contents?.[0]?.text?.includes("capabilities")) {
  throw new Error("Expected capability model resource content.");
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

const curatedProtocolPack = await client.callTool({
  name: "fetch_curated_protocol_pack",
  arguments: {
    ref: "ppk_ilens_core_trait_motive_stack",
  },
});

if (curatedProtocolPack.isError) {
  throw new Error(
    `Curated protocol pack tool returned error: ${curatedProtocolPack.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (curatedProtocolPack.structuredContent?.catalog_entry?.id !== "ppk_ilens_core_trait_motive_stack") {
  throw new Error("Expected curated protocol pack catalog entry.");
}

const promotionPolicy = await client.callTool({
  name: "fetch_research_promotion_policy",
  arguments: {
    contribution_model: "Mapping Vote",
  },
});

if (promotionPolicy.isError) {
  throw new Error(
    `Research promotion tool returned error: ${promotionPolicy.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (!Array.isArray(promotionPolicy.structuredContent?.promotion_pathways) || !promotionPolicy.structuredContent.promotion_pathways.length) {
  throw new Error("Expected filtered research promotion pathways.");
}

await transport.close();
console.log("MCP smoke test passed.");
