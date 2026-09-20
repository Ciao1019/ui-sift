<div align="center">

# UI Sift

**精选组件，精修界面。**

以 React 为主，面向简洁界面与精致交互的开源 Agent Skill。

[![版本 1.0](https://img.shields.io/badge/version-1.0-18181b)](https://github.com/Ciao1019/ui-sift/releases/tag/v1.0)
[![MIT 许可](https://img.shields.io/badge/license-MIT-18181b)](LICENSE)
[![测试](https://github.com/Ciao1019/ui-sift/actions/workflows/validate.yml/badge.svg)](https://github.com/Ciao1019/ui-sift/actions/workflows/validate.yml)
[![npx 安装次数](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FCiao1019%2Fui-sift%2Fmain%2F.github%2Fbadges%2Finstalls.json)](https://skills.sh/)

[English](README.md) · 简体中文

</div>

UI Sift 帮助编程 Agent 挑选适合的组件、发现官方 skills 和 MCP，并把来自不同来源的能力整合成统一的产品界面。关注清晰的层级、克制的动效、真实的交互和一致的视觉语言。

它依据使用者自己的框架、设计系统与约束工作，适合局部打磨、新页面、AI 对话、文档工作台和 UI 评审，不预设工程目录、包管理器或业务实现。

## 框架支持范围

**React 是主要适用方向。** 精选组件大多来自 React 生态，包含许多基于 shadcn/ui 和 Tailwind 的实现。目录也收录了少量其他框架的来源，不同框架的组件不能直接混用。

| 框架或用途 | 目录覆盖范围 |
| --- | --- |
| React / Next.js | 主要组件覆盖。仍需逐组件核对 React 版本、依赖以及客户端 / 服务端渲染要求。 |
| Vue / Nuxt | nxui；DayFlow 提供 Vue 集成。不能直接安装 React 组件作为 Vue 组件使用。 |
| Angular / Svelte | DayFlow 的日历集成，不代表这两个框架拥有完整的组件目录。 |
| Go templ | shadcn-templ，与 React 的 shadcn/ui 是不同项目。 |
| 视觉探索 | Variant 用于设计参考，不作为某个框架的运行时依赖。 |

Skill 会先确认目标框架再选组件。设计方法可以跨技术栈借鉴，源码必须与目标工程匹配；具体边界见[资源目录](references/catalog.md)。

## 一条命令安装

在你的项目目录执行，安装器会让你选择使用的编程 Agent：

```bash
npx skills add Ciao1019/ui-sift --skill ui-sift
```

需要指定 Agent 并跳过交互确认时：

```bash
npx --yes skills add Ciao1019/ui-sift --skill ui-sift --agent codex --yes
```

将 `codex` 替换为 `claude-code`、`cursor` 或其他[受支持的 Agent](https://github.com/vercel-labs/skills#supported-agents)。默认安装到当前项目；添加 `--global` 可为指定 Agent 全局安装。偏好文件副本时可加 `--copy`。

当前安装器需要 **Node.js 22.20+**、npm/npx 和 Git。Skill 本体由 Markdown 与 JSON 构成；可选辅助脚本需要 **Python 3.9+，没有第三方 Python 依赖**。

<details>
<summary>先查看，或手动安装</summary>

列出仓库中的 skill：

```bash
npx skills add Ciao1019/ui-sift --list
```

也可以下载源码或 [Release](https://github.com/Ciao1019/ui-sift/releases)，将完整的 `ui-sift` 文件夹放进所用 Agent 支持的 skill 目录，保留相邻文件结构。入口是 [SKILL.md](SKILL.md)，如宿主要求则重新加载 skills。

</details>

## 怎么使用

```text
用 $ui-sift 打磨这个后台列表。保留现有设计系统，
让筛选、空状态和错误恢复更顺手，不新增依赖。
```

```text
用 $ui-sift 做文档审核页。点击字段定位原文，
保存失败时保留修改，桌面与窄屏都能完成主流程。
```

```text
用 $ui-sift 评审这页 UI，给出最影响使用的三个问题和实际证据，
暂时不要改代码。
```

不同 Agent 的调用语法可能不同，也可以直接让它读取 `SKILL.md`。当前详细指导与参考资料主要使用简体中文，欢迎贡献其他语言版本。

## 它能带来什么

| 能力 | 用处 |
| --- | --- |
| **设计判断** | 先确定信息层级、密度、排版、语义颜色与值得打磨的交互。 |
| **精选发现** | 通过 30 类中英文意图，检索 22 个来源、69 组组件候选。 |
| **官方知识** | 查找已公开的 skill、MCP、llms、registry、包或源码入口。 |
| **实际集成** | 适配已有技术栈，统一 tokens 和基础组件，接通数据、事件与必要状态。 |
| **按需工作流** | 小改动直接处理；复杂任务按需展开简报、组件契约和验收记录。 |
| **有依据的验证** | 区分下载、安装、业务可用、视觉检查和未验证事项。 |

## 精选资源

| 场景 | 候选来源 |
| --- | --- |
| AI 对话与内容 | [Tool UI](https://www.tool-ui.com/docs/overview)、[assistant-ui](https://www.assistant-ui.com/docs/ui/syntax-highlighting)、[prompt-kit](https://www.prompt-kit.com/)、[Lobe UI](https://ui.lobehub.com/components/markdown)、[Plate](https://platejs.org/) |
| 文档与结构 | [Extend UI](https://www.extend.ai/ui/docs)、[mindmapcn](https://mindmapcn.vercel.app/)、[Kibo UI](https://www.kibo-ui.com/)、[UI TripleD](https://ui.tripled.work/) |
| 日期与专项输入 | [DayFlow](https://calendar.dayflow.studio/)、[shadcn/ui Calendar](https://ui.shadcn.com/docs/components/calendar)、[Cuicui Signature](https://cuicui.day/application-ui/signature) |
| 应用界面与交互 | [Astryx](https://astryx.atmeta.com/components)、[moumenlab](https://lab.moumen.dev/components)、[GodUI](https://godui.design/docs/components)、[Libraries.dev](https://libraries.dev/beam)、[Heroicons Animated](https://www.heroicons-animated.com/) |
| 特定技术栈 | [nxui](https://nxui.geoql.in/docs)、[shadcn-templ](https://shadcn-templ.com/) |
| 页面组合与方向探索 | [Ruixen UI](https://ruixen.com/)、[Shadcn Studio](https://shadcnstudio.com/)、[Variant](https://variant.com/community) |

[资源目录](references/catalog.md)说明各来源的强项、值得看的组件和取舍；[接入指南](references/acquisition.md)记录官方 skills/MCP 与源码发现方式。采用前仍需核对目标组件当前 API、兼容性与许可，目录不代表所有组件或连接均经过实测。

## 四个可选工具

在安装后的 skill 目录或仓库副本中执行。输出文件名仅为示例，建议放进本次任务的输出目录。

```bash
# 只读扫描目标 package，不执行项目脚本
python3 scripts/profile_project.py /path/to/frontend-package > profile.json

# 按工程画像缩小候选范围
python3 scripts/recommend.py "文档审核，定位原文" --framework auto --profile profile.json

# 下载一份官方资料到新文件，不执行或安装
python3 scripts/fetch_reference.py moumen --out moumen-llms.txt

# 检查验收记录的完整性
python3 scripts/check_delivery.py report.json --evidence-root /path/to/evidence
```

扫描与检索离线运行。下载器限制已记录的官方域名，检查跳转和响应，拒绝覆盖已有文件。验收记录完整不代表界面已通过视觉或功能验证。

参数和边界见[工具手册](references/tooling.md)。Windows 可使用已安装的 Python 启动器，例如 `py -3`。

## 目录结构

```text
ui-sift/
├── SKILL.md                 # Agent 入口与任务路由
├── agents/                  # 可选的 Agent 界面元数据
├── references/              # 设计、目录、获取、集成与评审
├── data/                    # 来源、组件候选与需求词表
├── scripts/                 # 四个标准库 Python 工具
├── templates/               # 设计简报与验收记录模板
├── tests/                   # 确定性工具回归测试
└── evals/                   # 路由用例与端到端评估场景
```

参考资料按需读取。修改一个按钮不要求填写完整简报、运行所有工具或生成 JSON 报告。

## 验证与贡献

```bash
python3 -m unittest discover -s tests -v
```

工具测试包含 **28 项测试**，其中路由回归覆盖 **18 个需求场景**，检查框架过滤、工程扫描、下载处理与证据引用。另有 7 个[端到端 Agent 评估场景](evals/manual-scenarios.md)，其界面效果仍待实际评估。

欢迎贡献具体组件推荐、官方入口更新、翻译和可复现的问题。新增来源请注明技术栈、具体强项、与现有条目的区别及官方证据，同步维护[目录](references/catalog.md)、[接入指南](references/acquisition.md)和[数据](data/resources.json)，并运行相关测试。

🙏 致谢
公开站点 UI 与排版设计借鉴自 astro-theme-retypeset。
感谢 LinuxDo 社区的支持。

## 致谢与许可

工作流的组织方式参考了 [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)、[Vercel agent-skills](https://github.com/vercel-labs/agent-skills) 和 [Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills)。借鉴范围与验证边界见[研究说明](references/research-notes.md)，本包不捆绑这些项目的 skills 或第三方组件源码。

UI Sift 原创代码与文档采用 [MIT 许可证](LICENSE)。引用的组件库、模板、付费素材仍遵循各自许可。
