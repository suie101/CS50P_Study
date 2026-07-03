# 说明：这是用户自己的 project.py 实现。
# 本次只添加中文学习注释，不改变你的代码逻辑，方便和 project_user_before_comments.py 对照。

# Python 知识点：import 导入标准库
# re: 正则表达式，用来解析 duration 和 tags。
# sys: 程序退出 sys.exit。
# csv: 读取 CSV 文件。
# argparse: 命令行参数解析。
# json: 输出 JSON 报告。
# pathlib.Path: 更现代、更稳定的路径处理。
import re,sys
import csv
import argparse
import json
from pathlib import Path


# Python 知识点：常量 + set 集合
# 用全大写变量名表示“常量约定”。set 适合做成员检查，判断 status 是否在允许集合中。
VALID_STATUSES = {"todo", "doing", "done", "blocked"}

# Python 知识点：函数封装 / 兼容测试接口
# test_project.py 需要从 project import summarize_records。
# 这里用一个包装函数，把通用名字 summarize_records 转交给你的 list 版本实现。
def summarize_records(records: list) -> dict:
    return summarize_records_list(records)

# Python 知识点：OOP 类 / 对象封装
# ReportRecord 把 records 数据和围绕 records 的统计方法放在一起。
# 这体现了 class 的核心动机：把“数据”和“操作这些数据的方法”绑定起来。
class ReportRecord:
    # Python 知识点：__init__ 构造方法
    # 创建 ReportRecord(records) 时会自动调用，初始化对象内部状态。
    def __init__(self, data: list[dict]):
        self.data = data
        self.total_minutes = 0
        self.by_topic = {}


    # Python 知识点：@property getter
    # 让外部可以用 report.data 访问内部 _data，同时保留未来做校验的入口。
    @property
    def data(self):
        return self._data
    
    # Python 知识点：@property setter
    # 当执行 self.data = data 时，会进入这个 setter，而不是直接赋值。
    @data.setter
    def data(self, record: list[dict] | None) -> None:
        # Python 知识点：None 判断
        # 如果传入 None，用空列表兜底，避免后续 for 循环时报错。
        if record == None:
            print("Empty!")
            self._data = []
        else:
            self._data = record

    # Python 知识点：__str__ 魔术方法
    # print(report_ins) 时会调用这个方法，决定对象如何转换成字符串。
    def __str__(self):
        return f"{self.data}"
    

    # Python 知识点：实例方法
    # self 表示当前 ReportRecord 对象；这个方法统计当前对象中所有记录的总分钟数。
    def get_total_minutes(self) -> int:
        # Python 知识点：列表推导式
        # 从每条 record 字典中取出 duration 字段，形成一个列表。
        minutes = [record["duration"] for record in self.data]
        # Python 知识点：map 函数
        # 把 parse_duration 应用到每个 duration 字符串上，得到分钟数迭代器。
        minutes = map(parse_duration, minutes)
        # Python 知识点：sum 聚合
        # 把所有分钟数加起来，得到总学习时间。
        self.total_minutes = sum(minutes)  
        return self.total_minutes

    # Python 知识点：字典聚合
    # 按 topic 汇总每个主题的学习分钟数。
    def get_topic(self) -> dict:
        by_topic = {}
        for topic in self.data:
            # Python 知识点：字典 key 检查
            # 如果这个 topic 第一次出现，就初始化；否则累加。
            if topic["topic"] not in by_topic.keys():
                by_topic.setdefault(topic["topic"], parse_duration(topic["duration"]))
            else:
                by_topic[topic["topic"]] += parse_duration(topic["duration"])
        self.by_topic = by_topic
        return self.by_topic

    # Python 知识点：列表推导式 + 条件过滤
    # 提取所有 status == done 的任务名。
    def get_done(self):
        return  [record["task"] for record in self.data if record["status"] == "done"]
    
    # Python 知识点：列表推导式 + 条件过滤
    # 函数名叫 get_completed，但实际取的是 blocked 任务；后续可考虑改名为 get_blocked。
    def get_completed(self):
        return  [record["task"] for record in self.data if record["status"] == "blocked"]
    


# Python 知识点：函数 + 正则表达式 + 异常处理
# 这个函数把 "1h 30m"、"45m"、"2h30m" 转换成整数分钟数。
def parse_duration(text: str) -> int:
    """
    Convert duration strings like '1h 30m' or '45m' into minutes .
    
    """
    # Python 知识点：海象运算符 :=
    # 一边执行 re.search，一边把结果保存到 matches。
    # 正则中 (\d+h)? 表示可选的小时部分，(\d+m)? 表示可选的分钟部分。
    if matches := re.search(r"(\d+h)?\s?(\d+m)?",text.strip()):
        # Python 知识点：捕获组 group
        # group(1) 是小时部分，group(2) 是分钟部分；如果两者都没有，说明输入非法。
        if matches.group(1) == None and matches.group(2) == None:
            raise ValueError("Can not convert to minutes! ")

        if matches.group(1) != None:
            # Python 知识点：字符串方法 removesuffix
            # "2h" 去掉后缀 "h" 后变成 "2"，再 int 转成整数。
            hours   = int(matches.group(1).removesuffix("h"))
        else:
            hours   = 0
        
        if matches.group(2) != None:
            minutes = int(matches.group(2).removesuffix("m"))
        else:
            minutes = 0

        return hours*60 + minutes
    else:
        # Python 知识点：raise 主动抛异常
        # 让调用者或 pytest 明确知道输入不合法。
        raise ValueError("Can not convert to minutes! ")
    


# Python 知识点：正则 findall + 列表推导式
# 从 notes 中提取 #pytest、#oop 这样的标签，并去掉 #。
def extract_tags(notes: str) -> list[str]:
    """
    Return tags such as ['pytest', 'oop'] from a notes string.

    """
    # 练习列表推导式
    if matches := re.findall(r"#\S+\b",notes.strip()):
        return [ match.removeprefix("#") for match in matches ]
    else:
        return []


# Python 知识点：输入标准化 + set 成员检查
# 把状态字符串变成小写并去掉空格，然后判断是否属于允许集合。
def normalize_status(status: str) -> str:
    """
    Normalize and validate task status.
    
    """
    if status.strip().lower() not in VALID_STATUSES:
        raise ValueError("Invalid STATUSES! ")
    else:
        return status.strip().lower()
    

# Python 知识点：文件 I/O + csv.DictReader + 函数返回值
# 读取 CSV 文件，把每一行变成一个字典；可选择返回 list 或 ReportRecord 对象。
def generate_records(file_name: str, class_choice: bool) -> list|ReportRecord:
    try:
        # Python 知识点：with open 上下文管理器
        # with 会在代码块结束后自动关闭文件。
        with open(file_name,'r') as file:
            records = []
            # Python 知识点：csv.DictReader
            # 根据 CSV 表头把每一行转换成 dict，例如 row["topic"]。
            reader = csv.DictReader(file)
            # 每一行提取成字典
            for row in reader:
                records.append(row)
            # Python 知识点：创建对象
            # 把 records 列表封装进 ReportRecord，使用类方法统计。
            report_ins =  ReportRecord(records)
            print(report_ins)
            if class_choice:
                return report_ins
            else:
                return records
    except FileNotFoundError:
            # Python 知识点：异常处理 + sys.exit
            # 文件不存在时终止程序并给出提示。
            sys.exit("Cannot find such a file! ")

# Python 知识点：OOP 版本汇总
# 输入是 ReportRecord 对象，统计逻辑委托给对象的方法。
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



# Python 知识点：list/dict 版本汇总
# 输入是 list[dict]，直接用循环、字典和列表推导式完成统计。
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


# Python 知识点：字符串构造 + Markdown 报告生成
# 输入 summary 字典，输出一个由多行字符串组成的 list，后续写入 .md 文件。
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
    # Python 知识点：enumerate
    # 同时拿到序号 i 和字典 key，用于生成表格序号。
    for i, key in enumerate(summary['by_topic']) :
        reports.append(f"| {i+1} | {key} | {summary['by_topic'][key]} |\n")


    print("============================Markdown_Reports=================================\n")
    print(reports)

    return reports

# Python 知识点：文件写入
# 把 render_markdown_report 生成的字符串列表写入 Markdown 文件。
def write_to_md(file_name: str, report: list) -> None:
    with open(file_name,'w') as file:
        # writer = csv.writer(file)
        file.writelines(report)



# Python 知识点：main 函数 + argparse + pathlib + 程序主流程
# main 负责串联完整流程：解析参数 -> 找路径 -> 读 CSV -> 汇总 -> 写 JSON/Markdown。
def main():
    """Run the learning log analyzer."""
    parser = argparse.ArgumentParser(description="Generate a study report")
    # Python 知识点：argparse 可选参数
    # --report 控制 Markdown 输出路径；--json 控制 JSON 输出路径。
    parser.add_argument("--report", default="reports/summary.md", help="Generate a summary in md", type=str)
    parser.add_argument("--json", default="reports/summary.json", help="Generate a summary in json", type=str)
    args = parser.parse_args()

    # Python 知识点：布尔变量控制流程
    # choice=True 时使用 OOP 类版本；False 时使用 list/dict 版本。
    choice = True
    # Python 知识点：Path(__file__).resolve().parent
    # 找到当前 project.py 所在目录，避免运行命令位置变化导致相对路径失效。
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
    
    # Python 知识点：JSON 序列化
    # json.dumps 把 Python dict 转成 JSON 字符串；indent=4 让输出更易读。
    if args.json != None:
        summart_json = json.dumps(summary, indent=4)
        with open(str(JSON_PATH),'w') as json_file:
            json_file.write(summart_json)

    report = render_markdown_report(summary, records)
    write_to_md(str(REPORT_PATH),report)


# Python 知识点：脚本入口保护
# 直接运行 project.py 时执行 main；被 pytest import 时不会自动跑 main。
if __name__ == "__main__":
    main()