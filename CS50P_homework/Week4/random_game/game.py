import random

def main():
    
    true_num = random.randint(1,100)
    while True:
        number = int(input("Please input the number between 1 and 100: "))
        if  1 <= number <= 100:
            if number > true_num:
                print("Too large!")
                continue
            elif number < true_num:
                print("Too small!")
                continue
            else:
                print("Just right!")
                break
        else:
            continue

main()