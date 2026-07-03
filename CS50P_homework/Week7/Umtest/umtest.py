import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    # 一个重要的知识点，就是\b匹配的是\w和\W的边界，可以问AI一个具体例子就懂了
    if matches := re.findall(r"\b(Um|um)\b",s):
        return len(matches)
    else:
        return None

if __name__ == "__main__":
    main()