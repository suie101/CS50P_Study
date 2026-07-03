import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    # 注意一个点，就是小括号内部的记得只需要搜索，而不需要匹配到结果里面
    if matches := re.search(r"((?:1[0-2]|0?[0-9])(?::[0-5][0-9])?)\s(AM|PM)\s\S*\s((?:1[0-2]|0?[0-9])(?::[0-5][0-9])?)\s(AM|PM)",s):
        print(matches.group(3))
        time_before = matches.group(1)
        time_after = matches.group(3)
        if ":" not in matches.group(1):
            time_before += ":00"
        if ":" not in matches.group(3):
            time_after  += ":00"
        print(time_before)
        print(time_after)
        time_before_hours, time_before_minus = time_before.split(":")
        time_after_hours, time_after_minus   = time_after.split(":")

        time_before_hours = int(time_before_hours)
        time_before_hours += (matches.group(2) == "PM")*12
        time_after_hours = int(time_after_hours)
        time_after_hours += (matches.group(4) == "PM")*12
        print(f"{time_before_hours:02}:{time_before_minus:02} to {time_after_hours:02}:{time_after_minus:02}")

    else:
        print("Wrong input format! ")




if __name__ == "__main__":
    main()