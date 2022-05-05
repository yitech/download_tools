"""
Python download tools to download large file (e.g. dataset)
"""

import argparse


def download(url: str, dst: str):
    print(f"url: {url}")
    print(f"dst: {dst}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url of download link", type=str)
    parser.add_argument("--dst", help="dst of download link", type=str)
    args = parser.parse_args()

    download(args.url, args.dst)

