def main():
    m = int(input("Please input the mass: "))
    E = Einstein(m)
    print("E:",E,sep=' ',end=' hello\n')

def Einstein(x):
    c = 3*(10**8)
    return x*c*c

main()