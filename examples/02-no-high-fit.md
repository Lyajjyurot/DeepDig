# 示例二：无高贴合项目时的诚实兜底

> 示例中的 Star 数、活跃度为写作时的大致示意，实际执行请以检索当时的数据为准。

## 用户

`/DeepDig 我想做一个给幼儿园老师用的课堂随机分组工具`

## Agent

**Q1：老师在什么设备、什么网络环境下用它？**

A. 教室电脑，有网络
B. 老师自己的手机，有网络
C. 教室里的老旧 iPad，网络不稳定，需要离线可用 【推荐】—— 你提到「课堂」，断网是常态风险
D. 其他（请说明）

## 用户

C

## Agent

✅ DECIDED：运行环境 → 老旧 iPad，需离线。

**Q2：一次分组的对象规模大概是？**

A. 一个班 20~35 人
B. 一个年级 100 人以上
C. 不定，两者都要
D. 其他（请说明）

## 用户

A

## Agent

✅ DECIDED：规模 → 单班 20~35 人。

**Q3：除了随机分组，还需要什么？**

A. 只要分组结果，列在屏幕上
B. 分组结果能导出成 A4 打印，贴在教室里 【推荐】—— 符合课堂使用习惯
C. 要记录历史分组，避免同一批孩子总被分到一起
D. 其他（请说明）

## 用户

B、C

## Agent

✅ DECIDED：输出 → A4 打印导出 + 历史记录。
✅ DECIDED：数据 → 本地保存分组历史（离线）。

**Q4：老 iPad 上的浏览器版本较旧，是否接受为此降低技术要求？**

A. 接受，能跑就行 【推荐】—— 设备是硬约束
B. 不接受，希望顺便换新设备
C. 其他（请说明）

## 用户

A

## Agent

✅ DECIDED：兼容性 → 优先保证旧 Safari 可用，功能可裁剪。

## 需求确认清单

| # | 决策点 | 结论 | 状态 |
|---|--------|------|------|
| 1 | 运行环境 | 老旧 iPad，离线可用 | DECIDED |
| 2 | 班级规模 | 单班 20~35 人 | DECIDED |
| 3 | 结果输出 | 屏幕展示 + A4 打印导出 | DECIDED |
| 4 | 历史记录 | 记录历史分组，降低重复 | DECIDED |
| 5 | 兼容性 | 优先兼容旧版 Safari | DECIDED |
| 6 | 账号与云同步 | 不做 | DECIDED |

> 以上需求是否确认？确认后我将搜索相似开源项目并询问是否复用。

## 用户

确认

## Agent

检索关键词：`random group generator classroom offline`、`student grouping tool printable`、`课堂随机分组 工具 打印`。

检索结果（按贴合度排序）：

**Random Group Generator（示例项目 A）** https://github.com/example/random-group-generator
Star：~400｜语言：JavaScript｜许可证：MIT
核心功能：网页端把名单随机拆成若干组。
贴合点：✅ 核心算法符合；✅ 浏览器运行
差异点：需要联网加载名单；无打印排版；无历史记录；长期未更新，未验证旧 Safari
贴合度：**低**

**Team Shuffler（示例项目 B）** https://github.com/example/team-shuffler
Star：~1.2k｜语言：TypeScript｜许可证：MIT
核心功能：团队随机分组，支持导入 CSV。
贴合点：✅ 分组算法；✅ 名单导入
差异点：面向企业工作坊，界面与文案不适配课堂；依赖现代框架，旧 iPad 风险高；无打印导出
贴合度：**低**

**未找到贴合度足够高的开源项目。**

最接近的是 **Team Shuffler**，差距在于：它没有 A4 打印导出与历史去重，而且技术栈对旧版 Safari 不友好——这两点恰好是你清单里的核心决策。

建议继续检索的关键词：`classroom grouping offline pwa`、`printable group maker`（https://github.com/search?q=classroom+grouping+offline+pwa&type=repositories&s=stars）

现有项目都不值得复用。我的实现方案建议：

- 纯静态单页应用（无构建或极轻构建），数据存 `localStorage`，保证离线与旧浏览器兼容；
- 分组算法用 Fisher–Yates 洗牌 + 冲突规避（参考历史记录）；
- 打印用 `@media print` 的 A4 版式，不需要额外 PDF 库；
- 用可控的旧版 Safari 实测，而不是只看 Can I Use。

需要我按这个方案继续设计吗？
