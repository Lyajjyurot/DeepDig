# DeepDig

> 写代码之前，先把话说清楚。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skill](https://img.shields.io/badge/Skill-Agent-blueviolet)](./SKILL.md)
[![CI](https://github.com/Lyajjyurot/DeepDig/actions/workflows/validate.yml/badge.svg)](https://github.com/Lyajjyurot/DeepDig/actions/workflows/validate.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

一个面向 AI Agent 的需求澄清 Skill：把「我想做一个 XXX」用**决策树式、一次一问、选项化**的方式收敛成双方确认的《需求确认清单》，确认后再自动检索 GitHub 上的相似开源项目，由你决定复用还是从零开始。

**只在用户明确提到 DeepDig 时触发**，最多追问 8 个问题。受 Matt Pocock 的 grill-me / grilling 思路启发——**先对齐，再动手**——但把开放式追问改成了低负担的选项化追问。

---

## 为什么需要它

- **需求模糊是默认状态**。「做一个记账 App」里没有范围、技术栈、数据存储和边界，直接开工等于赌运气。
- **一次抛十个问题，用户会敷衍回答**。一次一问、每题带选项，回答成本从「写一段话」降到「回一个字母」。
- **重复造轮子是常态**。需求确认后先搜一遍 GitHub，能复用就复用，不能复用也看清了差距。
- **确认前不动手**。没有确认清单，就没有实现动作——这条是硬约束。

## 适合与不适合

| 适合 | 不适合 |
|---|---|
| 需求还停留在「我想做一个 XXX」 | 需求已经明确，只差写代码 |
| 想先判断能不能复用现有开源项目 | 只想找一个现成项目直接抄 |
| 动手前需要与同伴 / 客户对齐范围 | 需要完整 PRD、排期与验收标准 |
| 愿意花 5~8 轮回答换取一份确认清单 | 希望 Agent 边问边写代码 |

## 它怎么工作

```text
用户明确提到 DeepDig + 模糊需求
  ↓
事实自查：代码 / 文档 / 配置能查到的，不提问
  ↓
建树 → 一次一问（最多 8 问，3~5 个选项 + 推荐 + 其他）
  ↓
每个决策点落到三态：DECIDED / RABBIT HOLE (v2) / NO-GO
  ↓
所有可达分支都有归宿？
  ├─ 否 → 未到 8 问继续问；已到 8 问强制收口
  └─ 是 → 输出《需求确认清单》
             ↓
         用户确认？
           ├─ 否 → 回到追问
           └─ 是 → 检索 GitHub 相似项目
                      ↓
                  项目卡片 + 贴合度（高 / 中 / 低）
                      ↓
                  有高贴合？
                    ├─ 是 → 询问：复用哪个 / 从零开始
                    └─ 否 → 未找到高贴合项目 + 差距说明 → 进入方案设计
```

## 核心规则

| 规则 | 说明 |
|---|---|
| 显式触发 | 只有提示词中明确提到 DeepDig 才启用，模糊需求本身不触发 |
| 一次一问 | 每轮只问一个问题，等回答再继续 |
| 最多 8 问 | 到第 8 问必须收口，未决点转为 RABBIT HOLE 或建议拆分 |
| 选项化 | 3~5 个选项，最多一个【推荐】，最后一项永远是「其他（请说明）」 |
| 事实不问 | 能从仓库、文件、配置、文档查到的，自己查 |
| 三态归宿 | 每个决策点必须落到 DECIDED / RABBIT HOLE / NO-GO |
| 确认前不动手 | 用户确认清单之前不搜索、不设计、不写代码 |
| 评级诚实 | 贴合度宁缺毋滥，不拔高中/低评级 |

## 安装

DeepDig 遵循 Agent Skills 开放标准：**把整个 `DeepDig` 文件夹放进 Agent 的 skills 目录，确保 `SKILL.md` 位于该文件夹根部即可。**

### 各 Agent 的技能目录

| Agent / IDE | 项目级目录 | 用户级目录（全局） | 备注 |
|---|---|---|---|
| Trae | `.trae/skills/DeepDig/` | `~/.trae-cn/skills/DeepDig/` | 项目技能需要把目录设为可信 |
| Claude Code | `.claude/skills/DeepDig/` | `~/.claude/skills/DeepDig/` | 可直接用 `/DeepDig` 调用 |
| Codex CLI / IDE | `.agents/skills/DeepDig/` | `~/.agents/skills/DeepDig/` | 输入 `/skills` 或 `$` 选择技能 |
| Cursor | `.cursor/skills/DeepDig/` | `~/.cursor/skills/DeepDig/` | 目前需 nightly 渠道；也兼容 `.claude/skills/` |
| VS Code + GitHub Copilot | `.github/skills/DeepDig/` | `~/.copilot/skills/DeepDig/` | 也读 `.claude/skills/` 与 `.agents/skills/` |

### 命令行安装

```bash
git clone https://github.com/Lyajjyurot/DeepDig.git

# Claude Code
mkdir -p ~/.claude/skills && cp -r DeepDig ~/.claude/skills/

# Codex
mkdir -p ~/.agents/skills && cp -r DeepDig ~/.agents/skills/

# Cursor
mkdir -p ~/.cursor/skills && cp -r DeepDig ~/.cursor/skills/

# VS Code + Copilot
mkdir -p ~/.copilot/skills && cp -r DeepDig ~/.copilot/skills/

# Trae 国内版
mkdir -p ~/.trae-cn/skills && cp -r DeepDig ~/.trae-cn/skills/
```

**Windows PowerShell**

```powershell
git clone https://github.com/Lyajjyurot/DeepDig.git

# 以 Claude Code 为例，其他 Agent 换成上表对应路径
$target = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force DeepDig $target
```

**项目级安装**

把 `DeepDig` 复制进仓库内的 `.trae/skills/`、`.claude/skills/`、`.agents/skills/`、`.cursor/skills/` 或 `.github/skills/`，团队共享同一份技能。

**其他 Agent**

若所用 Agent 还不支持 `SKILL.md`：先把 [SKILL.md](./SKILL.md) 作为项目规则或自定义指令导入，并保留 `references/` 与 `examples/` 供其按需读取；等它支持 Agent Skills 后，再按上表迁移。

**安装检查**

- skills 目录下有一层 `DeepDig/`，里面直接是 `SKILL.md`；
- 重启或重载 Agent 后，技能列表中能看到 DeepDig；
- 显式输入 `/DeepDig`（Codex 输入 `/skills` 或 `$`）能命中。

> 兼容性：Claude Code 等平台要求 frontmatter 的 `name` 只含小写字母、数字和连字符。若技能未被识别，把 `name` 改成 `deepdig`、安装目录也改为 `deepdig` 即可，触发词与行为不变。

## 使用

**必须显式点名 DeepDig**，否则不会触发：

```text
/DeepDig 我想做一个给独立开发者用的发布清单工具
```

也可以说：

- 「用 DeepDig 帮我把这个需求问清楚」
- 「DeepDig：我想做一个 XXX」
- 「先别写代码，用 DeepDig 跟我对齐需求」

只说「我想做一个 XXX」不会触发；即使需求很模糊，Agent 也不会自动接管。

Agent 会开始一次一问的追问（最多 8 个问题），最后给出《需求确认清单》，确认后再检索开源项目。

## 示例

| 示例 | 演示内容 |
|---|---|
| [从「书签管理器」到复用决策](./examples/01-greenfield-bookmark-manager.md) | 完整 6 轮追问 → 清单 → 3 张项目卡片 → 推荐复用 |
| [无高贴合项目时的诚实兜底](./examples/02-no-high-fit.md) | 需求收敛 → 诚实评「低」→ 输出「未找到贴合度足够高的开源项目」 |

## 目录结构

```
DeepDig/
├── SKILL.md                        # 主入口：触发条件、行为铁律与流程（正文 < 60 行）
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── references/
│   ├── decision-tree.md            # 建树、遍历、收敛、规模自检、反模式
│   ├── question-bank.md            # 七类决策点题库
│   ├── github-search.md            # 关键词、筛选、评级量表、兜底
│   └── templates.md                # 话术 / 清单 / 卡片模板
├── examples/
│   ├── 01-greenfield-bookmark-manager.md
│   └── 02-no-high-fit.md
├── scripts/
│   └── validate_skill.py           # 结构、规则、仓库文件与相对链接校验
└── .github/
    ├── workflows/validate.yml      # CI：每次提交自动校验
    └── ISSUE_TEMPLATE/             # Bug / 功能建议表单
```

## 设计原则

1. **正文极简，细则外置**。`SKILL.md` 只保留行为锚点，细节放进 `references/`，Agent 按需读取，避免上下文被规则淹没。
2. **措辞即行为**。用「毫不留情地（relentlessly）追问」「一次多个问题会让用户困惑（bewildering）」这类带体感的措辞，而不是「请仔细、全面地询问」。
3. **可自检的完成标准**。收口条件是「双方达成共享理解（shared understanding）」，而不是「问题问完了」。
4. **诚实优于成果感**。宁可报告「没有高贴合项目」，也不把低贴合包装成可复用。

## 校验

```bash
python3 scripts/validate_skill.py
```

检查项：

- frontmatter 完整性、`SKILL.md` 正文行数、必备章节；
- `references/`、`examples/` 的引用与占位符；
- 示例中的问题数是否超过 8 问、是否都带「其他（请说明）」；
- 开源所需文件是否齐全（README / LICENSE / CONTRIBUTING / Issue 模板 / CI）；
- README 与贡献指南中的相对链接是否有效。

## 常见问题

**会自动触发吗？**
不会。只有提示词里明确出现 DeepDig 才启用，模糊需求本身不触发。

**最多 8 问不够用怎么办？**
拆成多个子目标，各自跑一遍；非关键未决点标为 RABBIT HOLE 并写明风险。8 问是硬上限，不因「看起来还差一点」而放宽。

**确认清单之后它会替我把项目写完吗？**
不会。它负责澄清需求与判断是否复用开源项目；实现阶段由你或后续流程接手。确认前不搜索、不设计、不写代码。

**支持哪些 Agent？**
遵循 Agent Skills 开放标准的都支持：Trae、Claude Code、Codex、Cursor、VS Code + GitHub Copilot 等，目录见[安装](#安装)。不支持该标准的 Agent，可先把 `SKILL.md` 作为项目规则导入。

**能不能直接搬它的题库到别处？**
可以，MIT 许可证；保留版权声明即可。


## 许可证

[MIT](./LICENSE) © 2026 DeepDig contributors
