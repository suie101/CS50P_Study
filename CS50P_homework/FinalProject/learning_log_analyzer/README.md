# Learning Log Analyzer

A CS50P final project that reads learning-session records from CSV, summarizes study time and task status, and writes Markdown / JSON reports.

本项目用于练习 CS50P Python 基础知识：函数、CSV、正则、异常处理、OOP、argparse、文件 I/O、JSON 和 pytest。

## Files

```text
learning_log_analyzer/
├── project.py                         # 用户自己的正式版本
├── project_codex.py                   # Codex 写的 Pythonic 参考版本
├── project_user_before_comments.py    # 添加注释前的用户版本备份
├── test_project.py                    # pytest 测试
├── data/
│   └── sample_sessions.csv            # 示例输入数据
└── reports/
    ├── summary.md                     # 用户版本输出
    ├── summary.json                   # 用户版本输出
    ├── summary_codex.md               # Codex 参考版本输出
    └── summary_codex.json             # Codex 参考版本输出
```

## Requirements

The project uses only Python standard-library modules:

- `argparse`
- `csv`
- `json`
- `pathlib`
- `re`
- `collections`
- `dataclasses`

For testing, install `pytest` in the CS50P virtual environment.

## Input CSV Format

```csv
date,topic,task,status,duration,notes
2026-07-03,Python,Jar pytest,done,35m,"pytest 4 passed #pytest #oop"
```

Columns:

| Column | Meaning | Example |
| --- | --- | --- |
| `date` | Session date | `2026-07-03` |
| `topic` | Topic name | `Python` |
| `task` | Task description | `Jar pytest` |
| `status` | `todo`, `doing`, `done`, or `blocked` | `done` |
| `duration` | Study duration | `45m`, `1h`, `1h 30m`, `2h30m` |
| `notes` | Free notes with optional tags | `#pytest #oop` |

## Run User Version

```bash
cd /home/labpc/code/python_experiment_lab/CS50P/CS50P_homework/FinalProject/learning_log_analyzer
/home/labpc/code/python_experiment_lab/CS50P/cs50p/bin/python project.py
```

Default outputs:

```text
reports/summary.md
reports/summary.json
```

You can also pass output paths:

```bash
/home/labpc/code/python_experiment_lab/CS50P/cs50p/bin/python project.py --report reports/summary.md --json reports/summary.json
```

## Run Codex Reference Version

```bash
/home/labpc/code/python_experiment_lab/CS50P/cs50p/bin/python project_codex.py data/sample_sessions.csv --report reports/summary_codex.md --json reports/summary_codex.json
```

The Codex version is intended for comparison and learning. It uses `dataclass`, `Counter`, `pathlib`, `argparse`, and `utf-8-sig` CSV reading.

## Run Tests

```bash
/home/labpc/code/python_experiment_lab/CS50P/cs50p/bin/python -m pytest -q
```

Expected current result:

```text
5 passed in 0.01s
```

## Tested Functions

`test_project.py` currently tests:

- `parse_duration`
- `extract_tags`
- `normalize_status`
- `summarize_records` import compatibility

## Notes For Learning

- `project.py` contains the user's implementation with added Chinese comments explaining the Python knowledge points.
- `project_codex.py` is a separate reference implementation and does not replace the user's code.
- `project_user_before_comments.py` preserves the user's version before comments were added.