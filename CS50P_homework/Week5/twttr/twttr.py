def main():
    input_string = input("input: ")
    output_string = shorten(input_string)
    print(f"output: {output_string}")


def shorten(input_string):
    out = ""
    for character in input_string:
        if character not in ['A','E','I','O','U','a','e','i','o','u']:
            out += character;

    return out


if __name__ == "__main__":
    main()