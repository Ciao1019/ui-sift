<div align="center">

# UI Sift

**Curated components. Refined interfaces.**

A React-first agent skill for clean interfaces and thoughtful interactions.

[![Version 1.0](https://img.shields.io/badge/version-1.0-18181b)](https://github.com/Ciao1019/ui-sift/releases/tag/v1.0)
[![MIT License](https://img.shields.io/badge/license-MIT-18181b)](LICENSE)
[![Tests](https://github.com/Ciao1019/ui-sift/actions/workflows/validate.yml/badge.svg)](https://github.com/Ciao1019/ui-sift/actions/workflows/validate.yml)
[![Tracked npx installs](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FCiao1019%2Fui-sift%2Fmain%2F.github%2Fbadges%2Finstalls.json)](https://skills.sh/)

English · [简体中文](README.zh-CN.md)

</div>

UI Sift helps coding agents choose suitable components, find official skills and MCP tools, and turn those components into a coherent product. Its focus is clear hierarchy, restrained motion, real interactions, and a consistent visual language.

It adapts to your project’s framework, design system, and constraints. Use it for a small polish pass, a new page, an AI interface, a document workspace, or a UI review.

## Framework support

**React is the primary focus.** Most curated components target the React ecosystem, including many shadcn/ui and Tailwind-based implementations. The catalog also contains a few sources for other frameworks; components are not interchangeable across frameworks.

| Framework or use | Catalog coverage |
| --- | --- |
| React / Next.js | Main component coverage. Verify each component’s React version, dependencies, and client/server rendering requirements. |
| Vue / Nuxt | nxui; DayFlow provides a Vue integration. React components cannot be installed as Vue components. |
| Angular / Svelte | DayFlow calendar integrations; not a full component catalog for these frameworks. |
| Go templ | shadcn-templ, which is distinct from React’s shadcn/ui. |
| Visual exploration | Variant is a design reference, not a framework-specific runtime dependency. |

The skill checks the target framework before selecting components. Design guidance can transfer between stacks; source code must match the target project. See the [catalog](references/catalog.md) for component-level boundaries.

## Install in one command

Run this from your project directory. The installer lets you choose your coding agent:

```bash
npx skills add Ciao1019/ui-sift --skill ui-sift
```

For a non-interactive install targeting a specific agent:

```bash
npx --yes skills add Ciao1019/ui-sift --skill ui-sift --agent codex --yes
```

Replace `codex` with `claude-code`, `cursor`, or another [supported agent](https://github.com/vercel-labs/skills#supported-agents). Add `--global` to install for that agent across projects; installation is project-scoped by default. Use `--copy` if you prefer copies to symlinks.

The current installer requires **Node.js 22.20+**, npm/npx, and Git. The skill itself is Markdown and JSON; its optional helper scripts use **Python 3.9+ with no third-party Python dependencies**.

<details>
<summary>Preview or install manually</summary>

List the skill before installing:

```bash
npx skills add Ciao1019/ui-sift --list
```

For a manual install, download the source or a [release](https://github.com/Ciao1019/ui-sift/releases), put the complete `ui-sift` folder in your agent’s supported skill directory, and preserve its file structure. The entry point is [SKILL.md](SKILL.md). Reload skills if your agent requires it.

</details>

## Ask for a better interface

```text
Use $ui-sift to refine this dashboard. Keep the existing design system,
make filters and empty states easier to use, and avoid new dependencies.
```

```text
Use $ui-sift to build a document review page. Selecting a field should
locate its source, save failures should preserve edits, and the primary
workflow must work on narrow screens.
```

```text
Use $ui-sift to review this page. Report the three issues that most affect
usability, with evidence. Do not change the code yet.
```

Invocation syntax varies by agent; you can also ask it to read `SKILL.md`. The detailed skill guidance and reference library are currently written in Simplified Chinese. These English examples can be used with agents that understand that guidance; translations are welcome.

## What it brings

| Capability | How it helps |
| --- | --- |
| **Design judgment** | Establish hierarchy, density, typography, color roles, and a useful interaction detail before adding decoration. |
| **Curated discovery** | Search 22 UI sources and 69 component groups through 30 Chinese/English intent categories. |
| **Official knowledge** | Find a source’s documented skill, MCP, llms index, registry, package, or repository. |
| **Practical integration** | Preserve your stack, align tokens and shared primitives, wire data and events, and cover necessary states. |
| **Proportionate workflow** | Keep small edits lightweight; expand into briefs, contracts, and evidence for larger tasks. |
| **Honest verification** | Separate downloaded code, installed components, working behavior, visual review, and unverified work. |

## The curated library

| Area | Sources to explore |
| --- | --- |
| AI interfaces and content | [Tool UI](https://www.tool-ui.com/docs/overview), [assistant-ui](https://www.assistant-ui.com/docs/ui/syntax-highlighting), [prompt-kit](https://www.prompt-kit.com/), [Lobe UI](https://ui.lobehub.com/components/markdown), [Plate](https://platejs.org/) |
| Documents and structure | [Extend UI](https://www.extend.ai/ui/docs), [mindmapcn](https://mindmapcn.vercel.app/), [Kibo UI](https://www.kibo-ui.com/), [UI TripleD](https://ui.tripled.work/) |
| Dates and input | [DayFlow](https://calendar.dayflow.studio/), [shadcn/ui Calendar](https://ui.shadcn.com/docs/components/calendar), [Cuicui Signature](https://cuicui.day/application-ui/signature) |
| Application UI and interaction | [Astryx](https://astryx.atmeta.com/components), [moumenlab](https://lab.moumen.dev/components), [GodUI](https://godui.design/docs/components), [Libraries.dev](https://libraries.dev/beam), [Heroicons Animated](https://www.heroicons-animated.com/) |
| Framework-specific components | [nxui](https://nxui.geoql.in/docs), [shadcn-templ](https://shadcn-templ.com/) |
| Page composition and exploration | [Ruixen UI](https://ruixen.com/), [Shadcn Studio](https://shadcnstudio.com/), [Variant](https://variant.com/community) |

The [catalog](references/catalog.md) explains strengths, promising components, and tradeoffs. The [acquisition guide](references/acquisition.md) records official skills/MCP discovery and source retrieval paths. Entries are research notes, not claims that every integration has been tested. Verify the selected component’s current API, compatibility, and license before use.

## Four optional tools

Run these from the installed skill folder or a clone of this repository. Output filenames are examples; use a task-specific directory.

```bash
# Inspect a target package without running its scripts
python3 scripts/profile_project.py /path/to/frontend-package > profile.json

# Find compatible candidates using the package profile
python3 scripts/recommend.py "document review" --framework auto --profile profile.json

# Download one official reference to a new file; does not execute or install it
python3 scripts/fetch_reference.py moumen --out moumen-llms.txt

# Check the completeness of an evidence record
python3 scripts/check_delivery.py report.json --evidence-root /path/to/evidence
```

Scanning and recommendation run offline. Downloading is limited to recorded official hosts, checks redirects and payloads, and refuses to overwrite files. A complete evidence record does not mean the interface has passed a visual or functional review.

See the [tool manual](references/tooling.md) for options and limits. On Windows, use your available Python launcher, such as `py -3`.

## Inside the skill

```text
ui-sift/
├── SKILL.md                 # Agent entry point and task routing
├── agents/                  # Optional agent UI metadata
├── references/              # Design, catalog, acquisition, integration, review
├── data/                    # Sources, component candidates, intent vocabulary
├── scripts/                 # Four standard-library Python tools
├── templates/               # Design brief and evidence record
├── tests/                   # Deterministic tool regression tests
└── evals/                   # Routing cases and end-to-end evaluation scenarios
```

Supporting documents load when needed. A minor component adjustment does not require a full brief, every tool, or a JSON report.

## Validation and contributing

```bash
python3 -m unittest discover -s tests -v
```

The tool suite contains **28 tests**, including a regression test that exercises **18 routing cases**. These check framework filtering, local scanning, download handling, and evidence references. Seven [end-to-end agent scenarios](evals/manual-scenarios.md) are supplied for future evaluation; their design outcomes have not been validated.

Contributions are welcome: focused component recommendations, updated official access paths, translations, and reproducible failures. When adding a source, include its framework, a concrete strength, how it differs from existing entries, and official evidence. Keep the [catalog](references/catalog.md), [acquisition guide](references/acquisition.md), and [data](data/resources.json) consistent, then run the relevant tests.

## Acknowledgments and license

The workflow draws organizational lessons from [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design), [Vercel agent-skills](https://github.com/vercel-labs/agent-skills), and [Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills). The [research notes](references/research-notes.md) explain the scope and verification limits. UI Sift does not bundle those projects’ skills or third-party component source.

🙏 致谢
公开站点 UI 与排版设计借鉴自 astro-theme-retypeset。
感谢 LinuxDo 社区的支持。

[MIT](LICENSE) for UI Sift’s original code and documentation. Referenced libraries, components, templates, and paid assets retain their own licenses.
