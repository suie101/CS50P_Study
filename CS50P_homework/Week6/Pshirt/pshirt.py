import sys
from PIL import Image,ImageOps

def main():
    try:
        if len(sys.argv)>3:
            sys.exit("Too many command-line arguments")
        elif len(sys.argv)<3:
            sys.exit("Too few command-line arguments")
            # Python 官方类型提示（type hint）+ 函数签名说明
        elif not sys.argv[1].strip().endswith((".jpg",".jpeg",".png")) or not sys.argv[2].strip().endswith((".jpg",".jpeg",".png")):
            sys.exit("Must be jpg jpeg and png!")
        elif sys.argv[1].strip().split(".")[1] != sys.argv[2].strip().split(".")[1]:
            sys.exit("Must be the same format!")
        else:  
            with Image.open(sys.argv[1]) as before:
                with Image.open("shirt.png") as shirt:
                    shirt_size = shirt.size
                    im_fit = ImageOps.fit(before,size=shirt_size)
                    im_fit.save(sys.argv[1].strip().split(".")[0]+"_fit."+sys.argv[1].strip().split(".")[1])
                    # 注意三个参数第一个是要覆盖的图，第二个图是覆盖的位置，第三个是透明遮罩
                    im_fit.paste(shirt,(0,0),shirt) # 注意返回值是None 是原地修改图片 并不会返回图片对象
                    im_fit.save(sys.argv[2])

    except FileNotFoundError:
        sys.exit("Not found file!")

main()