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
  name: "a-person-index-contract-test",
  version: "0.1.0",
});

function expect(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

await client.connect(transport);

const tools = await client.listTools();
const toolNames = new Set(tools.tools.map((tool) => tool.name));
for (const requiredTool of [
  "orient_agent",
  "compare_frameworks",
  "trace_to_motifs",
  "fetch_protocol_spec",
  "list_protocol_packs",
  "fetch_protocol_pack_summary",
  "fetch_protocol_pack",
  "fetch_result_atom_schema",
  "fetch_research_models",
]) {
  expect(toolNames.has(requiredTool), `Expected ${requiredTool} in MCP tool surface.`);
}

const manifest = await client.readResource({ uri: "registry://manifest" });
const manifestPayload = JSON.parse(manifest.contents?.[0]?.text ?? "{}");
expect(manifestPayload.interfaces?.mcp?.entrypoint === "npm run mcp:serve", "Expected MCP manifest entrypoint.");
expect(manifestPayload.interfaces?.mcp?.contract_test === "npm run mcp:contract", "Expected MCP contract test entry.");

const currentState = await client.readResource({ uri: "registry://current-state" });
expect(currentState.contents?.[0]?.text?.includes("read-only MCP adapter"), "Expected current state to mention MCP adapter.");

const quickstart = await client.readResource({ uri: "registry://quickstart" });
expect(quickstart.contents?.[0]?.text?.includes("First moves"), "Expected quickstart resource content.");

const ilensWalkthrough = await client.readResource({ uri: "registry://ilens-walkthrough" });
expect(
  ilensWalkthrough.contents?.[0]?.text?.includes("Recommended MCP sequence"),
  "Expected ILENS walkthrough resource content.",
);

const mbtiResource = await client.readResource({ uri: "registry://instrument/mbti" });
const mbtiPayload = JSON.parse(mbtiResource.contents?.[0]?.text ?? "{}");
expect(mbtiPayload.instrument?.id === "instr_mbti", "Expected MBTI resource payload.");

const curatedPack = await client.readResource({
  uri: "registry://protocol-pack/ppk_ilens_core_trait_motive_stack",
});
const curatedPackPayload = JSON.parse(curatedPack.contents?.[0]?.text ?? "{}");
expect(
  curatedPackPayload.catalog_entry?.id === "ppk_ilens_core_trait_motive_stack",
  "Expected curated pack resource payload.",
);

const compare = await client.callTool({
  name: "compare_frameworks",
  arguments: {
    left: "MBTI",
    right: "Big Five",
  },
});
expect(!compare.isError, "Expected compare_frameworks tool to succeed.");
expect(compare.structuredContent?.left?.id === "instr_mbti", "Expected compare left instrument.");
expect(compare.structuredContent?.right?.id === "instr_big_five", "Expected compare right instrument.");
expect(
  Array.isArray(compare.structuredContent?.suggested_next_queries) &&
    compare.structuredContent.suggested_next_queries.length >= 2,
  "Expected compare to include suggested next queries.",
);

const orientation = await client.callTool({
  name: "orient_agent",
  arguments: {},
});
expect(!orientation.isError, "Expected orient_agent tool to succeed.");
expect(
  Array.isArray(orientation.structuredContent?.available_framework_refs) &&
    orientation.structuredContent.available_framework_refs.length >= 16,
  "Expected orientation framework refs.",
);
expect(
  orientation.structuredContent?.recommended_resources?.includes("registry://ilens-walkthrough"),
  "Expected orientation to include ILENS walkthrough resource.",
);

const trace = await client.callTool({
  name: "trace_to_motifs",
  arguments: {
    ref: "MBTI",
  },
});
expect(!trace.isError, "Expected trace_to_motifs tool to succeed.");
expect(Array.isArray(trace.structuredContent?.direct_mappings), "Expected trace direct mappings array.");
expect(Array.isArray(trace.structuredContent?.construct_mappings), "Expected trace construct mappings array.");
expect(
  trace.structuredContent.construct_mappings.some((group) =>
    group.mappings.some((mapping) => mapping.target_entity_id === "mtf_social_energy_orientation"),
  ),
  "Expected MBTI trace to include social energy orientation motif.",
);

const program = await client.callTool({
  name: "fetch_protocol_spec",
  arguments: {
    ref: "ILENS",
  },
});
expect(!program.isError, "Expected fetch_protocol_spec tool to succeed.");
expect(program.structuredContent?.protocol?.id === "proto_ilens", "Expected ILENS protocol payload.");

const packList = await client.callTool({
  name: "list_protocol_packs",
  arguments: {
    featured: true,
  },
});
expect(!packList.isError, "Expected list_protocol_packs tool to succeed.");
expect(
  Array.isArray(packList.structuredContent?.protocol_packs) &&
    packList.structuredContent.protocol_packs.some((pack) => pack.id === "ppk_ilens_core_trait_motive_stack"),
  "Expected featured pack listing.",
);

const packSummary = await client.callTool({
  name: "fetch_protocol_pack_summary",
  arguments: {
    ref: "ILENS",
    frameworks: ["Big Five", "MBTI", "Enneagram"],
  },
});
expect(!packSummary.isError, "Expected fetch_protocol_pack_summary tool to succeed.");
expect(packSummary.structuredContent?.summary?.protocol_name === "ILENS", "Expected ILENS pack summary.");
expect(
  Array.isArray(packSummary.structuredContent?.summary?.execution_order) &&
    packSummary.structuredContent.summary.execution_order.length >= 3,
  "Expected pack summary execution order.",
);

const resultAtom = await client.callTool({
  name: "fetch_result_atom_schema",
  arguments: {},
});
expect(!resultAtom.isError, "Expected fetch_result_atom_schema tool to succeed.");
expect(resultAtom.structuredContent?.result_atom_schema?.id === "ras_result_atom_v0_1", "Expected result atom schema.");

const researchModels = await client.callTool({
  name: "fetch_research_models",
  arguments: {},
});
expect(!researchModels.isError, "Expected fetch_research_models tool to succeed.");
expect(
  Array.isArray(researchModels.structuredContent?.contribution_models) &&
    researchModels.structuredContent.contribution_models.length >= 5,
  "Expected research contribution model list.",
);

await transport.close();
console.log("MCP contract test passed.");
