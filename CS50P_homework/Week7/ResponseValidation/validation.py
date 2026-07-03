from validator_collection import validators, checkers, errors

try:
    email_address = validators.email(input('Please input the email: '))
    print("Value!")
except errors.EmptyValueError:
    # Handling logic goes here
    print("Empty Value Error!")
except errors.InvalidEmailError:
    # More handlign logic goes here
    print("Invalid Email Error!")