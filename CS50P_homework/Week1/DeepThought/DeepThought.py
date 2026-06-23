def main():
    x = input("the answer to the Great Question of Life, the Universe and Everything").strip()
    y = check(x)
    if y:
        print('Yes')
    else:
        print('No')

def check(x):
    return (x == '42' or x == 'forty-two' or x == 'forty two')

main()