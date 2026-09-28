# assets/lab-report

| 文件 | 用途 |
|---|---|
| 标准实验报告.docx | 官方《标准实验报告.doc》的 docx 转换版（原样保真，作填充底版首选） |
| 标准实验报告骨架.docx | 程序填充占位符版（python-docx 构建，版式参数同 format.md） |
| layout_params.json | 官方模板解析产物（页面/样式/段落规格） |

## 骨架版占位符约定

- 封面：`{{school}}` `{{course_name}}` `{{name}}` `{{student_id}}` `{{teacher}}` `{{place}}` `{{time}}`
- 正文：`{{body_sec00}}`…`{{body_sec11}}` 依次对应官方十二节（一、实验室名称 … 十二、改进建议）
- 评分栏/签字栏保留空置

## 填充规则

1. 首选：复制 `标准实验报告.docx` 原版做段落匹配替换（保真）；
2. 骨架版用于程序构建路径：替换 `{{...}}` 占位符后交付；
3. 正文替换用"首 run 写入、删其余 run"保格式（见 engines/docx SKILL.md §5）；
4. 用户自有模板优先于本目录一切文件。
