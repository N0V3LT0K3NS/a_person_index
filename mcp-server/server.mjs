import { access, readFile } from "node:fs/promises";
import { constants as fsConstants } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

async function resolvePythonBin() {
  if (process.env.PERSON_INDEX_PYTHON) {
    return process.env.PERSON_INDEX_PYTHON;
  }

  const localVenvPython = path.join(repoRoot, ".venv", "bin", "python");
  try {
    await access(localVenvPython, fsConstants.X_OK);
    return localVenvPython;
  } catch {
    return "python3";
  }
}

function jsonResult(payload) {
  return {
    content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    structuredContent: payload,
  };
}

function jsonCollectionResult(key, items) {
  const payload = { [key]: items };
  return {
    content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    structuredContent: payload,
  };
}

function errorResult(message) {
  return {
    content: [{ type: "text", text: message }],
    isError: true,
  };
}

async function readRepoText(relativePath) {
  return readFile(path.join(repoRoot, relativePath), "utf-8");
}

async function runRegistryQuery(args, pythonBin) {
  const finalArgs = [...args];
  if (!finalArgs.includes("--format")) {
    finalArgs.push("--format", "json");
  }

  return new Promise((resolve, reject) => {
    const child = spawn(
      pythonBin,
      ["scripts/query_registry.py", ...finalArgs],
      {
        cwd: repoRoot,
        env: {
          ...process.env,
          PYTHONUTF8: "1",
        },
        stdio: ["ignore", "pipe", "pipe"],
      },
    );

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code !== 0) {
        reject(
          new Error(
            `Registry query failed (${code}): ${stderr.trim() || stdout.trim() || "unknown error"}`,
          ),
        );
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch (error) {
        reject(
          new Error(`Failed to parse registry JSON output: ${error instanceof Error ? error.message : String(error)}`),
        );
      }
    });
  });
}

async function buildServer() {
  const pythonBin = await resolvePythonBin();
  const server = new McpServer({
    name: "a-person-index",
    version: "0.1.0",
    instructions:
      "Use this server to retrieve canonical framework records, motif traces, interaction hypotheses, program packs, result atom schema, research contribution models, advanced run modes, comparison shapes, comparison preflight guidance, host profiles, capability records, expression profiles, artifact classes, actualization protocols, workflow recipes, and artifact realization guidance from A Person Index. Start with registry://quickstart when arriving cold. For pasted user assessment results, match frameworks first, then inspect featured program packs, then trace motifs. When the task becomes planning, artifact generation, or contextual comparison, inspect the advanced mode, comparison-shape, comparison-preflight, host-profile, capability, expression, actualization, workflow, and artifact-realization surfaces before improvising. Use prepare_comparison_run once a contextual or pairwise shape is chosen and you need to check whether the run is actually declared well enough to proceed. Use recommend_next_path when you already know either the host profile or the host capabilities and need the smallest disciplined next step. Use prepare_artifact_realization once a workflow recipe is chosen and you need a concrete scaffold for the finished artifact. Keep canonical data, house synthesis, index programs, downstream artifacts, and research evidence clearly separated.",
  });

  server.registerResource(
    "manifest",
    "registry://manifest",
    {
      title: "A Person Index Manifest",
      description: "Machine-readable onboarding and service-primitives manifest.",
      mimeType: "application/json",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("generated/manifest.json"),
        },
      ],
    }),
  );

  server.registerResource(
    "quickstart",
    "registry://quickstart",
    {
      title: "Agent Quickstart",
      description: "Shortest safe arrival path for agents using A Person Index.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/agent_quickstart.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "current-state",
    "registry://current-state",
    {
      title: "Current State",
      description: "Compressed statement of current shipped scope and completion level.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/current_state.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "roadmap",
    "registry://roadmap",
    {
      title: "Roadmap",
      description: "Phase and direction document for A Person Index.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/roadmap.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "assessment-workflow",
    "registry://assessment-workflow",
    {
      title: "Assessment Workflow",
      description: "Recommended workflow for turning user assessment results into matched frameworks, packs, motifs, and bounded synthesis.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/assessment_workflow.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "ilens-walkthrough",
    "registry://ilens-walkthrough",
    {
      title: "ILENS Walkthrough",
      description: "Worked example of the recommended MCP sequence for an ILENS-style pass on mixed assessment results.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/ilens_walkthrough.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "advanced-modes",
    "registry://advanced-modes",
    {
      title: "Advanced Modes",
      description: "Named higher-order run shapes such as planning, actualization, contextual comparison, and trace review.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/advanced_modes.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "comparison-shapes",
    "registry://comparison-shapes",
    {
      title: "Comparison Shapes",
      description: "Structured contextual and pairwise comparison shapes that make required declarations explicit before execution.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/comparison_shapes.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "comparison-preflight",
    "registry://comparison-preflight",
    {
      title: "Comparison Preflight",
      description: "How to validate declared contextual or pairwise comparison inputs before artifact selection and execution.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/comparison_preflight.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "host-profiles",
    "registry://host-profiles",
    {
      title: "Host Profiles",
      description: "Known host profiles that expand into capability sets for planning, comparison preflight, and artifact realization.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/host_profiles.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "artifact-realization",
    "registry://artifact-realization",
    {
      title: "Artifact Realization",
      description: "How to turn a chosen workflow recipe into a concrete artifact scaffold without turning A Person Index into a renderer.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/artifact_realization.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "capability-model",
    "registry://capability-model",
    {
      title: "Capability Model",
      description: "Abstract capability taxonomy for host-aware planning, actualization, and meta-skill behavior.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/capability_model.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "expression-model",
    "registry://expression-model",
    {
      title: "Expression Model",
      description: "Structured expression profiles for tacit, explanatory, technical, and mixed downstream rendering.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/expression_model.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "actualization-protocols",
    "registry://actualization-protocols",
    {
      title: "Actualization Protocols",
      description: "How A Person Index acts as comparative core inside richer downstream workflows and artifacts.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/actualization_protocols.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "workflow-recipes",
    "registry://workflow-recipes",
    {
      title: "Workflow Recipes",
      description: "Operational recipes that bind recommendation, actualization, expression, and capability fit into a concrete next sequence.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/workflow_recipes.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "expression-and-artifacts",
    "registry://expression-and-artifacts",
    {
      title: "Expression and Artifacts",
      description: "Voice modes, artifact classes, and output-grammar guidance for downstream realization.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/expression_and_artifacts.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "multi-subject-comparison",
    "registry://multi-subject-comparison",
    {
      title: "Multi-Subject Comparison",
      description: "Contextual, temporal, and pairwise comparison guidance beyond a single mixed stack.",
      mimeType: "text/markdown",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("docs/multi_subject_comparison.md"),
        },
      ],
    }),
  );

  server.registerResource(
    "research-promotion",
    "registry://research-promotion",
    {
      title: "Research Promotion Policy",
      description: "Staged promotion policy for research contributions and review pathways.",
      mimeType: "application/json",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("generated/research_promotion.json"),
        },
      ],
    }),
  );

  server.registerResource(
    "protocol-packs",
    "registry://protocol-packs",
    {
      title: "Program Pack Catalog",
      description: "Curated program-pack catalog and summary index.",
      mimeType: "application/json",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("generated/protocol_packs/index.json"),
        },
      ],
    }),
  );

  server.registerResource(
    "protocol-pack",
    new ResourceTemplate("registry://protocol-pack/{pack_id}", { list: undefined }),
    {
      title: "Curated Program Pack",
      description: "Generated curated program-pack artifact by pack ID.",
      mimeType: "application/json",
    },
    async (uri, { pack_id }) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText(`generated/protocol_packs/${pack_id}.json`),
        },
      ],
    }),
  );

  server.registerResource(
    "protocol-pack-grammar",
    "registry://protocol-pack-grammar",
    {
      title: "Program Pack Grammar",
      description: "Canonical grammar for generated program packs.",
      mimeType: "application/json",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText("generated/protocol_pack_grammar.json"),
        },
      ],
    }),
  );

  server.registerResource(
    "instrument-record",
    new ResourceTemplate("registry://instrument/{slug}", { list: undefined }),
    {
      title: "Instrument Record",
      description: "Generated per-instrument JSON export by slug.",
      mimeType: "application/json",
    },
    async (uri, { slug }) => ({
      contents: [
        {
          uri: uri.href,
          text: await readRepoText(`generated/instruments/${slug}.json`),
        },
      ],
    }),
  );

  server.registerPrompt(
    "registry-arrival",
    {
      title: "A Person Index Arrival",
      description: "Orient a newly arrived agent to the repo, layers, and safe starting surfaces.",
    },
    async () => ({
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: await readRepoText("docs/agent_quickstart.md"),
          },
        },
      ],
    }),
  );

  server.registerPrompt(
    "assessment-results-intake",
    {
      title: "Assessment Results Intake",
      description: "Load the preferred workflow for matching user assessment results into frameworks, packs, motifs, and caveats.",
    },
    async () => ({
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: await readRepoText("docs/assessment_workflow.md"),
          },
        },
      ],
    }),
  );

  server.registerPrompt(
    "protocol-pack-authoring",
    {
      title: "Program Pack Authoring",
      description: "Load the canonical grammar and constraints for creating future program packs.",
      argsSchema: {
        protocol_name: z.string().optional(),
      },
    },
    async ({ protocol_name }) => {
      const grammar = await readRepoText("docs/protocol_pack_grammar.md");
      const targetLine = protocol_name
        ? `Focus this authoring session on protocol: ${protocol_name}.`
        : "No protocol target was supplied. Keep the grammar generic.";
      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `${targetLine}\n\n${grammar}`,
            },
          },
        ],
      };
    },
  );

  server.registerPrompt(
    "ilens-walkthrough",
    {
      title: "ILENS Walkthrough",
      description: "Load the worked example for matching results, selecting a pack, tracing motifs, and keeping runtime boundaries clear.",
    },
    async () => ({
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: await readRepoText("docs/ilens_walkthrough.md"),
          },
        },
      ],
    }),
  );

  server.registerTool(
    "orient_agent",
    {
      title: "Orient Agent",
      description: "Return a compact onboarding payload with framework refs, featured program packs, common mistakes, and recommended first steps.",
      inputSchema: {},
    },
    async () => {
      try {
        return jsonResult(await runRegistryQuery(["orient"], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_analysis_modes",
    {
      title: "List Analysis Modes",
      description: "Return named run modes such as bounded analysis, planning, actualization, contextual comparison, or trace review.",
      inputSchema: {
        text: z.string().optional(),
      },
    },
    async ({ text }) => {
      try {
        const args = ["modes"];
        if (text) args.push("--text", text);
        return jsonCollectionResult("analysis_modes", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_analysis_mode",
    {
      title: "Fetch Analysis Mode",
      description: "Return the full record for a named analysis mode.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["modes", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_comparison_shapes",
    {
      title: "List Comparison Shapes",
      description: "Return contextual or pairwise comparison shapes with their required declarations and recommended protocol fit.",
      inputSchema: {
        mode: z.string().optional(),
        artifact: z.string().optional(),
        protocol: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ mode, artifact, protocol, text }) => {
      try {
        const args = ["comparison-shapes"];
        if (mode) args.push("--mode", mode);
        if (artifact) args.push("--artifact", artifact);
        if (protocol) args.push("--protocol", protocol);
        if (text) args.push("--text", text);
        return jsonCollectionResult("comparison_shapes", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_comparison_shape",
    {
      title: "Fetch Comparison Shape",
      description: "Return the full record for a named comparison shape including its required declarations, suitable artifacts, and recommended protocols.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["comparison-shapes", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_host_profiles",
    {
      title: "List Host Profiles",
      description: "Return known host profiles that expand into capability sets for planning and actualization.",
      inputSchema: {
        kind: z.string().optional(),
        capability: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ kind, capability, text }) => {
      try {
        const args = ["hosts"];
        if (kind) args.push("--kind", kind);
        if (capability) args.push("--capability", capability);
        if (text) args.push("--text", text);
        return jsonCollectionResult("host_profiles", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_host_profile",
    {
      title: "Fetch Host Profile",
      description: "Return the full record for a named host profile including its expanded capability set and cautions.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["hosts", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "prepare_comparison_run",
    {
      title: "Prepare Comparison Run",
      description: "Validate whether a contextual or pairwise comparison run is adequately declared before artifact selection and execution begins.",
      inputSchema: {
        comparison_shape: z.string(),
        declarations: z
          .record(z.string(), z.union([z.string(), z.array(z.string())]))
          .optional(),
        hosts: z.array(z.string()).optional(),
        capabilities: z.array(z.string()).optional(),
      },
    },
    async ({ comparison_shape, declarations, hosts, capabilities }) => {
      try {
        const args = ["comparison-preflight", comparison_shape];
        if (declarations) {
          args.push("--declarations-json", JSON.stringify(declarations));
        }
        for (const host of hosts ?? []) args.push("--host", host);
        for (const capability of capabilities ?? []) args.push("--capability", capability);
        return jsonResult(await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_capabilities",
    {
      title: "List Capabilities",
      description: "Return abstract host capabilities for meta-skill planning and artifact actualization.",
      inputSchema: {
        kind: z.string().optional(),
        artifact: z.string().optional(),
        actualization: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ kind, artifact, actualization, text }) => {
      try {
        const args = ["capabilities"];
        if (kind) args.push("--kind", kind);
        if (artifact) args.push("--artifact", artifact);
        if (actualization) args.push("--actualization", actualization);
        if (text) args.push("--text", text);
        return jsonCollectionResult("capabilities", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_capability",
    {
      title: "Fetch Capability",
      description: "Return the full record for a named host capability including the artifact classes and actualization protocols that depend on it.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["capabilities", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_expression_profiles",
    {
      title: "List Expression Profiles",
      description: "Return structured expression profiles for tacit, explanatory, technical, or mixed downstream rendering.",
      inputSchema: {
        mode: z.string().optional(),
        audience: z.string().optional(),
        artifact: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ mode, audience, artifact, text }) => {
      try {
        const args = ["expressions"];
        if (mode) args.push("--mode", mode);
        if (audience) args.push("--audience", audience);
        if (artifact) args.push("--artifact", artifact);
        if (text) args.push("--text", text);
        return jsonCollectionResult("expression_profiles", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_expression_profile",
    {
      title: "Fetch Expression Profile",
      description: "Return the full record for a named expression profile and the artifact classes that default to it.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["expressions", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_workflow_recipes",
    {
      title: "List Workflow Recipes",
      description: "Return workflow recipes that operationalize a specific artifact path in a host environment.",
      inputSchema: {
        mode: z.string().optional(),
        artifact: z.string().optional(),
        actualization: z.string().optional(),
        expression: z.string().optional(),
        capability: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ mode, artifact, actualization, expression, capability, text }) => {
      try {
        const args = ["workflows"];
        if (mode) args.push("--mode", mode);
        if (artifact) args.push("--artifact", artifact);
        if (actualization) args.push("--actualization", actualization);
        if (expression) args.push("--expression", expression);
        if (capability) args.push("--capability", capability);
        if (text) args.push("--text", text);
        return jsonCollectionResult("workflow_recipes", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_workflow_recipe",
    {
      title: "Fetch Workflow Recipe",
      description: "Return a concrete workflow recipe tying run mode, artifact class, expression profile, and actualization protocol into one operational sequence.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["workflows", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "prepare_artifact_realization",
    {
      title: "Prepare Artifact Realization",
      description: "Turn a chosen workflow recipe plus declared host profiles or capabilities into a concrete artifact scaffold, preferred form, and next steps.",
      inputSchema: {
        workflow_recipe: z.string(),
        hosts: z.array(z.string()).optional(),
        capabilities: z.array(z.string()).optional(),
      },
    },
    async ({ workflow_recipe, hosts, capabilities }) => {
      try {
        const args = ["artifact-realization", workflow_recipe];
        for (const host of hosts ?? []) args.push("--host", host);
        for (const capability of capabilities ?? []) args.push("--capability", capability);
        return jsonResult(await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "recommend_next_path",
    {
      title: "Recommend Next Path",
      description: "Recommend the next A Person Index path from the current run shape and declared host profile or capability context.",
      inputSchema: {
        mode: z.string().optional(),
        comparison_shape: z.string().optional(),
        hosts: z.array(z.string()).optional(),
        capabilities: z.array(z.string()).optional(),
        artifact: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ mode, comparison_shape, hosts, capabilities, artifact, text }) => {
      try {
        const args = ["recommend-path"];
        if (mode) args.push("--mode", mode);
        if (comparison_shape) args.push("--comparison-shape", comparison_shape);
        for (const host of hosts ?? []) args.push("--host", host);
        for (const capability of capabilities ?? []) args.push("--capability", capability);
        if (artifact) args.push("--artifact", artifact);
        if (text) args.push("--text", text);
        return jsonResult(await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_artifact_classes",
    {
      title: "List Artifact Classes",
      description: "Return downstream artifact classes that A Person Index can semantically support.",
      inputSchema: {
        mode: z.string().optional(),
        capability: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ mode, capability, text }) => {
      try {
        const args = ["artifacts"];
        if (mode) args.push("--mode", mode);
        if (capability) args.push("--capability", capability);
        if (text) args.push("--text", text);
        return jsonCollectionResult("artifact_classes", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_artifact_class",
    {
      title: "Fetch Artifact Class",
      description: "Return the full record for a named artifact class including evidence and capability expectations.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["artifacts", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_actualization_protocols",
    {
      title: "List Actualization Protocols",
      description: "Return downstream actualization protocols that turn A Person Index comparative work into artifacts or handoffs.",
      inputSchema: {
        mode: z.string().optional(),
        artifact: z.string().optional(),
        capability: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ mode, artifact, capability, text }) => {
      try {
        const args = ["actualization"];
        if (mode) args.push("--mode", mode);
        if (artifact) args.push("--artifact", artifact);
        if (capability) args.push("--capability", capability);
        if (text) args.push("--text", text);
        return jsonCollectionResult("actualization_protocols", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_actualization_protocol",
    {
      title: "Fetch Actualization Protocol",
      description: "Return the full record for a named actualization protocol.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["actualization", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "find_framework_records",
    {
      title: "Find Framework Records",
      description: "Resolve canonical framework records by name, alias, family, text, or related framework. Prefer refs for distinct labels and use text for short fuzzy recovery, not as a blind full-report dump.",
      inputSchema: {
        refs: z.array(z.string()).optional(),
        families: z.array(z.string()).optional(),
        filters: z.array(z.string()).optional(),
        text: z.string().optional(),
        related_to: z.string().optional(),
      },
    },
    async ({ refs, families, filters, text, related_to }) => {
      try {
        const args = ["find"];
        for (const ref of refs ?? []) args.push("--ref", ref);
        for (const family of families ?? []) args.push("--family", family);
        for (const filter of filters ?? []) args.push("--filter", filter);
        if (text) args.push("--text", text);
        if (related_to) args.push("--related-to", related_to);
        return jsonCollectionResult("results", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "compare_frameworks",
    {
      title: "Compare Frameworks",
      description: "Compare two canonical framework records and return shared ontology plus crosswalks.",
      inputSchema: {
        left: z.string(),
        right: z.string(),
      },
    },
    async ({ left, right }) => {
      try {
        return jsonResult(await runRegistryQuery(["compare", left, right], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "trace_to_motifs",
    {
      title: "Trace To Motifs",
      description: "Trace an instrument or construct through the house motif layer.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["trace", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_related_motifs",
    {
      title: "List Related Motifs",
      description: "Return motifs linked to a framework or construct.",
      inputSchema: {
        related_to: z.string(),
      },
    },
    async ({ related_to }) => {
      try {
        return jsonCollectionResult(
          "motifs",
          await runRegistryQuery(["motifs", "--related-to", related_to], pythonBin),
        );
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_interaction_hypotheses",
    {
      title: "List Interaction Hypotheses",
      description: "Return interaction hypotheses related to a scope and optionally filtered by type or protocol.",
      inputSchema: {
        related_to: z.string().optional(),
        interaction_type: z.string().optional(),
        protocol: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ related_to, interaction_type, protocol, text }) => {
      try {
        const args = ["interactions"];
        if (related_to) args.push("--related-to", related_to);
        if (interaction_type) args.push("--type", interaction_type);
        if (protocol) args.push("--protocol", protocol);
        if (text) args.push("--text", text);
        return jsonCollectionResult("interaction_hypotheses", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_protocol_spec",
    {
      title: "Fetch Protocol Spec",
      description: "Return an index program spec and its technique bundle. Use this to understand a program such as ILENS or Human Model Card, not to claim it already executed.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["protocols", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "list_protocol_packs",
    {
      title: "List Program Packs",
      description: "Return curated program-pack catalog entries with optional filters. Use featured=true first when you need the most likely reviewed starting points.",
      inputSchema: {
        text: z.string().optional(),
        consumer: z.string().optional(),
        protocol: z.string().optional(),
        status: z.enum(["draft", "experimental", "active"]).optional(),
        featured: z.boolean().optional(),
      },
    },
    async ({ text, consumer, protocol, status, featured }) => {
      try {
        const args = ["protocol-packs"];
        if (text) args.push("--text", text);
        if (consumer) args.push("--consumer", consumer);
        if (protocol) args.push("--protocol", protocol);
        if (status) args.push("--status", status);
        if (featured) args.push("--featured");
        return jsonCollectionResult("protocol_packs", await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_curated_protocol_pack",
    {
      title: "Fetch Curated Program Pack",
      description: "Return a curated program-pack catalog entry plus its generated runtime bundle.",
      inputSchema: {
        ref: z.string(),
      },
    },
    async ({ ref }) => {
      try {
        return jsonResult(await runRegistryQuery(["protocol-packs", ref], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_protocol_pack_summary",
    {
      title: "Fetch Program Pack Summary",
      description: "Return a compact summary of a runtime pack before fetching the full pack. Use this when you want execution order, techniques, and outputs without the full nested payload.",
      inputSchema: {
        ref: z.string(),
        frameworks: z.array(z.string()).optional(),
        constructs: z.array(z.string()).optional(),
      },
    },
    async ({ ref, frameworks, constructs }) => {
      try {
        const args = ["protocol-pack-summary", ref];
        for (const framework of frameworks ?? []) args.push("--framework", framework);
        for (const construct of constructs ?? []) args.push("--construct", construct);
        return jsonResult(await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_protocol_pack",
    {
      title: "Fetch Program Pack",
      description: "Assemble a downstream-ready program pack scoped to selected frameworks or constructs. The ref must be a real program name or ID such as ILENS, Human Model Card, Translation Memo, or Paradox Finder.",
      inputSchema: {
        ref: z.string(),
        frameworks: z.array(z.string()).optional(),
        constructs: z.array(z.string()).optional(),
      },
    },
    async ({ ref, frameworks, constructs }) => {
      try {
        const args = ["protocol-pack", ref];
        for (const framework of frameworks ?? []) args.push("--framework", framework);
        for (const construct of constructs ?? []) args.push("--construct", construct);
        return jsonResult(await runRegistryQuery(args, pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_protocol_pack_grammar",
    {
      title: "Fetch Program Pack Grammar",
      description: "Return the canonical grammar for generated program packs.",
      inputSchema: {},
    },
    async () => {
      try {
        return jsonResult(await runRegistryQuery(["protocol-pack-grammar"], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_result_atom_schema",
    {
      title: "Fetch Result Atom Schema",
      description: "Return the normalized downstream result-atom contract.",
      inputSchema: {},
    },
    async () => {
      try {
        return jsonResult(await runRegistryQuery(["result-atom-schema"], pythonBin));
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_research_models",
    {
      title: "Fetch Research Models",
      description: "Return allowed research contribution models for safe return traffic.",
      inputSchema: {
        ref: z.string().optional(),
        text: z.string().optional(),
      },
    },
    async ({ ref, text }) => {
      try {
        const args = ["research-models"];
        if (ref) args.push(ref);
        if (text) args.push("--text", text);
        const payload = await runRegistryQuery(args, pythonBin);
        if (Array.isArray(payload)) {
          return jsonCollectionResult("contribution_models", payload);
        }
        return jsonResult(payload);
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  server.registerTool(
    "fetch_research_promotion_policy",
    {
      title: "Fetch Research Promotion Policy",
      description: "Return the staged promotion policy or filter promotion pathways by contribution model, layer, or outcome.",
      inputSchema: {
        contribution_model: z.string().optional(),
        target_layer: z.enum(["house_synthesis", "protocol_library", "research_stream"]).optional(),
        outcome: z.enum([
          "mapping_revision",
          "interaction_hypothesis",
          "house_inference",
          "protocol_revision",
          "comparative_analysis",
        ]).optional(),
        text: z.string().optional(),
      },
    },
    async ({ contribution_model, target_layer, outcome, text }) => {
      try {
        const args = ["research-promotion"];
        if (contribution_model) args.push("--contribution-model", contribution_model);
        if (target_layer) args.push("--target-layer", target_layer);
        if (outcome) args.push("--outcome", outcome);
        if (text) args.push("--text", text);
        const payload = await runRegistryQuery(args, pythonBin);
        if (Array.isArray(payload)) {
          return jsonCollectionResult("promotion_pathways", payload);
        }
        return jsonResult(payload);
      } catch (error) {
        return errorResult(error instanceof Error ? error.message : String(error));
      }
    },
  );

  return server;
}

const server = await buildServer();
const transport = new StdioServerTransport();
await server.connect(transport);
