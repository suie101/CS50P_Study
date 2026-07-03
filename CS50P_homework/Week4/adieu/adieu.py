import inflect

def main():
    p = inflect.engine()
    name  = []
    while True:
        try:
            in_string = input("Name: ")
            name.append(in_string.strip())
        except EOFError:
            name_join = p.join(name)
            print(f"dieu, adieu, to {name_join}")
            break

main()
