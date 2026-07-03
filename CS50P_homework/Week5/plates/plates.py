def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    s_strip  = s.strip()
    # 检查长度 和 是否有标点符号 和 前两个不是字母 是否达标
    if (len(s_strip)<2 or len(s_strip)>6 or 
        not s_strip.isalnum() or 
        not s_strip[0:2].isalpha() or
        not s_strip[-1].isdigit()):
        return False
    else:
        return True


if __name__ == "__main__":
    main()