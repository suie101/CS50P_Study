"""Codex reference implementation for the CS50P final project.

这个文件是 Codex 写的参考版本，不覆盖用户自己的 project.py。
目标是展示一版更 Pythonic、结构更清楚、便于测试和扩展的实现。
"""

from __future__ import annotations

# Python 知识点：标准库导入
# argparse: 命令行参数；csv: 读取 CSV；json: 输出机器可读报告；re: 正则；
# Counter: 计数；dataclass: 简洁定义数据对象；Path: 跨平台路径处理。
import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


# Python 知识点：常量约定
# Python 没有强制常量，使用全大写变量名表示“不要在运行中修改”。
VALID_STATUSES = {"todo", "doing", "done", "blocked"}

# Python 知识点：预编译正则
# 多次使用的正则可以先 compile，命名后也更容易理解意图。
DURATION_RE = re.compile(r"^\s*(?:(?P<hours>\d+)h)?\s*(?:(?P<minutes>\d+)m)?\s*$", re.IGNORECASE)
TAG_RE = re.compile(r"#([A-Za-z0-9][A-Za-z0-9_-]*)")


@dataclass
class StudyRecord:
    """One normalized learning-log row.

    Python 知识点：dataclass / OOP
    dataclass 自动生成 __init__ 等方法，适合这种“主要保存数据”的类。
    这里把 CSV 的原始字符串行转换成类型更明确的对象：duration 已经是分钟，tags 已经是 list。
    """

    date: str
    topic: str
    task: str
    status: str
    duration_minutes: int
    notes: str
    tags: list[str]

    @property
    def is_done(self) -> bool:
        """Return whether this task is done.

        Python 知识点：@property
        调用方可以写 record.is_done，而不是 record.is_done()，读起来像属性。
        """

        return self.status == "done"

    @property
    def is_blocked(self) -> bool:
        """Return whether this task is blocked."""

        return self.status == "blocked"

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "StudyRecord":
        """Build a StudyRecord from a CSV DictReader row.

        Python 知识点：classmethod
        这是“替代构造器”：把一行 CSV 字典转换成 StudyRecord 对象。
        """

        return cls(
            date=row["date"].strip(),
            topic=row["topic"].strip(),
            task=row["task"].strip(),
            status=normalize_status(row["status"]),
            duration_minutes=parse_duration(row["duration"]),
            notes=row.get("notes", "").strip(),
            tags=extract_tags(row.get("notes", "")),
        )


def parse_duration(text: str) -> int:
    """Convert duration strings like '1h 30m' or '45m' into minutes.

    Python 知识点：正则表达式 + 异常处理
    支持 45m、1h、1h 30m、2h30m。非法输入抛 ValueError，便于 pytest 测试。
    """

    match = DURATION_RE.fullmatch(text)
    if not match or not (match.group("hours") or match.group("minutes")):
        raise ValueError(f"Invalid duration: {text}")

    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    return hours * 60 + minutes


def extract_tags(notes: str) -> list[str]:
    """Return tags such as ['pytest', 'oop'] from a notes string.

    Python 知识点：re.findall
    捕获组只返回 # 后面的标签文本，不把 # 本身放进结果。
    """

    return TAG_RE.findall(notes)


def normalize_status(status: str) -> str:
    """Normalize and validate task status.

    Python 知识点：字符串清洗 + set 成员检查 + raise
    strip/lower 处理输入格式差异；set 适合判断状态是否合法。
    """

    normalized = status.strip().lower()
    if normalized not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    return normalized


def load_records(csv_path: Path) -> list[StudyRecord]:
    """Read CSV rows and return normalized StudyRecord objects.

    Python 知识点：文件 I/O + csv.DictReader + pathlib
    encoding='utf-8-sig' 可以自动处理 UTF-8 BOM，避免字段名变成 '\ufeffdate'。
    """

    required_fields = {"date", "topic", "task", "status", "duration", "notes"}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty")

        missing = required_fields - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        return [StudyRecord.from_row(row) for row in reader]


def summarize_records(records: list[StudyRecord]) -> dict:
    """Return aggregate statistics for learning records.

    Python 知识点：dict / Counter / list comprehension
    把“多条记录”汇总成总时长、按 topic 汇总、按 status 计数、tag 计数等结构化结果。
    """

    by_topic: Counter[str] = Counter()
    by_status: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    done_tasks: list[str] = []
    blocked_tasks: list[str] = []

    for record in records:
        by_topic[record.topic] += record.duration_minutes
        by_status[record.status] += 1
        tag_counts.update(record.tags)

        if record.is_done:
            done_tasks.append(record.task)
        if record.is_blocked:
            blocked_tasks.append(record.task)

    return {
        "total_minutes": sum(record.duration_minutes for record in records),
        "by_topic": dict(sorted(by_topic.items())),
        "by_status": dict(sorted(by_status.items())),
        "tag_counts": dict(sorted(tag_counts.items())),
        "done": done_tasks,
        "blocked": blocked_tasks,
    }


def render_markdown_report(summary: dict, records: list[StudyRecord]) -> str:
    """Render a Markdown report from summary data and records.

    Python 知识点：字符串拼接 / Markdown 表格 / join
    先把每一行放入 list，最后用 ''.join(lines) 合成完整文本。
    """

    lines = [
        "# Learning Summary\n\n",
        "## Overview\n\n",
        f"- Total minutes: {summary['total_minutes']}\n",
        f"- Total records: {len(records)}\n",
        f"- Completed tasks: {len(summary['done'])}\n",
        f"- Blocked tasks: {len(summary['blocked'])}\n\n",
    ]

    lines.extend([
        "## By Topic\n\n",
        "| Topic | Minutes |\n",
        "| --- | ---: |\n",
    ])
    for topic, minutes in summary["by_topic"].items():
        lines.append(f"| {topic} | {minutes} |\n")

    lines.extend([
        "\n## By Status\n\n",
        "| Status | Count |\n",
        "| --- | ---: |\n",
    ])
    for status, count in summary["by_status"].items():
        lines.append(f"| {status} | {count} |\n")

    lines.extend([
        "\n## Tags\n\n",
        "| Tag | Count |\n",
        "| --- | ---: |\n",
    ])
    for tag, count in summary["tag_counts"].items():
        lines.append(f"| #{tag} | {count} |\n")

    if summary["blocked"]:
        lines.append("\n## Blocked Tasks\n\n")
        for task in summary["blocked"]:
            lines.append(f"- {task}\n")

    return "".join(lines)


def write_text(path: Path, content: str) -> None:
    """Write text content to a file, creating parent directories if needed.

    Python 知识点：pathlib + 文件写入
    parent.mkdir(..., exist_ok=True) 确保 reports/ 目录存在。
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, summary: dict, records: list[StudyRecord]) -> None:
    """Write JSON report to a file.

    Python 知识点：json.dumps + dataclass asdict
    JSON 适合机器读取；Markdown 适合人阅读。
    """

    payload = {
        "summary": summary,
        "records": [asdict(record) for record in records],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_path(base_dir: Path, value: str) -> Path:
    """Resolve a command-line path relative to the project directory.

    Python 知识点：pathlib 路径处理
    用户传相对路径时，相对于 project_codex.py 所在目录解释；传绝对路径时直接使用。
    """

    path = Path(value)
    if path.is_absolute():
        return path
    return base_dir / path


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Python 知识点：argparse
    把 CLI 参数定义单独放进函数，main() 会更短，也更容易测试和维护。
    """

    parser = argparse.ArgumentParser(description="Generate a learning-log summary report")
    parser.add_argument("csv_path", nargs="?", default="data/sample_sessions.csv", help="input CSV file")
    parser.add_argument("--report", default="reports/summary_codex.md", help="Markdown report path")
    parser.add_argument("--json", default="reports/summary_codex.json", help="JSON report path")
    return parser


def main() -> None:
    """Run the learning log analyzer.

    Python 知识点：main 入口
    main 只负责串流程：解析参数 -> 读取数据 -> 汇总 -> 渲染 -> 写文件。
    """

    base_dir = Path(__file__).resolve().parent
    args = build_parser().parse_args()

    csv_path = resolve_path(base_dir, args.csv_path)
    markdown_path = resolve_path(base_dir, args.report)
    json_path = resolve_path(base_dir, args.json)

    records = load_records(csv_path)
    summary = summarize_records(records)
    markdown = render_markdown_report(summary, records)

    write_text(markdown_path, markdown)
    write_json(json_path, summary, records)

    print(markdown)
    print(f"Markdown report written to: {markdown_path}")
    print(f"JSON report written to: {json_path}")


if __name__ == "__main__":
    main()