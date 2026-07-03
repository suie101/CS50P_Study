def main():
    items = []
    grocery_list = {}
    while True:
        try:
            item = input("input the item: ")
            if item.upper() not in grocery_list:
                grocery_list.setdefault(item.strip().upper(),1)
            else:
                grocery_list[item.upper()] = grocery_list[item.upper()] + 1
                
        except EOFError:
            print()
            # 如果想根据字典的值进行排序 sorted(grocery_list,key=grocery_list.get)
            for grocery in sorted(grocery_list.keys()):
                print(f"{grocery_list[grocery]}   {grocery}")
            break

main()