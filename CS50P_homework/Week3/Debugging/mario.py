def main():
    height = int(input("Height: "))
    pyramid(height)

def pyramid(n):
    for i in range(n):
        print_mine(i)
        

def print_mine(i):
    print("#"*i)
    print("?"*i)

if __name__ == "__main__":
    main()