def main():
    file_name = input("Please input the file name: ")
    file_suffix = suffix(file_name)
    print(file_suffix)

def suffix(f):
    if f.find('.') == -1:
        file_format = 'application/octet-stream'
        return  file_format
    
    _ , file_suffix = f.split('.')
    if file_suffix == 'gif':
        file_format = 'image/gif'
    elif file_suffix == 'jpg' or file_suffix == 'jpeg':
        file_format = 'image/jpeg'
    else:
        file_format = 'application/octet-stream'

    return file_format

main()
