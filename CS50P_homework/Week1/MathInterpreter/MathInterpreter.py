def main():
    expression = input('Please input the expressions: ')
    x,y,z = expression.split(' ')
    if cal(x,y,z) == 'None':
        print('不支持的运算!')
    else:
        result = float(cal(x,y,z))
        print(f"Result: {result:.1f}")
    
    

def cal(x,y,z):
    x_int = int(x)
    z_int = int(z)
    if y == '+':
        result = str(x_int+z_int) 
    elif y == '-':
        result = str(x_int-z_int)
    elif y == '*':
        result = str(x_int*z_int)
    elif y == '/':
        result = str(x_int/z_int)
    else:
        result = 'None'

    return result


main()