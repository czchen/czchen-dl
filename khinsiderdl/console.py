#!/usr/bin/env python3
# coding=UTF-8
#
# Copyright (c) 2015 ChangZhuo Chen (陳昌倬) <czchen@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import asyncio
import http.client
import logging
import os
import re

import aiohttp


def get_args():
    parser = argparse.ArgumentParser(
        description='KHInsider Downloader'
    )

    parser.add_argument('url',
                        metavar='url',
                        type=str,
                        nargs='+',
                        help='URL to download')

    parser.add_argument('--output', '-o',
                        metavar='output',
                        default=['output'],
                        type=str,
                        nargs=1,
                        help='Output directory')

    return parser.parse_args()


@asyncio.coroutine
def download_single_song(*, output_dir, song_url):
    print('song_url = ' + song_url)


@asyncio.coroutine
def download_single_album(*, output_dir, album_url):
    try:
        album_name = album_url[album_url.rfind('/') + 1:]
        album_dir = os.path.join(output_dir, album_url)

        rsp = yield from aiohttp.request('GET', album_url)

        if rsp.status != http.client.OK:
            logging.warning('Cannot GET {album_url}, status is {status}'.format(
                album_url=album_url,
                status=rsp.status))
            return

        body = yield from rsp.read()

    except Exception:
        logging.exception('Cannot retrive information from {album_url}'.format(
            album_url=album_url))
        return

    os.makedirs(album_dir, exist_ok=True)

    tasks = []

    for url in set(re.findall('href="(.*\.mp3)"', body.decode('UTF-8'))):
        task = asyncio.ensure_future(
            download_single_song(output_dir=album_dir,
                                 song_url=url))
        tasks.append(task)

    yield from asyncio.wait(tasks)


@asyncio.coroutine
def run():
    args = get_args()

    output_dir = args.output[0]

    os.makedirs(output_dir, exist_ok=True)
    logging.debug('output_dir is {}'.format(output_dir))

    tasks = []

    for url in args.url:
        task = asyncio.ensure_future(
            download_single_album(output_dir=output_dir,
                                  album_url=url))

        tasks.append(task)

    yield from asyncio.wait(tasks)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

    return 0
