# 精选资源目录

核验日期：2026-09-17。按场景查找，不要一次加载所有官网。以下覆盖原始清单的全部 22 个来源；组件名称是定位词，实际安装 ID、API、依赖与许可须在采用时从官方文档确认。

“优先挑选”是面向简洁交互的编辑判断；“值得探索”表示官网展示的额外候选，并不表示已完成生产验证。接入状态统一查 [官方接入与下载](acquisition.md)，组合与取舍查 [集成模式](integration-patterns.md)。

需要按需求检索时，使用 [工具手册](tooling.md) 的 `recommend.py`。离线 [组件数据](../data/components.json) 收录 69 组发现线索，以 30 类意图检索；它不替代下面的取舍说明，也不提供未经核实的安装 ID。

## AI 与富内容

### 1. Tool UI

- [官网与组件目录](https://www.tool-ui.com/docs/overview) · React / shadcn，面向结构化 tool output。
- **优先挑选**：Citation、Data Table、Plan、Progress Tracker、Approval Card。把引用、结果、阶段和待确认操作变成清晰的独立信息单元。
- **值得探索**：Option List、Question Flow、Parameter Slider、Preferences Panel、Code Diff，适合在对话内完成选择、补充参数与审查。
- **取舍**：它解决工具结果呈现，不替代完整聊天 runtime。先确定 schema、action 回调和 receipt；展示漂亮但操作不回传不算接入完成。

### 2. assistant-ui

- [原始高亮入口](https://www.assistant-ui.com/docs/ui/syntax-highlighting) · React 对话 runtime、原语与 Elements。
- **优先挑选**：Thread / Composer、Markdown Text、Syntax Highlighter 或 Shiki Highlighter；已有对话链中局部增强。
- **值得探索**：Tool Timeline、Agent Plan、Job Progress、Context Display、Reviewable Diff、Scroll Anchor，可把等待与工具使用变得可理解。
- **取舍**：原高亮 URL 本次跳转至 [Syntax Highlighter](https://www.assistant-ui.com/elements/syntax-highlighter)，当前该组件使用 Prism / `react-syntax-highlighter`。Shiki 是另一个选项；不要从旧教程推断当前 API，也不要两套都装。

### 3. prompt-kit

- [官网](https://www.prompt-kit.com/) · React AI 界面的可组合构件。
- **优先挑选**：Prompt Input、Message、Chat Container、Scroll Button、Source，用于轻量聊天和输入体验。
- **值得探索**：Prompt Suggestion、Feedback Bar、File Upload、Steps、Thinking Bar。
- **取舍**：先确认项目是否已用 assistant-ui。已有完整 runtime 时只补需要的视觉能力；不能为了输入框同时建立第二套消息状态。

### 4. Lobe UI Markdown

- [Markdown 文档](https://ui.lobehub.com/components/markdown) · React 富内容展示。
- **优先挑选**：Markdown 的排版、GFM 表格、数学表达、代码和自定义引用。
- **值得探索**：同站的 CodeDiff、Toc、Mermaid、Snippet，适合阅读和知识产品；按具体需求查看，不整套引入。
- **取舍**：先评估主题和包体积。只读内容与编辑器职责分开；流式渲染、HTML / 媒体和插件需要核对当前版本，保持内容处理边界。

### 5. Plate

- [官网](https://platejs.org/) · React 富文本编辑器与插件体系。
- **优先挑选**：Editor、Floating Toolbar、Slash Command、Table、Mention，形成完整的编辑流程。
- **值得探索**：Comments / Discussion、Suggestion、TOC、Block Selection、Markdown Streaming、版本历史示例。
- **取舍**：按能力装 feature kit / plugin；只读页面不为一个代码块加载完整编辑器。插件、UI 和核心版本要匹配，编辑器外观不能代替文档数据模型。

## 业务工作台与内容结构

### 6. Astryx

- [组件目录](https://astryx.atmeta.com/components) · React 设计系统，当前官方安装文档要求 React 19+，有独立主题与布局能力。
- **优先挑选**：Table、Token、Metadata List、Empty State、Stack，适合信息密集但安静的应用界面。
- **值得探索**：Power Search、Tree List、Command Palette、App Shell、Bottom Sheet；复杂后台可比较其完整布局能力。
- **取舍**：综合设计系统的主题成本高于小型 copy-paste 组件。先查全局 CSS、Provider 和项目现有 tokens；几个徽标不一定值得引入主题系统。

### 7. Extend UI

- [文档](https://www.extend.ai/ui/docs) · React 文档处理与人工审核界面。
- **优先挑选**：PDF / DOCX / Excel Viewer、Bounding Box Citations、Layout Blocks、File Thumbnail。
- **值得探索**：Schema Builder、Document Splits、File System (Finder)、E-Signature；真正需要编辑时评估 PDF Editor。
- **取舍**：官网当前把 DOCX Editor 和 Excel Editor 标为实验性。先确认文件格式、引擎与加载成本；普通上传直接复用项目上传组件。采用 style-aware registry，见接入指南。

### 8. Kibo UI

- [官网](https://www.kibo-ui.com/) · 可组合的 React / shadcn 扩展。
- **优先挑选**：[Tree](https://www.kibo-ui.com/components/tree)、[Table](https://www.kibo-ui.com/components/table)、Dropzone、Image Zoom，补足业务基础能力。
- **值得探索**：[Gantt](https://www.kibo-ui.com/components/gantt)、[Kanban](https://www.kibo-ui.com/components/kanban)、Color Picker、Code Block、Roadmap 组合。
- **取舍**：适合复杂应用组件，不能仅因有 Gantt 就把普通列表改成项目管理台。代码高亮、日期与拖拽依赖先与现有实现去重。

### 9. mindmapcn

- [原始官网](https://mindmapcn.vercel.app/) · [当前知识索引](https://mindmapcn.mind-elixir.com/llms.txt) · React + Mind Elixir + Tailwind / shadcn 风格。
- **优先挑选**：MindMap、MindMapControls；展示优先，适合组织结构、知识树、项目规划和只读决策树。
- **值得探索**：缩放适配、导出、紧凑布局、纯文本大纲输入；需要画布内编辑时再开启交互。
- **取舍**：它不是自带完整撤销工具栏与属性检查器的编辑产品。容器必须有明确高度；静态简单结构可沿用已有图表，不必增加画布运行时。

## 输入与时间

### 10. shadcn/ui Calendar

- [Calendar](https://ui.shadcn.com/docs/components/calendar) · React 日期与范围选择，当前文档提供不同基础组件变体。
- **优先挑选**：单日期、范围、月份年份下拉、预设范围；接入现有 Popover / Field。
- **值得探索**：时区处理、日期限制、窄屏单月与桌面多月。
- **取舍**：本次入口跳到 Base UI 版本，不代表旧项目应切换 Base UI。对齐项目原有 base / radix / aria 和 DayPicker 版本。它不是日程排班器。

### 11. DayFlow

- [官网](https://calendar.dayflow.studio/) · 提供 React、Vue、Angular、Svelte 日历接入。
- **优先挑选**：日 / 周 / 月 / 年 / Agenda、事件编辑、拖拽调整、日程搜索。
- **值得探索**：资源时间线、资源网格、打印与预约流程；官网将相关高级能力放在 Pro 介绍中，须逐项核对。
- **取舍**：不要为一个日期字段引入完整排程库。业务规则仍由应用负责；时区、跨日、资源冲突、撤销与持久化需要单独设计。

### 12. Cuicui Signature

- [签名组件](https://cuicui.day/application-ui/signature) · React copy-paste 组件与交互实验。
- **优先挑选**：React Signature 的书写、清空、验证流程。
- **值得探索**：已有项目中的 Modern Book Cover、轻纹理、Smooth Hover 导航可作为内容相关的细节；采用前重新找对应官网源码。
- **取舍**：官网当前提示作者维护方向转向 Control UI。不要据此擅自替换用户选型，但应检查维护与依赖。签名画布须验证触摸及空值，不能把它等同于完整签署服务。

## 微交互与动效

### 13. moumenlab

- [Component Lab](https://lab.moumen.dev/components) · React + Tailwind + `motion/react`；每个实验有演示、blueprint 和源码。
- **优先挑选**：File Upload Staging Area、Share & Permissions Popover、Command Palette with Argument Chips，效果直接服务实际流程。
- **值得探索**：OTP Segmented Input、Caret-Anchored Mention Popover、Drag-to-Reorder List、Search-Expand Navigation Bar、Inertial Wheel List。
- **取舍**：读交互机制再复制。演示里的上传、权限或支付不自动成为业务能力；保留键盘、取消、连续操作与恢复状态。

### 14. GodUI

- [组件目录](https://godui.design/docs/components) · React 动效组件与 motion guidelines。
- **优先挑选**：Segmented Control、Filter Bar、Command Palette、Floating Toolbar、Highlighter，适合少量精细增强。
- **值得探索**：Morphing Dialog、Reorder List、Agent Timeline、Presence Facepile、Progress Fold Button。
- **取舍**：背景、液态、光效与磁吸类只在任务和品牌需要时使用；长按确认不能成为无法替代的唯一操作方式。对照其 Motion Principles 判断动画是否有意义。

### 15. UI TripleD

- [官网](https://ui.tripled.work/) · React / Motion；组件提供 shadcn/ui、Base UI 等变体，索引还列有 Carbon。
- **优先挑选**：Native Nested List、Tabs、Hover Card、Tooltip，适合有细微反馈的内容管理。
- **值得探索**：Detail Task Card、Accessible Image Slider Card、Avatar Expand、Native User Card、AI Chat Interface。
- **取舍**：这是复制源码 / registry 模式，不是一个名为网站名称的通用 npm 包。组件后缀表达所用体系；别把 shadcnui、baseui、carbon 混装。官网使用的 Next.js 版本不等于所有组件必须依赖 Next.js，逐个检查。

### 16. Libraries.dev Beam

- [Border Beam](https://libraries.dev/beam) · React 的局部边框活动效果；同站提供其他独立效果库。
- **优先挑选**：正在生成的输入区、活动任务卡片的短时 Border Beam；配合可读状态。
- **值得探索**：Thinking Orbs 用于活动等待；Gooey、Metal、Image generation loader 只用于确实需要更强表现的场景。
- **取舍**：停止任务就停止效果，保持低强度和静态降级。官网当前把更深入的参数 skills 放在 Pro；公共组件和 Pro 预设 / Studio 授权边界不同。

### 17. Heroicons Animated

- [官网](https://www.heroicons-animated.com/) · React 18 / 19 + Motion，基于 Heroicons。
- **优先挑选**：与动作相符的复制、检查、下载、展开图标，按交互触发短动画。
- **值得探索**：通知、收藏、刷新等明确状态的图标；先在官方逐图标页看实际效果。
- **取舍**：优先保留现有图标体系。不要为一个动画图标更换整站图标；校验 focus、触摸、aria-label 与 reduced motion，不只检查 hover。

### 18. nxui

- [文档](https://nxui.geoql.in/docs) · Vue / Nuxt 动效候选，具体实现与运行时按组件确认。
- **优先挑选**：Command Menu、Animated TOC、Drag Reorder List、Stepper、Signature 等服务任务的组件。
- **值得探索**：Line Sidebar、Curved Drawer、Notification Center、Count Up；视觉实验可看 Border Beam、Spotlight Card。
- **取舍**：大量背景和 shader 不适合作为普通业务默认样式。React 项目先选原生兼容来源；这里只借鉴效果，不直接复制 Vue 实现。

## 页面系统与方向探索

### 19. shadcn-templ

- [官网](https://shadcn-templ.com/) · **Go templ + vanilla JavaScript**，原 templUI；本次官网为 2.0 beta 文档。
- **优先挑选**：Go templ 项目的 Button、Field、Dialog、Table、Sidebar 等统一基础构件。
- **值得探索**：Blocks、Charts、Typeset、Create，用于同栈页面系统。
- **取舍**：不能作为 React / Next.js 的安装起点。React 项目通常使用原版 shadcn/ui；可以借鉴信息布局，但不照搬 templ 代码和 CLI。

### 20. Ruixen UI

- [官网](https://ruixen.com/) · React / shadcn 营销 sections 与交互组件；当前提供 Tailwind v3 / v4、Radix / Base UI 变体。
- **优先挑选**：Structured Hero、Split Feature Showcase、Navbar Simple、Pricing Comparison、Wordmark Footer，挑与产品叙事对应的段落。
- **值得探索**：Comment Thread、Breadcrumb Dropdown、Password Field、Progressive Flux Loader。
- **取舍**：免费目录与 Pro 模板分开核验。音效与物理动效按产品场景取舍，默认不把营销页的持续动效带入日常工作台。

### 21. Shadcn Studio

- [官网](https://shadcnstudio.com/) · React / shadcn 组件、blocks、页面模板与主题工具。
- **优先挑选**：Application / Dashboard Shell、Data Table、Multi Step Form、Sidebar，先确定页面骨架再补局部。
- **值得探索**：营销区块、状态组件、统计与图表组合、主题生成器。
- **取舍**：有免费和 Pro 内容，也有 MCP 登录 / API key 等接入条件；逐项核对。按当前官方支持选择客户端，不把 Studio MCP 与 shadcn 官方 MCP 当作同一服务。

### 22. Variant Community

- [社区入口](https://variant.com/community) · 页面方向探索来源，不是本地组件运行时。
- **优先挑选**：当方向不明确时比较信息层级、密度、排版、内容组织与交互节奏。
- **值得探索**：同一产品任务的不同布局，而不是搜到一个漂亮页面就全盘复制。
- **取舍**：本次访问跳转登录页，未核实社区内部具体作品、导出能力或源码许可。可用已授权参考继续工作；不要编造其 MCP / skill / 安装包，也不要把参考截图描述成可自由复制的组件。
