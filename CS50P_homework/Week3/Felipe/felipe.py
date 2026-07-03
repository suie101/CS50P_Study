def main():
    meau = {
        "Baja Taco": 4.25,
        "Burrito": 7.50,
        "Bowl": 8.50,
        "Nachos": 11.00,
        "Quesadilla": 8.50,
        "Super Burrito": 8.50,
        "Super Quesadilla": 9.50,
        "Taco": 3.00,
        "Tortilla Salad": 8.00
    }
    
    total_money = 0

    while True:
        try:
            item = input("what you want: ")
            # 查询是否在菜单内
            if item.title() in meau:
                total_money += float(meau[item.title()])
                print(f"total money:{total_money}")
            else:
                print("Please input the item in the menu!")

        except EOFError:
            print(f"total money:{total_money}")
            break

main()