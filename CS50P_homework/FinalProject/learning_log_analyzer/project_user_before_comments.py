import re,sys
import csv
import argparse
import json
from pathlib import Path



VALID_STATUSES = {"todo", "doing", "done", "blocked"}

def summarize_records(records: list) -> dict:
    return summarize_records_list(records)

class ReportRecord:
    def __init__(self, data: list[dict]):
        self.data = data
        self.total_minutes = 0
        self.by_topic = {}


    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, record: list[dict] | None) -> None:
        if record == None:
            print("Empty!")
            self._data = []
        else:
            self._data = record

    def __str__(self):
        return f"{self.data}"
    

    def get_total_minutes(self) -> int:
        minutes = [record["duration"] for record in self.data]
        # map函数传入 转换成分钟数
        minutes = map(parse_duration, minutes)
        self.total_minutes = sum(minutes)  
        return self.total_minutes

    def get_topic(self) -> dict:
        by_topic = {}
        for topic in self.data:
            if topic["topic"] not in by_topic.keys():
                by_topic.setdefault(topic["topic"], parse_duration(topic["duration"]))
            else:
                by_topic[topic["topic"]] += parse_duration(topic["duration"])
        self.by_topic = by_topic
        return self.by_topic

    def get_done(self):
        return  [record["task"] for record in self.data if record["status"] == "done"]
    
    def get_completed(self):
        return  [record["task"] for record in self.data if record["status"] == "blocked"]
    


def parse_duration(text: str) -> int:
    """
    Convert duration strings like '1h 30m' or '45m' into minutes .
    
    """
    if matches := re.search(r"(\d+h)?\s?(\d+m)?",text.strip()):
        if matches.group(1) == None and matches.group(2) == None:
            raise ValueError("Can not convert to minutes! ")

        if matches.group(1) != None:
            hours   = int(matches.group(1).removesuffix("h"))
        else:
            hours   = 0
        
        if matches.group(2) != None:
            minutes = int(matches.group(2).removesuffix("m"))
        else:
            minutes = 0

        return hours*60 + minutes
    else:
        raise ValueError("Can not convert to minutes! ")
    


def extract_tags(notes: str) -> list[str]:
    """
    Return tags such as ['pytest', 'oop'] from a notes string.

    """
    # 练习列表推导式
    if matches := re.findall(r"#\S+\b",notes.strip()):
        return [ match.removeprefix("#") for match in matches ]
    else:
        return []


def normalize_status(status: str) -> str:
    """
    Normalize and validate task status.
    
    """
    if status.strip().lower() not in VALID_STATUSES:
        raise ValueError("Invalid STATUSES! ")
    else:
        return status.strip().lower()
    

def generate_records(file_name: str, class_choice: bool) -> list|ReportRecord:
    try:
        with open(file_name,'r') as file:
            records = []
            reader = csv.DictReader(file)
            # 每一行提取成字典
            for row in reader:
                records.append(row)
            report_ins =  ReportRecord(records)
            print(report_ins)
            if class_choice:
                return report_ins
            else:
                return records
    except FileNotFoundError:
            sys.exit("Cannot find such a file! ")

def summarize_records_class(records: ReportRecord) -> dict:
    """
    Return aggregate statistics for learning records.
    使用类定义版
    """
    summary = {}
    # total_minutes
    # 列表推导式
    summary.setdefault("total_minutes", records.get_total_minutes())

    # 根据主题分类
    summary.setdefault("by_topic", records.get_topic())

    # done 任务列表
    summary.setdefault("done", records.get_done())

    # blocked 任务列表
    summary.setdefault("blocked", records.get_completed())
    print("=============================Summary================================\n")

    print(summary)

    return summary



def summarize_records_list(records: list) -> dict:
    """
    Return aggregate statistics for learning records.
    (列表版)
    """
    summary = {}
    # total_minutes
    # 列表推导式
    minutes = [record["duration"] for record in records]
    # map函数传入 转换成分钟数
    minutes = map(parse_duration, minutes)
    total_minutes = sum(minutes)
    summary.setdefault("total_minutes", total_minutes)

    # 根据主题分类
    by_topic = {}
    for topic in records:
        if topic["topic"] not in by_topic.keys():
            by_topic.setdefault(topic["topic"], parse_duration(topic["duration"]))
        else:
            by_topic[topic["topic"]] += parse_duration(topic["duration"])
    # 最后记得添加回去
    summary.setdefault("by_topic", by_topic)

    # done 任务列表
    done = [record["task"] for record in records if record["status"] == "done"]
    summary.setdefault("done", done)

    # blocked 任务列表
    blocked = [record["task"] for record in records if record["status"] == "blocked"]
    summary.setdefault("blocked", blocked)
    print("===============================summary==============================\n")

    print(summary)

    return summary


def render_markdown_report(summary: dict, records: list|ReportRecord) -> list:
    """
    Render a Markdown report from summary data and records.
    
    """

    reports = []
    reports.append('# Learning Summary\n\n')
    reports.append('## Overview\n\n')
    # 总的学习时间统计
    reports.append(f"- Total minutes: {summary['total_minutes']}\n")
    # 已经完成的任务统计
    reports.append(f"- Completed tasks: {len(summary['done'])}\n")
    reports.append(f"-- {', '.join(summary['done'])}\n\n")
    # 阻塞的学习任务统计
    reports.append(f"- Blocked tasks: {len(summary['blocked'])}\n")
    reports.append(f"-- {', '.join(summary['blocked'])}\n\n")

    # 写入相关的主题统计
    reports.append("## By Topic\n\n")
    reports.append("| index | Topic | Minutes |\n")
    for i, key in enumerate(summary['by_topic']) :
        reports.append(f"| {i+1} | {key} | {summary['by_topic'][key]} |\n")


    print("============================Markdown_Reports=================================\n")
    print(reports)

    return reports

def write_to_md(file_name: str, report: list) -> None:
    with open(file_name,'w') as file:
        # writer = csv.writer(file)
        file.writelines(report)



def main():
    """Run the learning log analyzer."""
    parser = argparse.ArgumentParser(description="Generate a study report")
    parser.add_argument("--report", default="reports/summary.md", help="Generate a summary in md", type=str)
    parser.add_argument("--json", default="reports/summary.json", help="Generate a summary in json", type=str)
    args = parser.parse_args()

    choice = True
    BASE_DIR = Path(__file__).resolve().parent # 当前文件的py脚本位置的绝对路径所在目录

    DATA_DIR = BASE_DIR / "data"
    REPORT_DIR = BASE_DIR / "reports"

    CSV_PATH = DATA_DIR / "sample_sessions.csv"
    REPORT_PATH = BASE_DIR /args.report
    JSON_PATH = BASE_DIR / args.json
    records = generate_records(str(CSV_PATH), class_choice=choice)
    if choice:
        summary = summarize_records_class(records)
    else:
        summary = summarize_records_list(records)
    
    if args.json != None:
        summart_json = json.dumps(summary, indent=4)
        with open(str(JSON_PATH),'w') as json_file:
            json_file.write(summart_json)

    report = render_markdown_report(summary, records)
    write_to_md(str(REPORT_PATH),report)



if __name__ == "__main__":
    main()