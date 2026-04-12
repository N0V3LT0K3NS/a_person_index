# Site Design Options

This document records the three public landing-page directions currently generated for A Person Index.

They all present the same product. They differ in emphasis.

## Why this exists

The public site needs to communicate to different kinds of readers:

- someone trying to understand the product quickly
- a runtime or agent builder deciding whether to depend on it
- a curator or researcher evaluating its seriousness and scope discipline

Rather than forcing one compromise page too early, the repo now generates three distinct landing directions and keeps them versioned as code.

## The three directions

### Atlas

Path: `site/index.html` and `site/landing-atlas.html`

Purpose:
- public-facing flagship
- strongest articulation of the “comparative atlas” idea
- best default if the site needs to sell the concept clearly and broadly

Emphasis:
- the product thesis
- the layered model
- why the index matters
- who it serves

### Signal Stack

Path: `site/landing-signal.html`

Purpose:
- systems-facing explanation for agents, runtimes, and technical evaluators

Emphasis:
- canonical records -> motifs -> interactions -> programs -> packs -> runtimes -> return traffic
- CLI, MCP, generated JSON, and runtime bundle surfaces
- how consumers such as `GNOMY` should think about the repo

### Field Guide

Path: `site/landing-field-guide.html`

Purpose:
- calmer, more editorial direction for curators, researchers, and people evaluating scope and rigor

Emphasis:
- boundaries
- methodological stance
- what belongs in the repo vs outside it
- why staged evidence matters

## Selection guidance

- Choose `Atlas` when the site should explain the product to the broadest audience.
- Choose `Signal Stack` when the primary audience is technical or agentic.
- Choose `Field Guide` when the primary audience is curatorial, editorial, or research-oriented.

## Pencil note

Pencil’s documentation frames design as code and treats `.pen` files as versionable design artifacts.

Relevant references:
- [Pencil Documentation](https://docs.pencil.dev/)
- [Design as Code](https://docs.pencil.dev/core-concepts/design-as-code)
- [The .pen Format](https://docs.pencil.dev/for-developers/the-pen-format)
- [Pencil CLI](https://docs.pencil.dev/for-developers/pencil-cli)

At the moment this repo does not have a local authenticated Pencil CLI/session available, so these directions are encoded directly in the site generator and generated HTML/CSS. They can later be ported into `.pen` files once a Pencil CLI key or session is available.
