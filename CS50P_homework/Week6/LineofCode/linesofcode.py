# 需求是统计代码行数
# 跳过注释和空白行
import sys
def main():
    try:
        if len(sys.argv) > 2:
            print("Too many command line arguments!")
        elif len(sys.argv) <= 1:
            print("Too few command line arguments!")
        elif sys.argv[1].endswith('.py') != 1:
            print("Not a python file!")
        else:
            with open(f"{sys.argv[1]}",'r') as file:
                lines = file.readlines() # 返回一个文件每一行为元素的列表
                count = 0

            for line in lines:
                if (line.startswith('#') != True)  and (line.isspace() != True):
                    count += 1
            print(f"There are {count} lines of codes in this python file ")

    except FileNotFoundError:
        sys.exit("Not exit such a python file!")

main()