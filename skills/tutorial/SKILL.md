---
name: tutorial
description: "Create a polished beginner tutorial with Mermaid chapter visuals, source-backed research, and DOCX/PDF/HTML exports from any topic or reference materials. Use whenever the user wants to create a tutorial, guide, or course from a topic, URL, paper, GitHub repo, or draft. Trigger on phrases like 'create a tutorial', 'write a guide about', 'make a course on', '写一个教程', '帮我做个教程', '整理成教程'. Also triggers when the user provides reference materials and asks to turn them into a structured learning resource."
---

# Tutorial

面向教程成品生产的 Skill：输入一个主题，或输入一组参考资料、网址、论文、GitHub 仓库、草稿，它会把这些信息整理成一套带来源、带大纲、带章节配图、带多格式导出的完整教程。

基于 [yao-tutorial-skill](https://github.com/yaojingang/yao-open-skills/tree/main/skills/yao-tutorial-skill) 改进，主要改动：

1. **视觉系统改用 Mermaid**：章节配图使用 Mermaid 声明式语法 + `mmdc` 编译，布局更稳定、token 消耗更低。
2. **PDF 输出改用 Kami skill**：PDF 交给 Kami 的 long-doc 模板排版，获得专业级排版效果。

## 开始之前：依赖检查

在执行任何工作之前，先检查运行环境。依次运行以下命令：

```bash
which mmdc
which pandoc
```

- 如果 `mmdc` 缺失：告知用户"需要安装 Mermaid CLI 来编译章节图表"，请求许可后运行 `npm install -g @mermaid-js/mermaid-cli`。
- 如果 `pandoc` 缺失：告知用户"需要安装 pandoc 来导出 HTML 和 Word"，请求许可后运行 `brew install pandoc`（macOS）或 `sudo apt-get install -y pandoc`（Linux）。
- 如果两个都已安装，静默跳过，直接进入下一步。

只在首次使用时需要安装，后续调用会自动跳过。

## 它会做什么

1. 把输入归一化为 `brief.json`，明确主题、受众、目标、材料、格式和限制。
2. 优先吸收用户给的资料；资料不足时，再补充官方文档、论文、GitHub、实践案例和高质量分享。
3. 生成来源登记和证据映射，避免教程变成无依据的泛泛写作。
4. 用课程设计方法重构标题和大纲，让章节既有专业体系，又能说人话。
5. 写出完整教程正文，默认中文约 `5000-10000` 字，并以正式对外成品口吻呈现。
6. 为每个编号章节编写 Mermaid 图表，编译为 SVG/PNG 后嵌入正文。
7. 导出 `Markdown`、`Word`、`HTML`（自有脚本）和 `PDF`（Kami skill）。
8. 运行验证脚本，检查章节、配图、引用、截图、导出文件和本地路径泄漏。

## 典型输出

```text
output/
├── brief.json
├── outline.md
├── tutorial.md
├── research/
│   ├── source-register.md
│   └── evidence-map.md
├── visuals/
│   ├── visual-spec.json
│   ├── index.html
│   ├── *.mmd
│   └── *.svg
├── assets/
│   └── screenshots/
└── exports/
    ├── tutorial.html
    ├── tutorial.docx
    └── tutorial.pdf
```

## 依赖

- `pandoc`：HTML 和 DOCX 导出
- `mmdc`（Mermaid CLI）：图表编译，安装方式 `npm install -g @mermaid-js/mermaid-cli`
- `python-docx`（可选）：Word 参考样式文档生成
- **Kami skill**：PDF 排版

## 关键约束

- 用户资料足够时，以用户资料为主线，不机械扩大搜索范围。
- 用户资料不足时，外部来源优先级为官方/一手来源、论文、GitHub、权威实践分享。
- 内部研究文件保留来源 ID；公开 Markdown/HTML/Word/PDF 不显示 `[U1]`、`[X1]` 这类角标。
- 教程正文必须像正式出版物，不写"基于用户资料""根据原文整理"等内部来源话术。
- 标题和大纲要面向用户利益、痛点和学习路径，避免只堆专业术语。
- 每个编号章节都必须有一个 Mermaid 图表和一张嵌入配图。
- 章节配图使用 Mermaid 声明式语法，最多 6 个主节点，8 种图表类型。
- HTML 报告使用居中内容容器、粘性目录、日期和章节跳转。
- PDF 由 Kami skill 排版，使用暖色纸感设计系统。
- Word/PDF 默认不保留页眉页脚。

## 主要文件

- [`references/input-adaptation.md`](references/input-adaptation.md): 输入资料优先级和补充研究逻辑
- [`references/research-sourcing.md`](references/research-sourcing.md): 来源选择和证据登记规则
- [`references/tutorial-outline-and-writing.md`](references/tutorial-outline-and-writing.md): 大纲与正文写作规则
- [`references/course-design-principles.md`](references/course-design-principles.md): 课程标题、大纲和内容体验设计规则
- [`references/visual-html-workflow.md`](references/visual-html-workflow.md): Mermaid 配图生成规则
- [`references/visual-board-benchmarks.md`](references/visual-board-benchmarks.md): 图表设计约束
- [`references/editorial-production.md`](references/editorial-production.md): 排版和设计系统
- [`references/export-workflow.md`](references/export-workflow.md): HTML/Word/PDF 导出规则
- [`scripts/build_visual_pack.py`](scripts/build_visual_pack.py): Mermaid 编译 + 画板生成
- [`scripts/capture_visuals.py`](scripts/capture_visuals.py): Mermaid → PNG 截图
- [`scripts/export_tutorial.py`](scripts/export_tutorial.py): HTML/Word 导出脚本
- [`scripts/validate_package.py`](scripts/validate_package.py): 输出包验证脚本
- [`templates/mermaid-config.json`](templates/mermaid-config.json): Mermaid 主题配置
