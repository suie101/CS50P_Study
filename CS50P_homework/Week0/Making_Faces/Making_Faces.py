def main():
    string_mine = input("Please enter a string: ")

    # Replace :) with 🙂 and :( with 🙁
    string_face = convert(string_mine)

    print(string_face)

def convert(string):
    return string.replace(":)", "🙂").replace(":(", "🙁")

main()