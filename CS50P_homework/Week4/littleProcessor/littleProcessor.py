import random



def main():
    level = get_level()
    score = 0
    x,y = generate_integer(level)


    for question_index in range(len(x)):
        try_num = 0
        while try_num <= 2:
            user_answer = int(input(f'{x[question_index]} + {y[question_index]} = ')) 
            if user_answer == x[question_index] + y[question_index]:
                score += 1
                break
            elif try_num == 2:
                print('EEE, the answer is: ')
                print(f'{x[question_index]} + {y[question_index]} = {x[question_index]+y[question_index]}')
                break
            else:
                print('EEE: ')
                try_num += 1

    print(f"Scores: {score}")


def get_level():

    level = int(input('Please input the level (1,2,3) : '))
    if level not in [1,2,3]:
        raise ValueError("PLEASE INPUT 1 , 2 , 3 !!!")
    
    return level


def generate_integer(level):
    x = []
    y = []
    for _ in range(10):
        x.append(random.randint(10 ** (level - 1), 10**level - 1))
        y.append(random.randint(10 ** (level - 1), 10**level - 1))

    return x,y


if __name__ == "__main__":
    main()