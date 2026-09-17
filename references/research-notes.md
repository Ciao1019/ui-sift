# 资料依据与维护范围

调研日期：2026-09-17。资源目录覆盖 22 个精选官方入口，依据公开文档与组件说明整理。设计建议是面向“简洁、交互优美”的选型判断，不是组件流行度排名，也不是对所有候选的质量认证。

## 参考了哪些常见 skill 写法

在 [skills.sh](https://skills.sh/) 的公开榜单核实了以下前端相关 skills 的可见度，并阅读其官方源码。榜单会变，不固定引用安装数量或排名。

| 参考 | 采用的写法 | 如何适配这里 |
| --- | --- | --- |
| [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 先确定产品内容与视觉意图，再实现并做减法 | 明确“简洁交互”的取向，保留用户品牌与现有系统，不要求每个页面追求强烈视觉实验 |
| [Vercel web-design-guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) | 短入口，按需读取最新权威资料 | 接入信息放到独立参考文件；采用前核对当前文档，不在主 skill 堆积 API |
| [Vercel react-best-practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) | 按影响组织规则与细分资料 | 优先框架兼容、信息结构、真实状态与包体积，不把每条性能规则都复制进来 |
| [Tool UI 官方 Agent Skills 文档](https://www.tool-ui.com/docs/agent-skills) | 兼容检查、发现、安装、接线、验证 | 组件获取必须继续到真实业务接线，不能以复制 demo 作为完成 |

本包用自己的文字编写规则，未打包上述 skills 的完整内容或第三方组件源码。第三方组件、模板、脚本与媒体的授权仍按各来源执行。

## 参考 Vibe-Skills 的组织方式

同时研究了 [Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills)。本次读取的 revision 为 [`ddcaa2affca93c1efe026d008b6b93709e5fb7e2`](https://github.com/foryourhealth111-pixel/Vibe-Skills/tree/ddcaa2affca93c1efe026d008b6b93709e5fb7e2)。阅读其中文 README、根 SKILL、review protocol、current-routing-contract 与本地安装 skill 路由测试。

它的范围是通用技能编排与受治理的执行系统；目录规模同时来自大量捆绑能力，不能拿文件数直接衡量前端效果。本包的借鉴具体落在以下位置：

| 借鉴点 | UI Sift 的对应能力 |
| --- | --- |
| 分层入口与按需读取 | 主 skill 按任务规模路由到设计、集成、验收模块 |
| 候选发现与最终选择分开 | 离线检索只提供候选；框架、版本、许可和业务契约仍需核对 |
| 任务有实际执行结果 | 从简报到主流程、状态、响应式和视觉检查，不以下载结束任务 |
| 通过证据判断完成 | 验收要求与检查关联；完整记录、实际产品验收分别表述 |
| 用案例检验行为 | 工具回归用例 + 独立列出的真实 Agent 任务场景 |

没有复制其代码、协议文本或捆绑技能；没有引入通用全局运行时、强制多 Agent 调度或普遍的人工审批状态机。此处复杂度来自组件获取、项目适配和验证的具体需要。Vibe-Skills 自述的版本、测试与性能数字不适用于本包，也没有用它们为本包效果背书。

## 本次核实的关键变化

- Astryx 有远程 MCP 和 CLI 生成的 agent docs；当前安装文档要求 React 19+，并说明 CSS cascade layers。
- shadcn-templ 是 Go templ + vanilla JavaScript；不能归入 React 安装方案。
- assistant-ui 原高亮地址跳转到 Elements；当前 Syntax Highlighter 是 Prism 路线，Shiki 为另一个选项。
- Extend 新 registry 按 `{style}` 区分底层；旧地址可能向 Radix 项目提供 Base UI 组件。
- mindmapcn 当前官方索引强调展示优先，安装地址使用 `mindmapcn.mind-elixir.com`。
- Cuicui 官网提示新的维护方向；Libraries.dev 的完整参数 skills 涉及 Pro。
- DayFlow、Ruixen、Shadcn Studio 都需区分公共能力与 Pro 内容，不能统一描述成免费源码。
- Variant 社区跳转登录页，未核实内部作品和源码能力。

证据链接放在 [资源目录](catalog.md) 与 [接入指南](acquisition.md) 对应条目，避免另维护一份重复 URL 清单。

## 核验的限度

读取了官方页面、可用的 llms 索引和部分源码说明；浏览检查了 GodUI Segmented Control、moumenlab Share & Permissions Popover 等代表性页面。没有逐一安装所有库、连接所有 MCP、执行官方 skills 脚本或对所有示例做跨设备测试。

部分网页加载超时后使用官方文档文本继续核验。404、登录跳转和未确认的 skill / MCP 都按各自证据标注，没有将它们当成“不支持”。

## 后续维护

有任务要采用某个来源时更新该条目即可，无须每次重新扫全库。出现域名迁移、框架 / base library 变化、MCP / skill 新入口或授权范围变化时，同步修改目录与接入指南并更新核验日期。

增加新资源必须说明：最适合什么任务、具体值得看的组件、与现有来源的差异、框架边界、可验证入口。删除来源时同步修复主 skill 中的选型指引。

更新时还需同步 `data/resources.json`、`data/components.json` 和受影响的意图 / 回归用例。数据是离线发现索引，不得把未经当前核对的 API 或安装命令升级为已验证状态。

## 1.0 验证范围

验证日期：2026-09-17。以下针对本 skill 的文档、离线数据与可独立运行的工具。

| 检查 | 实际结果与范围 |
| --- | --- |
| skill-creator 的 quick_validate | 通过；验证 skill 元数据与基本结构 |
| 标准库 unittest | 28 个测试方法通过；包含 18 个路由场景、下载异常、项目扫描及证据引用边界 |
| JSON / Python / 本地链接 | JSON 可解析、Python 语法可解析、相对链接目标存在；22 个来源均有组件候选 |
| 通用场景检索 | 独立测试覆盖 React 日期选择、Vue / Nuxt 命令面板、Go templ 表单、只读 Markdown、多框架歧义与未命中场景 |
| 真实官方文本下载 | 获取 [Share & Permissions Popover](https://lab.moumen.dev/r/share-permissions-popover.md)，32,389 字节，UTF-8 文本，未执行其中代码 |

该下载响应的 SHA-256：`952eaba0313933e6e366a5a099a2859dc68e5644ee35c575adb2dc438809e944`。官网更新后内容与 hash 可以变化，不作为永久固定版本。

分享包只含通用文档、索引、脚本、模板与独立测试；不包含业务工程画像、运行日志或下载的第三方源码。没有连接全部 MCP、逐一安装组件或完成 7 个真实 Agent 页面实现评估；也没有把脚本通过率描述为审美提升指标。
