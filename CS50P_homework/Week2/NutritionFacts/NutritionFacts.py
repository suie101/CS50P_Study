def main():
    item = input("input the item: ").lower()
    calories_dict = [
        {'name':'apple','calories':130},
        {'name':'banana','calories':110},
        {'name':'grapes','calories':90}
    ]
    for term in calories_dict:
        if  item == term['name']:
            print(f'calories: {term['calories']}')

main()