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
  "list_analysis_modes",
  "list_comparison_shapes",
  "fetch_comparison_shape",
  "prepare_comparison_run",
  "list_capabilities",
  "list_expression_profiles",
  "fetch_expression_profile",
  "list_workflow_recipes",
  "fetch_workflow_recipe",
  "prepare_artifact_realization",
  "prepare_artifact_template",
  "recommend_next_path",
  "list_artifact_classes",
  "list_actualization_protocols",
  "compare_frameworks",
  "trace_to_motifs",
  "fetch_protocol_spec",
  "list_protocol_packs",
  "fetch_protocol_pack_summary",
  "fetch_protocol_pack",
  "fetch_result_atom_schema",
  "normalize_result_atom_bundle",
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

const advancedModes = await client.readResource({ uri: "registry://advanced-modes" });
expect(
  advancedModes.contents?.[0]?.text?.includes("Mode 1: orientation and sync"),
  "Expected advanced modes resource content.",
);

const comparisonShapes = await client.readResource({ uri: "registry://comparison-shapes" });
expect(
  comparisonShapes.contents?.[0]?.text?.includes("Comparison Shapes"),
  "Expected comparison shapes resource content.",
);

const comparisonPreflight = await client.readResource({ uri: "registry://comparison-preflight" });
expect(
  comparisonPreflight.contents?.[0]?.text?.includes("Comparison Preflight"),
  "Expected comparison preflight resource content.",
);

const capabilityModel = await client.readResource({ uri: "registry://capability-model" });
expect(
  capabilityModel.contents?.[0]?.text?.includes("Capability Model"),
  "Expected capability model resource content.",
);

const expressionModel = await client.readResource({ uri: "registry://expression-model" });
expect(
  expressionModel.contents?.[0]?.text?.includes("Expression Model"),
  "Expected expression model resource content.",
);

const workflowRecipes = await client.readResource({ uri: "registry://workflow-recipes" });
expect(
  workflowRecipes.contents?.[0]?.text?.includes("Workflow Recipes"),
  "Expected workflow recipes resource content.",
);

const artifactRealization = await client.readResource({ uri: "registry://artifact-realization" });
expect(
  artifactRealization.contents?.[0]?.text?.includes("Artifact Realization"),
  "Expected artifact realization resource content.",
);

const artifactTemplates = await client.readResource({ uri: "registry://artifact-templates" });
expect(
  artifactTemplates.contents?.[0]?.text?.includes("Artifact Templates"),
  "Expected artifact templates resource content.",
);

const resultAtomNormalization = await client.readResource({ uri: "registry://result-atom-normalization" });
expect(
  resultAtomNormalization.contents?.[0]?.text?.includes("Result Atom Normalization"),
  "Expected result atom normalization resource content.",
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
expect(
  Array.isArray(orientation.structuredContent?.advanced_docs) &&
    orientation.structuredContent.advanced_docs.includes("docs/advanced_modes.md"),
  "Expected orientation to include advanced docs.",
);
expect(
  orientation.structuredContent?.advanced_docs?.includes("docs/capability_model.md"),
  "Expected orientation to include capability model doc.",
);

const capabilities = await client.callTool({
  name: "list_capabilities",
  arguments: {
    artifact: "Context Matrix",
  },
});
expect(!capabilities.isError, "Expected list_capabilities tool to succeed.");
expect(
  Array.isArray(capabilities.structuredContent?.capabilities) &&
    capabilities.structuredContent.capabilities.some((item) => item.id === "cap_table_render"),
  "Expected capability list for context matrix artifact.",
);

const comparisonShapeList = await client.callTool({
  name: "list_comparison_shapes",
  arguments: {
    text: "compare me across time",
  },
});
expect(!comparisonShapeList.isError, "Expected list_comparison_shapes tool to succeed.");
expect(
  Array.isArray(comparisonShapeList.structuredContent?.comparison_shapes) &&
    comparisonShapeList.structuredContent.comparison_shapes.some(
      (item) => item.id === "cmp_contextual_time_slices",
    ),
  "Expected comparison shape list to include time-slice comparison.",
);

const comparisonRun = await client.callTool({
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
expect(!comparisonRun.isError, "Expected prepare_comparison_run tool to succeed.");
expect(
  comparisonRun.structuredContent?.readiness_status === "ready",
  "Expected comparison preflight readiness to be ready.",
);
expect(
  comparisonRun.structuredContent?.path_recommendation?.recommended_artifact?.artifact_class?.id === "art_context_matrix",
  "Expected preflight to recommend context matrix artifact path.",
);

const expressions = await client.callTool({
  name: "list_expression_profiles",
  arguments: {
    artifact: "Context Matrix",
  },
});
expect(!expressions.isError, "Expected list_expression_profiles tool to succeed.");
expect(
  Array.isArray(expressions.structuredContent?.expression_profiles) &&
    expressions.structuredContent.expression_profiles.some((item) => item.id === "expr_explanatory"),
  "Expected explanatory expression profile for context matrix artifact.",
);

const workflows = await client.callTool({
  name: "list_workflow_recipes",
  arguments: {
    artifact: "Context Matrix",
  },
});
expect(!workflows.isError, "Expected list_workflow_recipes tool to succeed.");
expect(
  Array.isArray(workflows.structuredContent?.workflow_recipes) &&
    workflows.structuredContent.workflow_recipes.some((item) => item.id === "wfr_context_matrix_explanatory"),
  "Expected workflow recipe for context matrix artifact.",
);

const resultAtomBundle = await client.callTool({
  name: "normalize_result_atom_bundle",
  arguments: {
    framework: "Big Five",
    comparison_shape: "Contextual Time Slices",
    default_source_quality: "self_reported",
    entries: [
      {
        construct: "Openness to Experience",
        output_type: "continuous_score",
        output_value: "0.74",
      },
      {
        construct: "Agreeableness",
        output_type: "continuous_score",
        output_value: "0.51",
      },
    ],
  },
});
expect(!resultAtomBundle.isError, "Expected normalize_result_atom_bundle tool to succeed.");
expect(
  resultAtomBundle.structuredContent?.readiness_status === "ready",
  "Expected result atom normalization readiness to be ready.",
);
expect(
  resultAtomBundle.structuredContent?.bundle?.comparison_shape_id === "cmp_contextual_time_slices",
  "Expected comparison shape metadata on the normalized bundle.",
);
expect(
  resultAtomBundle.structuredContent?.bundle?.atoms?.[0]?.mapped_motif_ids?.includes("mtf_exploratory_openness"),
  "Expected normalized bundle to include mapped motifs for openness.",
);
expect(
  Array.isArray(resultAtomBundle.structuredContent?.warnings) &&
    resultAtomBundle.structuredContent.warnings.some((item) => item.includes("Agreeableness")),
  "Expected result atom normalization warnings for unmapped constructs.",
);

const artifactRealizationPlan = await client.callTool({
  name: "prepare_artifact_realization",
  arguments: {
    workflow_recipe: "Context Matrix Explanatory",
    capabilities: ["Markdown Write", "Table Render"],
  },
});
expect(!artifactRealizationPlan.isError, "Expected prepare_artifact_realization tool to succeed.");
expect(
  artifactRealizationPlan.structuredContent?.readiness_status === "ready",
  "Expected artifact realization readiness to be ready.",
);
expect(
  artifactRealizationPlan.structuredContent?.selected_realization_form === "markdown table",
  "Expected artifact realization to choose markdown table.",
);

const artifactTemplatePlan = await client.callTool({
  name: "prepare_artifact_template",
  arguments: {
    workflow_recipe: "Structured Result Bundle Technical",
    hosts: ["Codex Desktop"],
  },
});
expect(!artifactTemplatePlan.isError, "Expected prepare_artifact_template tool to succeed.");
expect(
  artifactTemplatePlan.structuredContent?.template_kind === "json_object",
  "Expected artifact template to return a JSON object template for result bundles.",
);
expect(
  artifactTemplatePlan.structuredContent?.template_object?.template_meta?.workflow_recipe_id === "wfr_structured_result_bundle_technical",
  "Expected artifact template metadata to reflect the selected workflow recipe.",
);

const recommendation = await client.callTool({
  name: "recommend_next_path",
  arguments: {
    mode: "Contextual and Multi-Subject Comparison",
    comparison_shape: "Contextual Time Slices",
    capabilities: ["Markdown Write", "Table Render"],
    text: "compare me across time and make a matrix",
  },
});
expect(!recommendation.isError, "Expected recommend_next_path tool to succeed.");
expect(
  recommendation.structuredContent?.recommended_comparison_shape?.id === "cmp_contextual_time_slices",
  "Expected recommended comparison shape for contextual matrix path.",
);
expect(
  recommendation.structuredContent?.recommended_artifact?.artifact_class?.id === "art_context_matrix",
  "Expected recommended artifact for contextual matrix path.",
);
expect(
  recommendation.structuredContent?.recommended_expression_profile?.id === "expr_explanatory",
  "Expected recommended expression profile for contextual matrix path.",
);
expect(
  recommendation.structuredContent?.recommended_workflow_recipe?.workflow_recipe?.id === "wfr_context_matrix_explanatory",
  "Expected recommended workflow recipe for contextual matrix path.",
);
expect(
  recommendation.structuredContent?.recommended_tools?.includes("prepare_artifact_realization"),
  "Expected recommendation to point to artifact realization.",
);
expect(
  recommendation.structuredContent?.recommended_tools?.includes("prepare_artifact_template"),
  "Expected recommendation to point to artifact template preparation.",
);

const actualizationProtocols = await client.callTool({
  name: "list_actualization_protocols",
  arguments: {
    mode: "Artifact Actualization",
  },
});
expect(!actualizationProtocols.isError, "Expected list_actualization_protocols tool to succeed.");
expect(
  Array.isArray(actualizationProtocols.structuredContent?.actualization_protocols) &&
    actualizationProtocols.structuredContent.actualization_protocols.some(
      (item) => item.id === "actx_single_subject_comparative_memo",
    ),
  "Expected actualization protocols for artifact mode.",
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
