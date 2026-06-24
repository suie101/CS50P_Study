def main():
    # insert_coin = int(input("Please insert the coin (only accept 25 10 5): "))
    back = check50()
    print("The deal finished!")

def check50():

    # 跳出循环的条件是交易结束 或者是交的钱大于50
    res = 50;

    while True:
        insert_coin = int(input("Please insert the coin (only accept 25 10 5): "))
        # 提醒用户输入指定的面额
        if insert_coin  not in [5, 10, 25]:
            continue

        # 还剩余交付
        res = res - insert_coin;

        if res > 0:
            print(f"Amount Due: {res}");
        else:
            print(f"Change Owed: {-res}");
            break

main()
