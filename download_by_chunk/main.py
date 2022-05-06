"""
Python download tools to download large file (e.g. dataset)
test url: https://www.cs.cornell.edu/projects/megadepth/dataset/Megadepth_v1/MegaDepth_v1.tar.gz
size of file: 199 GB
workdir: project dir

cmd:
export url=https://www.cs.cornell.edu/projects/megadepth/dataset/Megadepth_v1/MegaDepth_v1.tar.gz
python download_by_chunk/main.py --url=$url --dst=downloads/MegaDepth_v1.tar.gz
"""
import os
import asyncio
import concurrent.futures
import argparse
import requests


async def get_size(url: str):
    response = requests.head(url)
    size = int(response.headers['Content-Length'])
    return size


def download_range(url: str, start: int, end: int,output: str, chunk_size:int = 1024):
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers)
    with open(output, 'wb') as f:
        for part in response.iter_content(chunk_size):
            f.write(part)


async def download(executor, url, output, chunk_size=1000000):
    loop = asyncio.get_event_loop()

    file_size = await get_size(url)
    chunks = range(0, file_size, chunk_size)

    tasks = [
        loop.run_in_executor(
            executor,
            download_range,
            url,
            start,
            start + chunk_size - 1,
            f'{output}.part{i}',
        )
        for i, start in enumerate(chunks) if not os.path.exists(f'{output}.part{i}')
    ]

    await asyncio.wait(tasks)

    with open(output, 'wb') as o:
        for i in range(len(chunks)):
            chunk_path = f'{output}.part{i}'
            with open(chunk_path, 'rb') as s:
                o.write(s.read())
            os.remove(chunk_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url of download link", type=str)
    parser.add_argument("--dst", help="dst of download link", type=str)
    parser.add_argument("--worker", help="number of worker", type=int, default=3)
    args = parser.parse_args()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=args.worker)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(
            download(executor, args.url, args.dst)
        )
    finally:
        loop.close()