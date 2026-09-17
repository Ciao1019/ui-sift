# 可执行工具手册

四个脚本只依赖 Python 3.9+ 标准库。先定位当前 skill 目录，在该目录运行下述命令；不把示例中的缓存路径写死进业务代码。Windows 可以用 `py -3` 替换 `python3`。

工具辅助判断，不强制每次任务全部执行。一个按钮的小调整通常直接读代码即可；新工程、跨库选型或多页面验收更适合使用工具。没有 Python 时按相同资料手工完成，不让辅助工具阻断工作。

## 1. 项目扫描：profile_project.py

```bash
python3 scripts/profile_project.py /path/to/frontend-package > /tmp/frontend-profile.json
```

输出框架、包版本声明、UI / 动效 / 图标依赖、锁文件位置、部分组件文件路径、主题 token 名称与可用检查命令的**名称**。输出含本机项目绝对路径，对外分享前自行删去；扫描器不会上传结果。

只读，不联网，不执行项目脚本。跳过隐藏文件、隐藏目录、符号链接、node_modules 和常见产物目录；不读取 `.env`、锁文件内容或脚本命令字符串。registry 只输出名称，不输出带鉴权参数的地址。依赖中的 URL 引用不会原样输出。

```bash
python3 scripts/profile_project.py /path/to/project --max-files 5000
```

扫描最多 10,000 个文件、目录深度 7，最多列出 500 个组件候选路径；`--max-files` 可更改文件数上限。CSS 只扫描常见全局文件的前 262,144 字符。`scan.truncated` 表示触及文件数限制，深度及清单限制仍可能漏项。框架检测依靠清单依赖或 `.templ` 文件，不是编译器。

**结果使用边界**：有文件不等于业务已使用；有包声明不等于版本兼容；扫描到多个框架时应对目标 package 重新扫描。继续用 `rg` 检查调用点、导出、主题 Provider 和路由。

## 2. 离线组件检索：recommend.py

```bash
python3 scripts/recommend.py "日期范围筛选" --framework react
python3 scripts/recommend.py "AI 对话代码高亮" --framework auto --profile /tmp/frontend-profile.json
python3 scripts/recommend.py "文档审核，定位原文" --framework react --intent document --intent citations
python3 scripts/recommend.py "分享权限弹层" --framework react --no-new-dependencies
```

参数：

| 参数 | 含义 |
| --- | --- |
| `--framework` | react / vue / angular / svelte / go-templ / html / unknown / auto；支持 next、nextjs、nuxt、templ 别名 |
| `--profile` | 扫描器输出的 JSON；用于已有依赖偏好，`auto` 要求恰好一个框架 |
| `--intent` | 可以重复；显式指定后替代关键词推断；值见 `data/intents.json` |
| `--limit` | 返回 1–25 个候选，默认 5 |
| `--motion` | 0 静态、1 轻反馈、2 允许较强表现；默认 1；用于筛选候选的典型表现 |
| `--no-new-dependencies` | 以本地复用或实现为主，外部候选全部标为 inspiration_only |

候选附带匹配理由、文档入口、官方 skill / MCP 记录与注意事项。先过滤被明确排除的来源、框架和动效，再按意图交集、具体能力词、名称与已有相关依赖排序；`score` 是检索排序值，**不是审美、质量或兼容性评分**。`unknown` 不做框架硬过滤，只能用于早期探索。

名称匹配不会把英文 `template` 当成 `Plate`。否定识别只覆盖邻近短语，不能理解全部自然语言；复杂请求先提炼意图再用 `--intent`。例如“文章目录”可明确指定 `markdown`，但阅读器与 Toc 的最终选取仍由具体任务决定。

没有结果时正常返回空列表，表示本目录未命中。候选的 `api_verified` 固定为 false，`install_command` 固定为 null；工具不联网核对 API，也不生成安装命令。版本、许可、Radix / Base UI 和实际功能仍要查官方页。

## 3. 官方资料下载：fetch_reference.py

```bash
python3 scripts/fetch_reference.py moumen --out /tmp/moumen-llms.txt
python3 scripts/fetch_reference.py moumen \
  --url https://lab.moumen.dev/r/share-permissions-popover.md \
  --kind text --out /tmp/share-permissions-popover.md
```

`source` 使用 `data/resources.json` 的 id。省略 `--url` 时用已记录的 llms 地址；没有记录就报错，不能猜测地址。每次用新输出路径，不覆盖已有文件。

| `--kind` | 适用响应 |
| --- | --- |
| `text`（默认） | llms、Markdown、源码文本；拒绝 HTML 回退页 |
| `page` | 已确认的公共官方网页；HTML 只是原始资料，需要继续读内容 |
| `json` | JSON 索引或结构化资料 |
| `registry` | 含内联 `files[].content` 的 registry item；只缓存，不写入项目 |

仅接受该来源已记录官方域名的 HTTPS；逐跳检查重定向、拒绝显式登录跳转。最大 2 MB，网络操作超时 15 秒。检查 UTF-8、非空、内容类型和基本结构，返回原始文件、最终 URL、SHA-256 与 `downloaded_unreviewed` 状态。

这不是浏览器，也不能识别所有伪装登录页或验证网页内容的正确性。失败时读取当前官方入口，必要时用可用浏览工具；新域名或 GitHub 仓库先核实官方关联，再用常规下载工具。不要为了绕过检查随意扩充域名。

**下载后仍要完成**：读源码与许可 → 核对框架 / 依赖 / 副作用 → 选择官方安装方式或整理目标源码 → 接业务数据和事件 → 实际验证。registry 缓存不代表安装成功，skill 文件不代表宿主已加载，MCP 文档不代表连接通过。

## 4. 验收记录检查：check_delivery.py

按 [验收模板](../templates/delivery-evidence.json) 填写实际观察和证据文件，然后运行：

```bash
python3 scripts/check_delivery.py /path/to/delivery-evidence.json --evidence-root /path/to/task-output
```

报告包含来自任务的 `requirements` 和对应的 `checks`。每项检查引用要求 id，状态为 pass / fail / unverified / not-applicable；pass 必须引用真实存在、非空且位于 evidence root 内的文件。相对路径从 evidence root 解析，符号链接也不能逃出该目录。

输出状态：`invalid`（结构或证据引用错误）、`has_failures`（存在失败）、`incomplete`（有未验证项）、`evidence_record_complete`（记录齐全）。只有最后一种退出码为 0，其余为 2。模板初始为 unverified，预期输出 incomplete。

脚本不执行测试，不读取截图语义，不判定日志真假；Agent 必须核查实际证据。记录齐全不能被写成“界面验收通过”。某要求如果必需，不能通过全部标为 not-applicable 来跳过。

## 5. 数据与维护

- [resources.json](../data/resources.json)：22 个来源、框架、知识入口、未确认与访问边界；`connection_tested` 表示是否实际测过连接，目前均为 false。
- [components.json](../data/components.json)：69 组候选，名称是发现线索，可能合并多个组件；不是 69 个经过安装验证的 export 或 registry ID。
- [intents.json](../data/intents.json)：30 类中英文意图词表；保持特定需求与通用装饰分离。

候选适用性、动效等级、集成成本是本 skill 的编辑判断。新增记录时同时维护 [目录](catalog.md)、[接入指南](acquisition.md) 与路由用例；不要只改 JSON 而让文字互相矛盾。核验日期是本次资料阅读日期，不代表永久有效。

运行包内工具测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

这组测试检验脚本边界和选型不变量。Agent 是否做出优秀界面，应另用 [真实任务场景](../evals/manual-scenarios.md) 观察实际结果。
