from pyfiglet import Figlet
import sys
import random

def main():
    # 字体对象
    figlet = Figlet()
    front_list = figlet.getFonts()
    if len(sys.argv) == 1:
        string  = input("Please input the string: ")
        # 随机生成字体
        random_front = random.choice(front_list)
        # 设置字体
        figlet.setFont(font=random_front)
        # 输出
        print(figlet.renderText(string))

    elif len(sys.argv) == 3:
        if sys.argv[1] not in ['-f','--font'] or sys.argv[2] not in front_list:
            sys.exit("No legal arguments")
        else:
            string  = input("Please input the string: ")
            # 设置字体
            figlet.setFont(font=sys.argv[2])
            # 输出
            print(figlet.renderText(string))           


    else:
        sys.exit("Please input 0 or 2 arguments")

main()


    