import time
import requests
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)
sess = requests.Session()


def get_size(url: str):
    response = requests.head(url)
    size = int(response.headers['Content-Length'])
    return size


def requester(start, end):
    url = "https://www.cs.cornell.edu/projects/megadepth/dataset/Megadepth_v1/MegaDepth_v1.tar.gz"
    headers = {
        "Host": "www.cs.cornell.edu",
        "Connection": "keep-alive",
        "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='100', 'Google Chrome';v='100'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Cookie": "_ga=GA1.2.1221016298.1651809175; _gid=GA1.2.779474844.1651809175",
        "Range": f"bytes={start}-{end}",
    }
    rsp = sess.get(url, headers=headers, stream=True, verify=False)
    return rsp


if __name__ == '__main__':
    # setup
    ttl = 200  # GB
    unit = 1024 * 1024 * 1024  # GB to bytes
    n = 50  # Partition
    bytes_ = [int(i / n * unit) for i in range(ttl * n)] + [""]

    # run
    i = 0
    t = time.time()
    while i < ttl * n:
        print("{0:.4%}".format(i / n / ttl), end=": ")
        try:
            rsp = requester(start=bytes_[i], end=bytes_[i + 1])
            if i == 0:
                with open("./downloads/MegaDepth_v1.tar.gz", "wb") as fp:
                    fp.write(rsp.content)
            else:
                with open("./downloads/MegaDepth_v1.tar.gz", "ab") as fp:
                    fp.write(rsp.content)
            print("ok", end=" ")
            print(int(time.time() - t))
            i += 1
        except Exception as e:
            print("fail", end=" ")
            time.sleep(1)
