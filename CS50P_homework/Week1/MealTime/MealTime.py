def main():
    time_now = input('Please input the time now: ')
    time_new = convert(time_now)
    if 7.0 <= time_new <= 8.0:
        print('breakfast time')
    elif 12.0 <= time_new <= 13.0:
        print('lunch  time')
    elif 18.0 <= time_new <= 19.0:
        print('dinner  time')
    else:
        print('No in special time')

def convert(time):
    hour,minu = time.split(':')
    hour = int(hour)
    minu = int(minu)
    time_new = float(hour + minu/60)
    return time_new


if __name__ == "__main__":
    main()