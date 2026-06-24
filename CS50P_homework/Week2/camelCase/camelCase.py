def main():
    camel_name = input("Please input the camel name: ");
    snake_name = snake(camel_name)
    print(f"The snake name : {snake_name}")


# Python 的 str 是不可变对象，不能像列表那样直接改某个位置

def snake(camel_name):
    snake_name  = "";
    for character in  camel_name:
        if character.isupper():
             snake_name += '_' + character.lower()
        else:
            snake_name += character
    
    return snake_name

main()