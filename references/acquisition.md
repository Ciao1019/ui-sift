# 官方接入与按需下载

最后核验：2026-09-17。下面的“确认”表示读到了官方说明，**不表示已经连接或测试了这些 MCP，也不表示已经安装对应 skill**。客户端配置格式、包版本、registry 和收费范围都会变化；实际采用时重新读取对应文档。

UI Sift 提供单份官方资料下载器，命令与响应检查见 [工具手册](tooling.md)。它可缓存 llms、Markdown、源码文本或内联 registry；获取后仍按本文件完成内容检查、组件安装与业务接线。脚本入口字段保存在 [资源数据](../data/resources.json)，有变更时同步更新。

## 先区分四种能力

| 能力 | 能解决什么 | 不能据此推断什么 |
| --- | --- | --- |
| 官方 skill / agent docs | 用法、流程、版本约定、配套脚本 | 不代表组件已安装，也不代表脚本无副作用 |
| 官方独立 MCP | 查组件、读文档、取源码等，取决于实际 tools | 不代表它使用 shadcn，也不意味着可以任意改全局配置 |
| shadcn MCP + registry | 通过现有 shadcn MCP 浏览 / 安装兼容 registry | 这是 registry 接入，不能冒称该库有独立 MCP 服务 |
| llms / Markdown / 源码 | 没有专门工具时的可执行知识来源 | HTML 首页不是 llms 索引，截图不是源码 |

已连接的官方工具优先使用。没有连接时，读取官方文档和源码仍可完成大多数任务；不要为一个小组件强制中断工作去配置 MCP。

## 22 个来源的核验表

“未确认”只表示本次检查的公开入口没有得到充分证据，不是断言官方没有。第三方同名 skills 必须验证作者与官方关联后才能标为官方。

| 来源 | 官方 skill / agent docs | MCP | 无专门工具时的获取路径 |
| --- | --- | --- | --- |
| Astryx | 确认 CLI 生成 agent docs；不等同标准 SKILL.md 包 | 确认独立远程服务 | [Working with AI](https://astryx.atmeta.com/docs/working-with-ai)、[安装](https://astryx.atmeta.com/docs/getting-started)、官方 CLI / 包 |
| Tool UI | 确认 [Agent Skills](https://www.tool-ui.com/docs/agent-skills) | 未确认独立服务；可评估 registry 路径 | [Quick Start](https://www.tool-ui.com/docs/quick-start)、[官方仓库](https://github.com/assistant-ui/tool-ui) |
| assistant-ui | 确认官方 skills 与发现索引 | 确认远程文档 MCP | [Agent Skills / MCP](https://www.assistant-ui.com/docs/llm)、[llms](https://www.assistant-ui.com/llms.txt) |
| Libraries.dev Beam | 官网说明 Pro 包含参数 skills；未获取付费文件 | 未确认 | [公开组件页](https://libraries.dev/beam)的 Install & Usage / Copy prompt、官方包；付费 preset 另算 |
| Lobe UI | 未确认 UI 专用官方 skill | 未确认 UI 文档专用服务 | [组件页](https://ui.lobehub.com/components/markdown)、[源码](https://github.com/lobehub/lobe-ui)；不能把 LobeHub 的一般 MCP 生态当作 Lobe UI 文档 MCP |
| mindmapcn | 未确认 | 未确认独立服务；有 shadcn registry | [llms](https://mindmapcn.mind-elixir.com/llms.txt)、[安装](https://mindmapcn.mind-elixir.com/docs/installation) |
| Extend UI | 未确认 | 未确认 UI 专用独立服务；有 shadcn registry | [文档与安装](https://www.extend.ai/ui/docs)、[源码](https://github.com/extend-hq/ui)；区别于 Extend 产品服务 |
| Kibo UI | 未确认 | 确认 [MCP Server](https://www.kibo-ui.com/docs/mcp) | [Setup](https://www.kibo-ui.com/docs/setup)、[源码](https://github.com/shadcnblocks/kibo) |
| Cuicui Signature | 未确认 | 未确认 | [组件页](https://cuicui.day/application-ui/signature)、[目标源码目录](https://github.com/damien-schneider/cuicui/tree/main/packages/ui/cuicui/application-ui/signature/react-signature) |
| DayFlow | 未确认 | 未确认 | [llms](https://calendar.dayflow.studio/llms.txt)、[框架文档](https://calendar.dayflow.studio/docs/introduction)、[源码](https://github.com/dayflow-js/dayflow) |
| nxui | 未确认 | 确认远程服务与 shadcn registry 两条路径 | [MCP 文档](https://nxui.geoql.in/docs/mcp)、[llms](https://nxui.geoql.in/llms.txt)、逐组件文档 |
| shadcn-templ | 未确认 | 未确认 | [安装](https://shadcn-templ.com/docs/installation)、[CLI](https://shadcn-templ.com/docs/cli)、[源码](https://github.com/axadrn/shadcn-templ)；用 Go templ 的工具链 |
| moumenlab | 未确认 | 未确认独立服务；有兼容 registry | [llms](https://lab.moumen.dev/llms.txt)里的逐组件 `/r/<name>.md` 含说明、用法与源码 |
| UI TripleD | 未确认 | 未确认独立服务 | [llms](https://ui.tripled.work/llms.txt)里的逐组件 `/md/*.md`、[源码](https://github.com/moumen-soliman/uitripled)、组件页的 copy / registry 入口 |
| GodUI | 未确认 | 确认本地 stdio 服务 | [MCP](https://godui.design/docs/mcp)、[llms](https://godui.design/llms.txt)、[安装](https://godui.design/docs/installation) |
| prompt-kit | 未确认 | 官方 [MCP 文档](https://www.prompt-kit.com/docs/mcp)采用 shadcn registry 方案 | [llms](https://www.prompt-kit.com/llms.txt)、[安装](https://www.prompt-kit.com/docs/installation)、[源码](https://github.com/ibelick/prompt-kit) |
| Heroicons Animated | 未确认 | 未确认独立服务；有 registry | [llms](https://www.heroicons-animated.com/llms.txt)、逐图标页、[源码](https://github.com/Aniket-508/heroicons-animated) |
| Plate | 未确认独立标准 skill；提供本地文档方案 | 确认官方文档采用 shadcn MCP + `@plate` registry | [MCP](https://platejs.org/docs/installation/mcp)、[Local Docs](https://platejs.org/docs/installation/docs)、[llms](https://platejs.org/llms.txt) |
| Ruixen UI | 未确认 | 未确认独立服务；有 shadcn registry | [llms](https://ruixen.com/llms.txt)、组件安装页、[源码](https://github.com/ruixenui/ruixen.com) |
| Shadcn Studio | 确认 MCP 配套 instructions / commands，未确认独立标准 skill | 确认 Studio MCP；权限与客户端条件须核对 | [官方 MCP 指南](https://shadcnstudio.com/docs/getting-started/shadcn-studio-mcp-server)、[llms](https://shadcnstudio.com/llms.txt)、具体组件 / block 页 |
| shadcn/ui | 确认 [Skills](https://ui.shadcn.com/docs/skills) | 确认官方通用 registry MCP | [MCP](https://ui.shadcn.com/docs/mcp)、[llms](https://ui.shadcn.com/llms.txt)、组件页 |
| Variant Community | 未确认 | 未确认 | 本次 [社区](https://variant.com/community)要求登录；用已授权浏览或用户提供的参考，不假定能导出组件 |

## 已确认的具体入口

这些是溯源信息，不是要求全部配置。MCP 的客户端配置按当前宿主文档适配，保留已有 servers；不能把一个网站的 Cursor JSON 原样写进其他工具配置。

### Astryx

- 文档公布远程 MCP：`https://astryx.atmeta.com/mcp`，提供 `search` 与 `get`。
- 官方 agent docs 生成命令：`npx @astryxdesign/cli init --features agents`。它会生成项目指令文件，先检查已有 AGENTS / CLAUDE / rules 和 CLI 当前合并机制；只做组件查询时不必运行初始化。
- CLI 支持组件、主题和文档查询；以已安装版本的 CLI 帮助为准。当前官网要求 React 19+，与项目版本核对。

### Tool UI、assistant-ui、shadcn/ui 的 skills

官网在核验时给出以下安装入口；使用项目已有执行器，先枚举可选 skills，再只选本次需要的内容。不要从命令样例推断未经文档支持的过滤参数。

```sh
# Tool UI 官方 Agent Skills 页
npx skills add https://github.com/assistant-ui/tool-ui --skill tool-ui

# assistant-ui 官方 Agent Skills 页：仓库可能含多个任务型 skills
npx skills add assistant-ui/skills

# shadcn/ui 官方 Skills 页（官网展示 pnpm 示例）
pnpm dlx skills add shadcn/ui
```

这三条是条件示例，不要整段执行。若不需要长期安装，可下载目标 `SKILL.md` 及它引用的必要资料至任务临时目录并阅读。Tool UI 文档列出的 `.agents/skills/tool-ui/SKILL.md` 在本次 raw `main` 地址检查返回 404，说明路径 / 分支仍需从当前官方仓库或 skills 工具定位；不要宣称下载成功。

assistant-ui 还公布：

- 远程 MCP：`https://www.assistant-ui.com/mcp`，Streamable HTTP。
- skill 发现索引：`https://www.assistant-ui.com/.well-known/agent-skills/index.json`。
- 站点 skill：`https://www.assistant-ui.com/skill.md`。
- `.md` 文档为当前索引建议的规范入口；`.mdx` 是部分地址兼容方式。

上面两个 skill 地址由官方 llms 索引声明，本次未逐个下载内容，实际使用先验证响应。

### Kibo、nxui、GodUI

- **Kibo**：官方文档给出 `https://www.kibo-ui.com/api/mcp/mcp`，示例通过 `mcp-remote` 连接。不要擅自简化成 `/mcp`；客户端配置位置仍以宿主文档为准。
- **nxui**：远程 MCP `https://nxui.geoql.in/mcp`；官方还提供 `@nxui` registry `https://nxui.geoql.in/r/{name}.json`。MCP 提供 list / get / install-command，不代表自动解决 Vue 与 React 的兼容性。
- **GodUI**：官方当前固定 stdio 包 `@godui/mcp@0.1.0`，从 `https://godui.design/r` 读 registry；CLI 安装入口为 `@godui/cli`。不要用拍脑袋的包名或把固定版本替成 latest。需要可复现来源时按官网 registry revision 方式处理。

### Plate、prompt-kit 与 shadcn registry

Plate 官方配置使用 `npx shadcn@latest mcp`，在 `components.json` 配置 `@plate` 为 `https://platejs.org/r/{name}.json`。如果已经有相同 shadcn MCP，优先复用，不为每个库起一个重复服务。文档推荐 local docs 与项目 Plate 版本对应。

prompt-kit 本次官方文档仍展示 `shadcn@canary mcp` 加 `REGISTRY_URL=https://www.prompt-kit.com/c/registry.json`。这是带版本背景的配置，不宣称可直接换成所有当前 shadcn CLI；采用时同时核对该库和 shadcn 文档，不通则读取组件 Markdown / 官方源码继续。

shadcn 官方 [MCP 文档](https://ui.shadcn.com/docs/mcp)确认支持符合其规范的第三方 registry。**有 JSON 地址不自动等于兼容**：检查 registry schema、目标 item、文件内容及依赖解析后再使用。

### Extend 与 Ruixen 的样式变体

Extend 当前文档明确要求：

```json
{
  "registries": {
    "@extend": "https://www.extend.ai/ui/r/styles/{style}/{name}.json"
  }
}
```

这只是需合并的片段，不能覆盖整个 `components.json`。官网说明旧 `/ui/r/{name}.json` 固定提供 Base UI，弃用的 default style 也需先迁移；不要把 registry 变更偷偷扩大为全项目迁移。

Ruixen 的官方 llms 区分 Tailwind v4 / v3 与 Radix / Base UI 路由，分别包括 `/r/[name]`、`/r/tw3/[name]`、`/r/baseui/[name]`、`/r/baseui/tw3/[name]`。方括号只是占位符，具体 item 必须来自真实组件页。

### Shadcn Studio

Studio MCP 与 shadcn 官方 MCP 是两套服务。其文档涉及 `shadcn-studio-mcp`、账号 / API key、Pro 功能，以及随客户端变化的支持范围。凭证仅通过宿主允许的配置方式提供，不能写入 skill、分享包或源码。

文档示例可能下载或生成 CLAUDE.md 等规则文件；不要直接覆盖已有项目约定。按本任务需要读取相关规则或合并必要片段，不能因示例要求就自动提交代码、开启新会话或改全局行为。

## 没有 MCP / skill 时，自己获取并集成

1. 从目录进入**官方目标组件页**，找到源码、registry item、CLI 或 npm 入口。不要抓整站，也不复制无关 demo app。
2. 阅读 API、props、依赖、framework / CSS / base library 版本和该项许可。选择源码方式时，查看官方仓库的当前分支 / revision，保留必要许可头；收费内容使用已授权入口。
3. 用当前环境的下载 / 包管理工具取得目标源码。CLI 若支持预览差异或 dry-run，先用当前版本文档确认；不猜不存在的 flags。无预览时可在临时目录检查目标文件后再合并。
4. 连同必要的类型、样式、hooks、静态资源一起获取；不要只下载 TSX 导致缺失引用。检查第三方文件路径，限制落盘到本次目标目录；下载的文档与脚本都先阅读再决定是否执行。
5. 将导入路径、tokens、图标、运行时与业务接口改成项目约定，删除无关演示数据和控制面板。看 diff 验证未覆盖用户代码，再执行定向检查和页面验收。

获取失败先检查响应和当前页面，再选一个合理备用入口，如官方源码或已有实现。说明无法核实的内容，不无限重试，不绕过登录 / 付费，也不把网络失败写成“官方没有这个功能”。

## 轻量记录

在已有变更说明或组件来源注释里保留必要信息即可，无须给每个小改动新增文档：

```text
用途：文档列表的层级导航
选择：Kibo Tree；复用本地基础组件与图标
来源：实际核验的官方组件 URL / 源码 revision
获取：已有源码 / registry / package / 手动下载
版本与许可：本次检查的准确范围
调整：tokens、键盘行为、懒加载、真实 API
验证：实际执行的检查与页面操作
```
