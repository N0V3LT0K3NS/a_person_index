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
if (!tools.tools.some((tool) => tool.name === "list_comparison_shapes")) {
  throw new Error("Expected list_comparison_shapes tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "prepare_comparison_run")) {
  throw new Error("Expected prepare_comparison_run tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "list_capabilities")) {
  throw new Error("Expected list_capabilities tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "list_expression_profiles")) {
  throw new Error("Expected list_expression_profiles tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "list_workflow_recipes")) {
  throw new Error("Expected list_workflow_recipes tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "prepare_artifact_realization")) {
  throw new Error("Expected prepare_artifact_realization tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "prepare_artifact_template")) {
  throw new Error("Expected prepare_artifact_template tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "fetch_framework_result_shape")) {
  throw new Error("Expected fetch_framework_result_shape tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "normalize_result_atom_bundle")) {
  throw new Error("Expected normalize_result_atom_bundle tool in MCP surface.");
}
if (!tools.tools.some((tool) => tool.name === "recommend_next_path")) {
  throw new Error("Expected recommend_next_path tool in MCP surface.");
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

const comparisonShapeResource = await client.readResource({ uri: "registry://comparison-shapes" });
if (!comparisonShapeResource.contents?.[0]?.text?.includes("Comparison Shapes")) {
  throw new Error("Expected comparison shapes resource content.");
}

const comparisonPreflightResource = await client.readResource({ uri: "registry://comparison-preflight" });
if (!comparisonPreflightResource.contents?.[0]?.text?.includes("Comparison Preflight")) {
  throw new Error("Expected comparison preflight resource content.");
}

const capabilityResource = await client.readResource({ uri: "registry://capability-model" });
if (!capabilityResource.contents?.[0]?.text?.includes("capabilities")) {
  throw new Error("Expected capability model resource content.");
}

const expressionResource = await client.readResource({ uri: "registry://expression-model" });
if (!expressionResource.contents?.[0]?.text?.includes("Expression Model")) {
  throw new Error("Expected expression model resource content.");
}

const workflowResource = await client.readResource({ uri: "registry://workflow-recipes" });
if (!workflowResource.contents?.[0]?.text?.includes("Workflow Recipes")) {
  throw new Error("Expected workflow recipes resource content.");
}

const artifactRealizationResource = await client.readResource({ uri: "registry://artifact-realization" });
if (!artifactRealizationResource.contents?.[0]?.text?.includes("Artifact Realization")) {
  throw new Error("Expected artifact realization resource content.");
}

const artifactTemplateResource = await client.readResource({ uri: "registry://artifact-templates" });
if (!artifactTemplateResource.contents?.[0]?.text?.includes("Artifact Templates")) {
  throw new Error("Expected artifact template resource content.");
}

const resultShapeDiscoveryResource = await client.readResource({ uri: "registry://result-shape-discovery" });
if (!resultShapeDiscoveryResource.contents?.[0]?.text?.includes("Result Shape Discovery")) {
  throw new Error("Expected result shape discovery resource content.");
}

const resultAtomNormalizationResource = await client.readResource({ uri: "registry://result-atom-normalization" });
if (!resultAtomNormalizationResource.contents?.[0]?.text?.includes("Result Atom Normalization")) {
  throw new Error("Expected result atom normalization resource content.");
}

const comparisonPreflight = await client.callTool({
  name: "prepare_comparison_run",
  arguments: {
    comparison_shape: "Contextual Time Slices",
    declarations: {
      slice_labels: ["earlier self", "later self"],
      comparison_question: "What changed in a meaningful way?",
    },
    capabilities: ["Markdown Write", "Table Render"],
  },
});

if (comparisonPreflight.isError) {
  throw new Error(
    `Comparison preflight tool returned error: ${comparisonPreflight.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (comparisonPreflight.structuredContent?.readiness_status !== "ready") {
  throw new Error("Expected comparison preflight readiness to be ready.");
}

if (comparisonPreflight.structuredContent?.path_recommendation?.recommended_artifact?.artifact_class?.id !== "art_context_matrix") {
  throw new Error("Expected comparison preflight to recommend the context matrix path.");
}

const artifactRealization = await client.callTool({
  name: "prepare_artifact_realization",
  arguments: {
    workflow_recipe: "Context Matrix Explanatory",
    capabilities: ["Markdown Write", "Table Render"],
  },
});

if (artifactRealization.isError) {
  throw new Error(
    `Artifact realization tool returned error: ${artifactRealization.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (artifactRealization.structuredContent?.readiness_status !== "ready") {
  throw new Error("Expected artifact realization readiness to be ready.");
}

if (artifactRealization.structuredContent?.selected_realization_form !== "markdown table") {
  throw new Error("Expected artifact realization to select the markdown table form.");
}

const artifactTemplate = await client.callTool({
  name: "prepare_artifact_template",
  arguments: {
    workflow_recipe: "Human Model Card Mixed",
    hosts: ["Codex Desktop"],
  },
});

if (artifactTemplate.isError) {
  throw new Error(
    `Artifact template tool returned error: ${artifactTemplate.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (artifactTemplate.structuredContent?.template_kind !== "markdown_document") {
  throw new Error("Expected artifact template to return a markdown document template.");
}

const resultShape = await client.callTool({
  name: "fetch_framework_result_shape",
  arguments: {
    framework: "Big Five",
  },
});

if (resultShape.isError) {
  throw new Error(
    `Result shape tool returned error: ${resultShape.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (resultShape.structuredContent?.construct_count !== 5) {
  throw new Error("Expected Big Five result shape to return five constructs.");
}

const resultAtomBundle = await client.callTool({
  name: "normalize_result_atom_bundle",
  arguments: {
    framework: "Big Five",
    entries: [
      {
        construct: "Openness to Experience",
        output_type: "continuous_score",
        output_value: "0.74",
        source_quality: "self_reported",
      },
    ],
  },
});

if (resultAtomBundle.isError) {
  throw new Error(
    `Result atom normalization tool returned error: ${resultAtomBundle.content?.[0]?.text ?? "unknown error"}`,
  );
}

if (resultAtomBundle.structuredContent?.bundle?.atoms?.[0]?.construct_id !== "con_big_five_openness") {
  throw new Error("Expected result atom normalization to resolve the Big Five openness construct.");
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
