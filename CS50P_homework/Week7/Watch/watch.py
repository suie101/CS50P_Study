import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    # 注意一个重要的区别，就是吗match只看开头，但是search式全文扫描
    if matches := re.search(r"src=\"(\S+)\" ",s):
        print("Group: "+matches.group(1))
        return re.sub(r"(www\.)?youtube\.com/embed/","youtu.be/",matches.group(1))
    else:
        print("No matched src")
        return None


if __name__ == "__main__":
    main()