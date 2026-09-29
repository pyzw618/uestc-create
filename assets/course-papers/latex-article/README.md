# 文章式课程报告模板（latex-article）

uestc-create 第二套 LaTeX 课程报告模板：**ctexart 文章式**——`\section` 制、12pt、1.5 倍行距、GB/T 7714-2015 **著者-出版年**引用（正文引用呈 `(作者, 年份)` 形式）。

与上一级 `../latex/`（thesis-uestc 仿学位论文章节制）互补，二选一：

| | 本套（latex-article） | `../latex/`（thesis-uestc） |
|---|---|---|
| 体例 | 文章式：引言/方法/实验/总结 | 章节制：第一章…，仿学位论文 |
| 适用 | 普通课程论文、小论文、课程报告 | 正式大报告、结题报告 |
| 引用 | GB/T 7714 著者-出版年 | 顺序编码 `[1]` |
| 底版 | ctexart 12pt、1.5 倍行距 | thesis-uestc.cls |

选型规则见 `workflows/course-papers.md` 第 0 步：按篇幅给建议并请用户确认，老师模板永远优先。

## 结构

```
latex-article/
├── main.tex                        ← 骨架主文档（封面字段与正文均为占位）
├── Reference.bib                   ← 占位文献库（三种常用条目类型各一条）
├── gbt-7714-2015-author-year.bst   ← GB/T 7714-2015 国标样式（gbt7714 宏包，许可见其上游）
└── images/
    └── UESTC-Logo.pdf              ← 封面校徽
```

> 来源说明：骨架取自一套实际课程报告的版式（ctexart + titletoc 点线目录 + titlepage 封面），
> 封面字段与正文全部替换为占位文字；原报告含个人信息，未随包分发。

## 编译方法

### 命令行（在本目录下执行）

只改正文、不动参考文献时，跑两遍即可（第二遍生成目录与交叉引用）：

```bat
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

改动 `Reference.bib` 后，需要完整四步：

```bat
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

也可以用 `latexmk -xelatex main.tex` 一步到位（会自动调度 bibtex）。

### VS Code

1. 安装扩展 **LaTeX Workshop**；
2. 打开本文件夹，按 `Ctrl+Alt+B`；
3. 工具配方选 **XeLaTeX**；需要完整编译时选 xelatex → bibtex → xelatex ×2。

## 关键配置点（学习要点）

1. **中文支持**：`\documentclass[UTF8,a4paper,12pt]{ctexart}`，文件一律存成 UTF-8。
2. **图片路径**：导言区 `\graphicspath{{images/}}`，正文里只写文件名，
   如 `\includegraphics[width=0.85\textwidth]{train_loss.png}`——所有图片放进
   `images/` 即可，不必改正文。
3. **页面设置**：`geometry` 调页边距（本模板左右 2.5cm、上下 2.8cm），
   `setspace` 的 `\onehalfspacing` 调 1.5 倍行距。
4. **目录样式**：`titletoc` + `\titlecontents` 自定义目录项（点线、页码对齐）。
5. **章节标题**：`titlesec` 可进一步自定义 `\section` 格式（骨架未额外改动）。
6. **参考文献国标**：
   ```latex
   \bibliographystyle{gbt-7714-2015-author-year}
   \bibliography{Reference}
   ```
   引用时用 `\cite{键名}`，键名在 `Reference.bib` 里查。
7. **超链接**：`hyperref` 配 `colorlinks`，目录、引用可点击跳转。

## 注意事项

- 新增图片请放进 `images/`，文件名建议用英文或数字开头，避免空格。
- 删除 `.aux/.log/.toc/.out/.bbl` 等中间文件不影响结果，重新编译会自动生成。
- 交付给老师前：封面占位字段（XX学院/XX课程/张三/20XX）必须全部替换为真实信息；
  正文占位段全部重写；示例图/表删除或替换。
