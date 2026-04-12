from __future__ import annotations

from html import escape
from typing import Any


FONT_LINKS = """
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
"""


def _clean_markup(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def landing_variants_manifest() -> list[dict[str, Any]]:
    return [
        {
            "id": "atlas",
            "title": "Atlas of Personhood Systems",
            "path": "landing-atlas.html",
            "summary": "Editorial flagship direction that frames A Person Index as the comparative atlas where frameworks can finally talk without being flattened.",
            "audience": "public_and_generalist",
            "recommended": True,
        },
        {
            "id": "signal",
            "title": "Signal Stack",
            "path": "landing-signal.html",
            "summary": "Systems-facing direction that emphasizes the runtime pipeline from canonical records to motifs, programs, packs, and research-safe return traffic.",
            "audience": "agents_and_runtime_builders",
            "recommended": False,
        },
        {
            "id": "field-guide",
            "title": "Field Guide",
            "path": "landing-field-guide.html",
            "summary": "Minimal research and curator-facing direction that emphasizes boundaries, editorial stance, and long-term corpus discipline.",
            "audience": "curators_and_researchers",
            "recommended": False,
        },
    ]


def _head(title: str, description: str) -> str:
    safe_title = escape(title)
    safe_description = escape(" ".join(description.split()))
    return f"""<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{safe_description}" />
    <meta name="theme-color" content="#8f4b2f" />
    <meta property="og:title" content="{safe_title}" />
    <meta property="og:description" content="{safe_description}" />
    <meta property="og:type" content="website" />
    <title>{safe_title}</title>
    <link rel="icon" href="favicon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="landing.css" />
{FONT_LINKS}
  </head>"""


def _nav(current: str, repo_url: str) -> str:
    links = [
        ("index.html", "atlas", "Home"),
        ("landing-signal.html", "signal", "Signal"),
        ("landing-field-guide.html", "field-guide", "Field Guide"),
        ("landing-options.html", "options", "All Options"),
        ("search.html", "", "Search"),
        ("protocols.html", "", "Programs"),
        (repo_url, "", "GitHub"),
    ]
    items: list[str] = []
    for href, key, label in links:
        active = " active" if key == current else ""
        items.append(
            f'<a class="landing-nav-link{active}" href="{escape(href)}">{escape(label)}</a>'
        )
    return '<nav class="landing-nav">' + "".join(items) + "</nav>"


def _stat_card(value: str, label: str, detail: str) -> str:
    return f"""
<article class="landing-stat">
  <strong>{escape(value)}</strong>
  <span>{escape(label)}</span>
  <p>{escape(detail)}</p>
</article>
"""


def _panel(kicker: str, title: str, body: str, tags: list[str] | None = None) -> str:
    tags_html = ""
    if tags:
        tags_html = '<div class="landing-tags">' + "".join(
            f'<span>{escape(tag)}</span>' for tag in tags
        ) + "</div>"
    return f"""
<article class="landing-panel">
  <p class="landing-kicker">{escape(kicker)}</p>
  <h3>{escape(title)}</h3>
  <p>{escape(body)}</p>
  {tags_html}
</article>
"""


def _step(number: str, title: str, body: str) -> str:
    return f"""
<article class="landing-step">
  <span class="landing-step-number">{escape(number)}</span>
  <h3>{escape(title)}</h3>
  <p>{escape(body)}</p>
</article>
"""


def _chapter(number: str, title: str, body: str) -> str:
    return f"""
<article class="landing-chapter">
  <span class="landing-chapter-number">{escape(number)}</span>
  <div>
    <h3>{escape(title)}</h3>
    <p>{escape(body)}</p>
  </div>
</article>
"""


def _option_card(variant: dict[str, Any]) -> str:
    recommendation = "Recommended default" if variant["recommended"] else "Alternate direction"
    return f"""
<article class="option-card option-{escape(variant['id'])}">
  <div class="option-preview">
    <span class="option-dot option-dot-a"></span>
    <span class="option-dot option-dot-b"></span>
    <span class="option-dot option-dot-c"></span>
  </div>
  <p class="landing-kicker">{escape(recommendation)}</p>
  <h3>{escape(variant['title'])}</h3>
  <p>{escape(variant['summary'])}</p>
  <div class="landing-tags"><span>{escape(variant['audience'])}</span></div>
  <a class="landing-button subtle" href="{escape(variant['path'])}">Open direction</a>
</article>
"""


def landing_css() -> str:
    return """:root {
  --atlas-bg: #f5efe2;
  --atlas-panel: rgba(255, 250, 242, 0.88);
  --atlas-line: rgba(159, 121, 77, 0.26);
  --atlas-accent: #8f4b2f;
  --atlas-accent-soft: #eedcc0;
  --atlas-ink: #1c1813;
  --signal-bg: #eef3fa;
  --signal-panel: rgba(255, 255, 255, 0.9);
  --signal-line: rgba(42, 88, 143, 0.18);
  --signal-accent: #255eb2;
  --signal-accent-soft: #dce7fb;
  --signal-ink: #0f1c2d;
  --field-bg: #f3f1ea;
  --field-panel: rgba(255, 253, 247, 0.9);
  --field-line: rgba(90, 112, 86, 0.18);
  --field-accent: #32624e;
  --field-accent-soft: #deeadf;
  --field-ink: #1a231d;
  --shadow: 0 24px 52px rgba(44, 34, 23, 0.08);
}

* { box-sizing: border-box; }

body.landing-body {
  margin: 0;
  min-height: 100vh;
  font-family: "Manrope", sans-serif;
  color: var(--landing-ink);
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.78), transparent 34%),
    linear-gradient(180deg, var(--landing-bg) 0%, color-mix(in srgb, var(--landing-bg) 88%, #ffffff 12%) 100%);
}

body.theme-atlas {
  --landing-bg: var(--atlas-bg);
  --landing-panel: var(--atlas-panel);
  --landing-line: var(--atlas-line);
  --landing-accent: var(--atlas-accent);
  --landing-accent-soft: var(--atlas-accent-soft);
  --landing-ink: var(--atlas-ink);
}

body.theme-signal {
  --landing-bg: var(--signal-bg);
  --landing-panel: var(--signal-panel);
  --landing-line: var(--signal-line);
  --landing-accent: var(--signal-accent);
  --landing-accent-soft: var(--signal-accent-soft);
  --landing-ink: var(--signal-ink);
  background-image:
    linear-gradient(rgba(37, 94, 178, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 94, 178, 0.05) 1px, transparent 1px),
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.85), transparent 32%),
    linear-gradient(180deg, var(--landing-bg) 0%, #f7fbff 100%);
  background-size: 24px 24px, 24px 24px, auto, auto;
}

body.theme-field-guide {
  --landing-bg: var(--field-bg);
  --landing-panel: var(--field-panel);
  --landing-line: var(--field-line);
  --landing-accent: var(--field-accent);
  --landing-accent-soft: var(--field-accent-soft);
  --landing-ink: var(--field-ink);
  background-image:
    linear-gradient(180deg, rgba(50, 98, 78, 0.06) 0, rgba(50, 98, 78, 0.06) 1px, transparent 1px, transparent 32px),
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.82), transparent 36%),
    linear-gradient(180deg, var(--landing-bg) 0%, #fcfaf4 100%);
  background-size: auto 32px, auto, auto;
}

.landing-shell {
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px 18px 88px;
}

.landing-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.landing-nav-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid var(--landing-line);
  background: rgba(255, 255, 255, 0.6);
  color: var(--landing-ink);
  text-decoration: none;
  font-size: 0.94rem;
}

.landing-nav-link.active,
.landing-button.primary {
  background: var(--landing-accent);
  color: #fffaf4;
  border-color: var(--landing-accent);
}

.landing-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 999px;
  text-decoration: none;
  border: 1px solid var(--landing-line);
  background: rgba(255, 255, 255, 0.65);
  color: var(--landing-ink);
  font-weight: 600;
}

.landing-button.subtle {
  background: var(--landing-accent-soft);
}

.landing-hero,
.landing-section,
.landing-callout,
.landing-stat,
.landing-panel,
.landing-step,
.landing-chapter,
.option-card,
.landing-quote,
.landing-sidecard {
  border: 1px solid var(--landing-line);
  background: var(--landing-panel);
  box-shadow: var(--shadow);
}

.landing-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.95fr);
  gap: 18px;
  padding: 26px;
  border-radius: 28px;
  position: relative;
  overflow: hidden;
}

.landing-hero::after {
  content: "";
  position: absolute;
  inset: auto -10% -25% auto;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  background: radial-gradient(circle, color-mix(in srgb, var(--landing-accent) 24%, transparent) 0%, transparent 72%);
  pointer-events: none;
}

.landing-hero-copy,
.landing-hero-side {
  position: relative;
  z-index: 1;
}

.landing-label,
.landing-kicker,
.landing-overline,
.landing-step-number,
.landing-chapter-number {
  font-family: "IBM Plex Mono", monospace;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.landing-label,
.landing-kicker,
.landing-overline {
  font-size: 0.77rem;
  margin: 0 0 10px;
  color: color-mix(in srgb, var(--landing-accent) 74%, #5b5143 26%);
}

.landing-hero h1,
.landing-section h2,
.landing-panel h3,
.landing-step h3,
.landing-chapter h3,
.option-card h3,
.landing-callout h2,
.landing-sidecard h3 {
  font-family: "Fraunces", serif;
  letter-spacing: -0.03em;
  margin: 0;
}

.landing-hero h1 {
  font-size: clamp(3rem, 7vw, 5.6rem);
  line-height: 0.92;
  max-width: 11ch;
}

.landing-lede {
  margin: 18px 0 0;
  max-width: 62ch;
  font-size: 1.07rem;
  line-height: 1.68;
}

.landing-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}

.landing-hero-side {
  display: grid;
  gap: 14px;
  align-content: start;
}

.landing-quote,
.landing-sidecard {
  border-radius: 22px;
  padding: 18px 18px 16px;
}

.landing-quote p,
.landing-sidecard p {
  margin: 0;
  line-height: 1.65;
}

.landing-quote strong {
  display: block;
  margin-bottom: 10px;
}

.landing-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.landing-stat {
  border-radius: 18px;
  padding: 16px 16px 14px;
}

.landing-stat strong {
  display: block;
  font-size: 2rem;
  line-height: 1;
  margin-bottom: 6px;
}

.landing-stat span {
  display: block;
  font-weight: 700;
  margin-bottom: 8px;
}

.landing-stat p {
  margin: 0;
  font-size: 0.92rem;
  line-height: 1.5;
}

.landing-section {
  margin-top: 22px;
  padding: 22px;
  border-radius: 24px;
}

.landing-section-header {
  max-width: 64ch;
  margin-bottom: 16px;
}

.landing-section-header h2 {
  font-size: clamp(1.8rem, 4vw, 2.7rem);
  margin-bottom: 8px;
}

.landing-grid {
  display: grid;
  gap: 14px;
}

.landing-grid.cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.landing-grid.cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.landing-grid.cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }

.landing-panel,
.landing-step,
.landing-chapter,
.option-card,
.landing-callout {
  border-radius: 20px;
  padding: 18px;
}

.landing-panel p,
.landing-step p,
.landing-chapter p,
.option-card p,
.landing-callout p {
  line-height: 1.63;
}

.landing-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.landing-tags span {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--landing-accent-soft) 78%, white 22%);
  border: 1px solid var(--landing-line);
  font-size: 0.85rem;
}

.landing-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
}

.landing-step-number,
.landing-chapter-number {
  display: inline-flex;
  margin-bottom: 12px;
  color: var(--landing-accent);
  font-size: 0.8rem;
}

.landing-callout {
  margin-top: 20px;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--landing-accent-soft) 56%, white 44%) 0%, rgba(255,255,255,0.82) 100%);
}

.landing-callout h2 {
  font-size: 1.6rem;
  margin-bottom: 8px;
}

.landing-band {
  display: grid;
  gap: 14px;
  grid-template-columns: 1.25fr 0.95fr;
  align-items: stretch;
}

.landing-bullets {
  margin: 0;
  padding-left: 20px;
  line-height: 1.7;
}

.landing-monobox {
  border-radius: 18px;
  padding: 16px;
  background: rgba(255,255,255,0.52);
  border: 1px solid var(--landing-line);
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.88rem;
  line-height: 1.75;
  white-space: pre-wrap;
}

.landing-instrument-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.landing-instrument-list span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255,255,255,0.72);
  border: 1px solid var(--landing-line);
  font-size: 0.92rem;
}

.landing-chapter-list {
  display: grid;
  gap: 12px;
}

.landing-chapter {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 14px;
  align-items: start;
}

.landing-footer {
  margin-top: 26px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  font-size: 0.94rem;
}

.landing-footer p { margin: 0; max-width: 58ch; line-height: 1.6; }

.option-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.option-preview {
  height: 110px;
  border-radius: 16px;
  margin-bottom: 16px;
  border: 1px solid var(--landing-line);
  background:
    linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.38)),
    linear-gradient(180deg, color-mix(in srgb, var(--landing-accent-soft) 84%, white 16%) 0%, transparent 100%);
  position: relative;
  overflow: hidden;
}

.option-preview::after {
  content: "";
  position: absolute;
  inset: 16px;
  border-radius: 14px;
  border: 1px dashed color-mix(in srgb, var(--landing-accent) 32%, transparent);
}

.option-dot {
  position: absolute;
  display: block;
  border-radius: 999px;
  background: color-mix(in srgb, var(--landing-accent) 82%, white 18%);
}

.option-dot-a { width: 110px; height: 20px; top: 18px; left: 18px; }
.option-dot-b { width: 160px; height: 16px; top: 48px; left: 18px; opacity: 0.85; }
.option-dot-c { width: 76px; height: 56px; bottom: 18px; right: 18px; opacity: 0.72; }

.option-card.option-signal .option-preview {
  background:
    linear-gradient(rgba(37, 94, 178, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 94, 178, 0.06) 1px, transparent 1px),
    linear-gradient(180deg, rgba(255,255,255,0.92), rgba(220,231,251,0.78));
  background-size: 20px 20px, 20px 20px, auto;
}

.option-card.option-field-guide .option-preview {
  background:
    linear-gradient(180deg, rgba(50, 98, 78, 0.06) 0, rgba(50, 98, 78, 0.06) 1px, transparent 1px, transparent 22px),
    linear-gradient(180deg, rgba(255,255,255,0.94), rgba(222,234,223,0.68));
  background-size: auto 22px, auto;
}

@media (max-width: 960px) {
  .landing-hero,
  .landing-band {
    grid-template-columns: 1fr;
  }

  .landing-grid.cols-4 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .landing-shell {
    padding: 18px 14px 70px;
  }

  .landing-hero {
    padding: 20px;
  }

  .landing-hero h1 {
    max-width: none;
    font-size: clamp(2.5rem, 14vw, 4.1rem);
  }

  .landing-grid.cols-2,
  .landing-grid.cols-3,
  .landing-grid.cols-4,
  .landing-chapter {
    grid-template-columns: 1fr;
  }
}
"""


def _atlas_page(context: dict[str, Any], variants: list[dict[str, Any]], current_path: str) -> str:
    repo_url = context["repo_url"]
    tags = "".join(
        f"<span>{escape(name)}</span>" for name in context["instrument_names"]
    )
    return f"""<!doctype html>
<html lang="en">
  {_head("A Person Index | Atlas of Personhood Systems", "A Person Index keeps personhood frameworks intact, translates them through a house interlingua, and lets downstream runtimes call the map without flattening it.")}
  <body class="landing-body theme-atlas">
    <div class="landing-shell">
      {_nav("atlas", repo_url)}
      <section class="landing-hero">
        <div class="landing-hero-copy">
          <p class="landing-label">Atlas / flagship direction</p>
          <h1>Finally, a map where personhood frameworks can talk.</h1>
          <p class="landing-lede">A Person Index keeps each framework in its own terms, then layers motifs, index programs, program packs, and research-safe return contracts on top. It is the comparative atlas for systems that were never built to speak to each other directly.</p>
          <div class="landing-actions">
            <a class="landing-button primary" href="search.html">Browse the corpus</a>
            <a class="landing-button subtle" href="landing-options.html">Compare all three directions</a>
            <a class="landing-button" href="protocols.html">See programs</a>
          </div>
        </div>
        <div class="landing-hero-side">
          <aside class="landing-quote">
            <strong>The job is not to flatten these systems into one bucket.</strong>
            <p>The job is to preserve them, dimension them, and make their overlaps, divergences, and incommensurabilities legible.</p>
          </aside>
          <aside class="landing-sidecard">
            <p class="landing-kicker">Current shipped slice</p>
            <p>{context["stats"]["frameworks"]} framework records, {context["stats"]["motifs"]} motifs, {context["stats"]["programs"]} index programs, {context["stats"]["packs"]} curated packs, and {context["stats"]["research_models"]} research contribution models.</p>
          </aside>
        </div>
      </section>

      <section class="landing-metrics">
        {_stat_card(str(context["stats"]["frameworks"]), "Seeded framework records", "Source-backed canonical records across psychometric, symbolic, relational, and workplace systems.")}
        {_stat_card(str(context["stats"]["motifs"]), "House motifs", "The translation handles that let different systems point into shared circuitry without claiming equivalence.")}
        {_stat_card(str(context["stats"]["programs"]), "Index programs", "Reusable higher-order analyses like ILENS, Translation Memo, Human Model Card, and Paradox Finder.")}
        {_stat_card(str(context["stats"]["packs"]), "Program packs", "Scoped runtime bundles that downstream systems can call instead of reconstructing the method by hand.")}
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">Why this exists</p>
          <h2>One repository, four kinds of leverage.</h2>
          <p>This is not just a corpus. It is a layered substrate for preserving frameworks faithfully, translating across them, composing analyses from smaller lego pieces, and accepting only research-safe return traffic.</p>
        </div>
        <div class="landing-grid cols-4">
          {_panel("Registry", "Keep the source intact", "Store each framework in its own language with claims, constructs, resources, risks, and use cases preserved rather than averaged away.", ["source-truth", "provenance"])}
          {_panel("Synthesis", "Translate without pretending equivalence", "Use motifs, mappings, and interaction hypotheses as a house interlingua so overlap and incommensurability can both be named.", ["motifs", "comparative map"])}
          {_panel("Programs", "Compose methods like legos", "Build Paradox Finder, Translation Memo, ILENS, and future programs from smaller reusable techniques instead of leaving the craft implicit.", ["techniques", "index programs"])}
          {_panel("Research", "Return signal safely", "Downstream runtimes can send back result atoms, mapping votes, and distilled observations without polluting canonical source records.", ["result atoms", "promotion policy"])}
        </div>
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">How the stack works</p>
          <h2>Archive, translate, compose, return.</h2>
        </div>
        <div class="landing-steps">
          {_step("01", "Canonical records", "Frameworks stay attributable, versioned, and source-faithful inside the registry layer.")}
          {_step("02", "Motifs and mappings", "House synthesis attaches motifs and comparative handles without erasing epistemic differences.")}
          {_step("03", "Index programs", "Named programs compose reusable techniques into stable analysis patterns.")}
          {_step("04", "Program packs", "Curated or dynamic bundles hydrate a program with the exact scope and return contracts a runtime needs.")}
        </div>
      </section>

      <section class="landing-band">
        <section class="landing-section">
          <div class="landing-section-header">
            <p class="landing-overline">Who it serves</p>
            <h2>A shared substrate, not a private ontology.</h2>
          </div>
          <div class="landing-grid cols-3">
            {_panel("Curators", "Version the map itself", "Extend the corpus, refine the ontology, and keep the comparative layer coherent over time.", ["git-native", "reviewable"])}
            {_panel("Agents", "Arrive to a real surface", "Read manifested service primitives, query motifs and interactions, and fetch packs instead of guessing the choreography.", ["CLI", "MCP", "JSON"])}
            {_panel("Runtimes", "Call packs, not vibes", "Systems like GNOMY do person-level synthesis locally while depending on this repo for shared methods and governance.", ["consumer-agnostic", "runtime-ready"])}
          </div>
        </section>
        <aside class="landing-callout">
          <p class="landing-overline">Current canonical slice</p>
          <h2>Fifteen seeded systems are already in play.</h2>
          <p>The current corpus is still instrument-centered, but the broader framework, technique, and program model is already encoded.</p>
          <div class="landing-instrument-list">{tags}</div>
        </aside>
      </section>

      <footer class="landing-footer">
        <p>The recommended public default is this Atlas direction. The other two options push the same product through different communicative lenses so you can choose the right public face.</p>
        <div class="landing-actions">
          <a class="landing-button subtle" href="landing-options.html">See all options</a>
          <a class="landing-button" href="{escape(repo_url)}">Open GitHub</a>
        </div>
      </footer>
    </div>
  </body>
</html>
"""


def _signal_page(context: dict[str, Any], variants: list[dict[str, Any]]) -> str:
    repo_url = context["repo_url"]
    return f"""<!doctype html>
<html lang="en">
  {_head("A Person Index | Signal Stack", "A systems-facing landing page for A Person Index that emphasizes the pipeline from canonical records to motifs, programs, runtime packs, and research-safe return traffic.")}
  <body class="landing-body theme-signal">
    <div class="landing-shell">
      {_nav("signal", repo_url)}
      <section class="landing-hero">
        <div class="landing-hero-copy">
          <p class="landing-label">Signal Stack / systems-facing direction</p>
          <h1>From frameworks to circuitry.</h1>
          <p class="landing-lede">A Person Index is the layer that turns disconnected personality and typing systems into something runtimes can actually compute with. Canonical records become motifs. Motifs become programs. Programs become packs. Packs become usable runtime dependencies.</p>
          <div class="landing-actions">
            <a class="landing-button primary" href="protocols.html">Browse programs</a>
            <a class="landing-button subtle" href="protocol-packs.html">Browse packs</a>
            <a class="landing-button" href="landing-options.html">See all directions</a>
          </div>
        </div>
        <div class="landing-hero-side">
          <aside class="landing-sidecard">
            <p class="landing-kicker">Runtime promise</p>
            <p>Downstream systems should not need to reconstruct the map. They should query it, trace it, and call it.</p>
          </aside>
          <aside class="landing-monobox">frameworks → motifs → interactions → programs → packs → runtimes → research-safe returns</aside>
        </div>
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">Signal path</p>
          <h2>The comparative pipeline in six steps.</h2>
        </div>
        <div class="landing-steps">
          {_step("01", "Canonical records", f"{context['stats']['frameworks']} seeded framework records with claims, resources, crosswalks, risks, and use cases.")}
          {_step("02", "Motifs", f"{context['stats']['motifs']} house motifs and {context['stats']['mappings']} mappings turn framework-local outputs into translation handles.")}
          {_step("03", "Interactions", f"{context['stats']['interactions']} interaction hypotheses preserve tension, masking, compensation, and reinforcement rather than forcing coherence.")}
          {_step("04", "Index programs", f"{context['stats']['programs']} composed analyses encode reusable comparative craft such as ILENS and Paradox Finder.")}
          {_step("05", "Program packs", f"{context['stats']['packs']} curated packs and dynamic pack assembly give runtimes a stable execution bundle.")}
          {_step("06", "Research returns", f"{context['stats']['research_models']} contribution models and a staged promotion policy keep return traffic useful without collapsing it into truth.")}
        </div>
      </section>

      <section class="landing-band">
        <section class="landing-section">
          <div class="landing-section-header">
            <p class="landing-overline">Service surfaces</p>
            <h2>Arrive to a real interface, not a pile of files.</h2>
          </div>
          <div class="landing-grid cols-2">
            {_panel("CLI", "Local, deterministic, scriptable", "Validation, build, docs, compare, trace, program-pack, result-atom-schema, and research-promotion are all callable from the terminal.", ["maintainers", "local agents"])}
            {_panel("MCP", "Agent-native retrieval", "The read-only MCP adapter exposes manifest, motif tracing, interaction lookup, program specs, program packs, and research models to downstream agents.", ["stdio", "read-only"])}
            {_panel("Generated JSON", "Portable artifacts", "Machine-readable outputs make the substrate usable even when a consumer does not want to call live tools.", ["generated", "cacheable"])}
            {_panel("Static docs", "Human comprehension", "The site stays browsable and legible while sharing the same source of truth as the runtime-facing surfaces.", ["docs", "public face"])}
          </div>
        </section>
        <aside class="landing-callout">
          <p class="landing-overline">Current surface area</p>
          <h2>Enough structure to use today.</h2>
          <div class="landing-metrics">
            {_stat_card(str(context["stats"]["programs"]), "Programs", "Composable analyses")}
            {_stat_card(str(context["stats"]["packs"]), "Packs", "Curated runtime bundles")}
            {_stat_card(str(context["stats"]["research_models"]), "Models", "Return traffic contracts")}
          </div>
        </aside>
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">What a runtime can do on arrival</p>
          <h2>Call the substrate directly.</h2>
        </div>
        <div class="landing-grid cols-3">
          {_panel("Trace", "Map a framework into motifs", "A runtime can start from MBTI, Enneagram, Big Five, or any other seeded framework and trace the comparative handles already stored here.", ["trace", "motifs"])}
          {_panel("Compose", "Fetch packs for known tasks", "When the task is already known, the runtime can fetch a program pack instead of assembling techniques, mappings, and interactions ad hoc.", ["program-pack", "runtime bundle"])}
          {_panel("Return", "Send back only structured signal", "Research-safe return traffic uses result atoms, mapping votes, pairwise judgments, and distilled observations rather than raw personal corpora.", ["research stream", "privacy-minimizing"])}
        </div>
      </section>

      <footer class="landing-footer">
        <p>The Signal Stack direction is the clearest option if the audience is runtime builders, agent developers, or people deciding whether to depend on this repo programmatically.</p>
        <div class="landing-actions">
          <a class="landing-button subtle" href="landing-options.html">Compare directions</a>
          <a class="landing-button" href="{escape(repo_url)}">Open GitHub</a>
        </div>
      </footer>
    </div>
  </body>
</html>
"""


def _field_guide_page(context: dict[str, Any], variants: list[dict[str, Any]]) -> str:
    repo_url = context["repo_url"]
    tags = "".join(
        f"<span>{escape(name)}</span>" for name in context["instrument_names"][:10]
    )
    return f"""<!doctype html>
<html lang="en">
  {_head("A Person Index | Field Guide", "A minimal field-guide landing page for A Person Index focused on curation, boundaries, and research-ready clarity.")}
  <body class="landing-body theme-field-guide">
    <div class="landing-shell">
      {_nav("field-guide", repo_url)}
      <section class="landing-hero">
        <div class="landing-hero-copy">
          <p class="landing-label">Field Guide / minimal research-facing direction</p>
          <h1>A field guide to systems that describe a person.</h1>
          <p class="landing-lede">A Person Index is a maintained comparative substrate for tests, typologies, symbolic systems, and adjacent personhood frameworks. It keeps them intact, marks the house layer explicitly, and gives downstream systems a safer way to use the resulting map.</p>
          <div class="landing-actions">
            <a class="landing-button primary" href="research.html">See the research layer</a>
            <a class="landing-button subtle" href="landing-options.html">Compare directions</a>
            <a class="landing-button" href="motifs.html">See motifs</a>
          </div>
        </div>
        <div class="landing-hero-side">
          <aside class="landing-quote">
            <strong>Not a quiz. Not a score report. Not a single theory of the person.</strong>
            <p>It is the map, the method library, and the boundary surface between canonical records, house synthesis, programs, and staged evidence.</p>
          </aside>
          <aside class="landing-sidecard">
            <p class="landing-kicker">Current footprint</p>
            <p>{context["stats"]["frameworks"]} records, {context["stats"]["motifs"]} motifs, {context["stats"]["research_models"]} contribution models, and a live MCP surface for agents.</p>
          </aside>
        </div>
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">Four working rules</p>
          <h2>What keeps this index from turning into soup.</h2>
        </div>
        <div class="landing-chapter-list">
          {_chapter("01", "Keep the source intact", "Source claims stay attributable. Official language is stored faithfully, even when the house view disagrees with it.")}
          {_chapter("02", "Translate without flattening", "Motifs and mappings exist to compare frameworks, not to pretend that every system measures the same thing.")}
          {_chapter("03", "Make methods composable", "Paradox Finder, ILENS, and future programs should be legible composites of smaller techniques, not giant opaque prompts.")}
          {_chapter("04", "Accept evidence in stages", "Research-safe returns come back as structured contributions and only become house synthesis after review and promotion policy.")}
        </div>
      </section>

      <section class="landing-band">
        <section class="landing-section">
          <div class="landing-section-header">
            <p class="landing-overline">In bounds</p>
            <h2>What belongs here.</h2>
          </div>
          <div class="landing-grid cols-2">
            {_panel("Canonical", "Framework records and ontology", "Claims, resources, annotations, inferences, crosswalks, risks, use cases, and notes for the current seeded corpus.", ["registry", "ontology"])}
            {_panel("House layer", "Motifs, interactions, and methods", "Translation handles, interaction hypotheses, techniques, programs, and packs that downstream systems can actually depend on.", ["house synthesis", "methods"])}
          </div>
        </section>
        <aside class="landing-callout">
          <p class="landing-overline">Out of bounds</p>
          <h2>What this repo should refuse.</h2>
          <ul class="landing-bullets">
            <li>Raw personal chat logs or narrative corpora as canonical source truth</li>
            <li>One-off person analysis that belongs inside a consumer runtime</li>
            <li>Consumer quiz UX, scoring engines, or dashboard theater</li>
            <li>Unreviewed research claims silently promoted into the map</li>
          </ul>
        </aside>
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">Current slice</p>
          <h2>The corpus is already broad enough to be useful.</h2>
          <p>Today’s seeded slice spans psychometric, symbolic, workplace, and relational systems, which is enough to make the translation layer genuinely informative instead of decorative.</p>
        </div>
        <div class="landing-instrument-list">{tags}</div>
      </section>

      <footer class="landing-footer">
        <p>The Field Guide direction is the clearest option if the audience is curators, researchers, writers, or anyone who needs the repo to feel disciplined, sober, and durable.</p>
        <div class="landing-actions">
          <a class="landing-button subtle" href="landing-options.html">Compare directions</a>
          <a class="landing-button" href="{escape(repo_url)}">Open GitHub</a>
        </div>
      </footer>
    </div>
  </body>
</html>
"""


def _options_gallery_page(context: dict[str, Any], variants: list[dict[str, Any]]) -> str:
    repo_url = context["repo_url"]
    cards = "\n".join(_option_card(variant) for variant in variants)
    return f"""<!doctype html>
<html lang="en">
  {_head("A Person Index | Landing Directions", "Three different landing-page directions for A Person Index: Atlas, Signal Stack, and Field Guide.")}
  <body class="landing-body theme-atlas">
    <div class="landing-shell">
      {_nav("options", repo_url)}
      <section class="landing-hero">
        <div class="landing-hero-copy">
          <p class="landing-label">Landing directions</p>
          <h1>Three ways to present the same substrate.</h1>
          <p class="landing-lede">These options do not change the product. They change the public emphasis. Atlas is the strongest public default. Signal Stack is best for technical/runtime audiences. Field Guide is best for curator and research audiences.</p>
          <div class="landing-actions">
            <a class="landing-button primary" href="index.html">Open the recommended default</a>
            <a class="landing-button subtle" href="search.html">Browse the current site</a>
          </div>
        </div>
        <div class="landing-hero-side">
          <aside class="landing-sidecard">
            <p class="landing-kicker">Selection rule</p>
            <p>If the site should first sell the idea, choose Atlas. If it should first explain the runtime architecture, choose Signal Stack. If it should first establish seriousness and scope discipline, choose Field Guide.</p>
          </aside>
        </div>
      </section>

      <section class="landing-section">
        <div class="landing-section-header">
          <p class="landing-overline">Option gallery</p>
          <h2>Choose the public face that matches the audience.</h2>
        </div>
        <div class="option-gallery">{cards}</div>
      </section>
    </div>
  </body>
</html>
"""


def landing_site_bundle(context: dict[str, Any]) -> dict[str, Any]:
    variants = landing_variants_manifest()
    pages = {
        "index.html": _clean_markup(_atlas_page(context, variants, "index.html")),
        "landing-atlas.html": _clean_markup(_atlas_page(context, variants, "landing-atlas.html")),
        "landing-signal.html": _clean_markup(_signal_page(context, variants)),
        "landing-field-guide.html": _clean_markup(_field_guide_page(context, variants)),
        "landing-options.html": _clean_markup(_options_gallery_page(context, variants)),
    }
    return {
        "variants": variants,
        "css": _clean_markup(landing_css()),
        "pages": pages,
    }
