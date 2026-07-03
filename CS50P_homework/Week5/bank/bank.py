def main():
    greet = input("Greeting: ")
    dollar = value(greet)
    print(f"You got ${dollar}")


def value(x):
    if x.strip().lower()[0:5] == "hello":
        y = 0.0
    elif x.strip().lower()[0] == "h":
        y = 20.00
    else:
        y = 100.00

    return y

if __name__ == "__main__":
    main()
