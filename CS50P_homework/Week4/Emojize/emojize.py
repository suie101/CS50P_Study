import emoji

def main():
     x = input('Input: ')
     transfer(x)

def transfer(string):
     string_tranf = emoji.emojize(string)
     print(string_tranf)

main()