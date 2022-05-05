"""
test url: https://www.python.org/static/img/python-logo@2x.png
size of file: 16 KB
workdir: project dir
cmd: python download_simple/main.py --url=https://www.python.org/static/img/python-logo@2x.png --dst=python.png
"""

import argparse
import requests
from tqdm import tqdm


def download(url: str, dst: str, chunk_size: int = 1024):
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(dst, 'wb') as out:
            for chunk in tqdm(r.iter_content(chunk_size)):
                out.write(chunk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url of file", type=str)
    parser.add_argument("--dst", help="dst of file", type=str)
    args = parser.parse_args()

    download(args.url, args.dst)

