import sys
import re
import inflect
import datetime as dt


def main():
    birth = input("Date of Birth: ").strip()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", birth):
        sys.exit("Invalid date")

    try:
        year, month, day = birth.split("-")
        born_day = dt.date(int(year), int(month), int(day))
    except ValueError:
        sys.exit("Invalid date")

    today = dt.date.today()
    minutes = (today - born_day).days * 24 * 60

    p = inflect.engine()
    words = p.number_to_words(minutes, andword="")
    print(f"{words.capitalize()} minutes")


if __name__ == "__main__":
    main()