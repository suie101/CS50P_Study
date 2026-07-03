import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    pattern = r"^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"
    # [1:-1]表示去掉第一个字符和最后一个字符 
    return bool(re.search(rf"{pattern[1:-1]}\.{pattern[1:-1]}\.{pattern[1:-1]}\.{pattern[1:-1]}$", ip.strip()))


if __name__ == "__main__":
    main()