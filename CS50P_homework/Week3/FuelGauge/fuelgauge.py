def  main():
    while True:
        try:
            fuel = input("Fraction: ")
            X,Y = fuel.split('/')
            z = int(X)/int(Y)*100.00
            percentage = round(z)
            if percentage <= 1:
                print("E")
                break
            elif percentage >= 99:
                print("F")
                break
            elif 1 < percentage < 99:
                print(f"{percentage}%")
                break
            else:
                print("Error num!")


        except ValueError:
            print("Can't convert to X/Y format!")

        except ZeroDivisionError:
            print("Zero division error!")

main()