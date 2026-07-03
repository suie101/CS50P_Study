import sys
import csv
from tabulate import tabulate

def main():
    try:
        if len(sys.argv) > 2:
            sys.exit("Too many command line arguments!")
        elif len(sys.argv) <= 1:
            sys.exit("Too few command line arguments!")
        elif sys.argv[1].endswith('.csv') != 1:
            sys.exit("Not a csv file!")
        else:
            with open(f"{sys.argv[1]}",'r') as file:
                reader = csv.DictReader(file) # 返回一个文件每一行为元素的列表
                print(tabulate(reader,headers="keys",tablefmt="grid"))
                # for row in reader:
                #     print(f"{row['Sicilian Pizza']}-{row['Small']}-{row['Large']} ")

    except FileNotFoundError:
        sys.exit("Not such a csv file! ")

main()