def main():
    month_list = {
        "January": '1',
        "February": '2',
        "March": '3',
        "April": '4',
        "May": '5',
        "June": '6',
        "July": '7',
        "August": '8',
        "September": '9',
        "October": '10',
        "November": '11',
        "December": '12'
    }
    month = 0
    day = 0
    year = 0

    while True:
        try:
            date = input("Please input the date: ")
            if date.find('/') != -1:
                month,day,year = date.split('/')
            elif date.find(',') != -1:
                month_day, year = date.split(',')
                year = year.strip()
                months,day = month_day.split()
                if months.title() not in month_list.keys():
                    print("Wrong month! ")
                    continue
                else:
                    month = month_list[months.title()]
            else:
                print("Wrong format! ")
                continue

            month = int(month)
            day   = int(day)
            year  = int(year)
            if 1<=month<=12 and 1<=day<=31 and year>0:
                print(f"{int(year)}-{int(month)}-{int(day)}")
            else:
                print("Wrong month day  year number! ")

            break
        except ValueError:
            print("Please input the right format! ")

main()