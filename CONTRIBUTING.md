# 贡献指南

感谢你愿意改进 DeepDig。这个项目的核心资产是**措辞**和**追问质量**，所以贡献门槛不高，但对准确性要求很高。

## 可以贡献什么

| 类型 | 例子 |
|---|---|
| 题库 | 新增一个领域的决策点（如「数据管道」「Agent 工具」「硬件项目」） |
| 示例 | 一段完整的真实追问记录，包含翻车与修正 |
| 反模式 | 你见过的糟糕提问方式，以及为什么糟糕 |
| 评级校准 | 指出某个贴合度评级标准不合理，并给出替代方案 |
| 文档 | 错别字、失效链接、表达不清 |

## 开发与校验

无需安装依赖，只需要 Python 3.8+：

```bash
git clone https://github.com/Lyajjyurot/DeepDig.git
cd DeepDig
python3 scripts/validate_skill.py
```

CI 会在每次 push / PR 时执行同样的校验。

## 写作规范

### SKILL.md

- **正文不超过 60 行**（不含 frontmatter）。超了就把细节移到 `references/`。
- 只写行为约束，不写背景故事。每一条都应该是「Agent 能照做」的指令。
- 保留以下小节：`触发`、`铁律`、`流程`、`评级诚实`、`高频异常`、`参考`。
- 不得放宽两条硬约束：**只有提示词明确提到 DeepDig 才触发**；**追问最多 8 个问题**。
- 修改措辞时优先考虑**行为锚定**：用能产生体感的词（relentlessly / bewildering / shared understanding），不用「仔细、全面、认真」这类空修饰。

### references/

- 一个文件只讲一件事，开头一句话说明用途。
- 多用表格和可直接复制的模板，少写长段落。
- 新增规则时，先问：这条规则会不会和 `SKILL.md` 的铁律冲突？冲突就不要加。

### 示例

- 必须是**完整对话**：用户输入 → 追问 → 归宿播报 → 清单 → 检索结果。
- 项目卡片里的 Star 数、活跃度若无法核实，写「未获取」或在文首注明是示意数据。**不要编造精确数字。**
- 鼓励收录「Agent 犯错后被纠正」的片段。

### 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat(question-bank): 增加数据管道类决策点
fix(skill): 修正清单状态枚举不一致
docs(examples): 补充无高贴合兜底示例
```

## PR 检查清单

- [ ] `python3 scripts/validate_skill.py` 通过
- [ ] `SKILL.md` 正文仍在 60 行以内
- [ ] 仍保持「显式提到 DeepDig 才触发」与「最多 8 问」两条硬约束
- [ ] 新增内容没有引入「一次多问」或「省略其他选项」的示范
- [ ] 所有链接可访问
- [ ] 没有编造的 Star 数、许可证或功能描述

## 行为准则

讨论对事不对人。指出问题时给出可执行的修改建议，而不是只说「这样不好」。安全问题不要开公开 Issue，请私下联系维护者。

## 发布前检查（维护者）

首次把仓库公开到 GitHub 时，逐项确认：

- [ ] 把 README、Issue 模板 `config.yml`、徽章里的 `your-org` 替换为实际组织或用户名
- [ ] 仓库描述填写：`决策树式一次一问的需求澄清 Skill，确认后检索 GitHub 相似开源项目`
- [ ] 添加 Topics：`agent-skill`、`prompt-engineering`、`requirements`、`product-discovery`、`claude-code`、`trae`
- [ ] 开启 Issues 与 Discussions，关闭 Wiki（文档都在仓库内）
- [ ] 为 `main` 分支开启保护：要求 CI 通过、至少 1 次 review
- [ ] 确认 Actions 可运行，`validate` 工作流绿灯
- [ ] 上传社交预览图（1280×640）与 LICENSE 识别（GitHub 自动识别 MIT）
- [ ] 打 tag `v1.1.0`，按语义化版本维护后续 tag