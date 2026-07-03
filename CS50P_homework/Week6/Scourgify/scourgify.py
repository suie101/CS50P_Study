import csv
import sys

def main():
    try:
        if len(sys.argv) > 3:
            sys.exit("Too many command line arguments!")
        elif len(sys.argv) < 3:
            sys.exit("Too few command line arguments!")
        elif not sys.argv[1].endswith('.csv') and not sys.argv[2].endswith('.csv'):
            sys.exit("Not a csv file!")
        else:
            with open(f"{sys.argv[1]}",'r') as csvRead:
                with open(f"{sys.argv[2]}",'w') as csvWrite:
                    reader = csv.DictReader(csvRead) # 返回一个文件每一行为元素的列表
                    fieldnames_reader = reader.fieldnames
                    fieldnames_writer = ['first','last','house']
                    writer = csv.DictWriter(csvWrite,fieldnames=fieldnames_writer)
                    writer.writeheader() # 记得先写头
                    for row in reader:
                        last, first = row["name"].strip().split(", ")
                        house = row["house"].strip()
                        writer.writerow({fieldnames_writer[0]:first,fieldnames_writer[1]:last,fieldnames_writer[2]:house})
    except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")


main()