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
      "Use this server to retrieve canonical framework records, motif traces, interaction hypotheses, program packs, result atom schema, and research contribution models from A Person Index. Keep canonical data, house synthesis, index programs, and research evidence clearly separated.",
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
      description: "Curated protocol-pack catalog and summary index.",
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
      title: "Curated Protocol Pack",
      description: "Generated curated protocol-pack artifact by pack ID.",
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
      description: "Canonical grammar for generated protocol packs.",
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
            text: await readRepoText("AGENTS.md"),
          },
        },
      ],
    }),
  );

  server.registerPrompt(
    "protocol-pack-authoring",
    {
      title: "Protocol Pack Authoring",
      description: "Load the canonical grammar and constraints for creating future protocol packs.",
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

  server.registerTool(
    "find_framework_records",
    {
      title: "Find Framework Records",
      description: "Resolve canonical framework records by name, alias, family, text, or related framework.",
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
      description: "Return a protocol spec and its technique bundle.",
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
      title: "List Protocol Packs",
      description: "Return curated protocol-pack catalog entries with optional filters.",
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
      title: "Fetch Curated Protocol Pack",
      description: "Return a curated protocol-pack catalog entry plus its generated runtime bundle.",
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
    "fetch_protocol_pack",
    {
      title: "Fetch Protocol Pack",
      description: "Assemble a downstream-ready protocol pack scoped to selected frameworks or constructs.",
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
      title: "Fetch Protocol Pack Grammar",
      description: "Return the canonical grammar for generated protocol packs.",
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
