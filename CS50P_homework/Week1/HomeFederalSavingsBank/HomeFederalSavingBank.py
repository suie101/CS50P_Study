def main():
    greet = input("Greeting: ")
    dollar = cal(greet)
    print(f"You got ${dollar}")


def cal(x):
    
    if x.find('hello',0) != -1:
        y = 0.0
    elif x.find('h',0) != -1:
        y = 20.00
    else:
        y = 100.00

    return y

main()