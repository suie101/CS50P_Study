import requests
import sys

def main():
    # 检测命令行输入
    if len(sys.argv) == 1:
        sys.exit("Missing the command-line message!")

    # 类型转换
    try:
        bitcoin = float(sys.argv[1])
    except:
        sys.exit("can't convert to float!")

    # 网页抓取
    try:
        response = requests.get('https://rest.coincap.io/v3/assets/bitcoin?apiKey=54d21f926795870a29d259479c4bac951867ee5965a3a274a5adb5cad5b6d490')
        response = response.json()
        priceUsd = response["data"]["priceUsd"]
        price    = bitcoin * float(priceUsd)
        print(f"{price:.4f}")

    except requests.RequestException:
        sys.exit()

main()