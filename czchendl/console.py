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
import logging.config
import os
import re

import aiohttp
import yaml


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

    parser.add_argument('--config', '-c',
                        metavar='config',
                        type=str,
                        nargs='?',
                        help='configuration')

    return parser.parse_args()


@asyncio.coroutine
def find_all_match_in_page(*, url, pattern):
    logging.debug('Find pattern {pattern} in {url}'.format(
        url=url, pattern=pattern))

    try:
        rsp = yield from aiohttp.request('GET', url)
        if rsp.status != http.client.OK:
            logging.warning('Cannot GET {url} for pattern {pattern}, status is {status}'.format(
                url=url,
                pattern=pattern,
                status=rsp.status))
            return iter([])

        body = (yield from rsp.read()).decode('UTF-8')

    except Exception:
        logging.exception('Cannot GET {url} for pattern {pattern}'.format(
            url=url,
            pattern=pattern))
        return iter([])

    return re.findall(pattern, body)


@asyncio.coroutine
def download_single_song(*, output_dir, song_url, semaphore):
    try:
        with (yield from semaphore):
            rsp = yield from aiohttp.request('GET', song_url)
        if rsp.status != http.client.OK:
            logging.warning('Cannot GET {song_url}, status is {status}'.format(
                song_url=song_url,
                status=rsp.status))
            return

        body = yield from rsp.read()

    except Exception:
        logging.exception('Cannot retrive song information from {song_url}'.format(
            song_url=song_url))
        return

    match = re.search('href="(?P<song>.*\.mp3)"', body.decode('UTF-8'))
    if match is None:
        logging.warning('Cannot find download link in {song_url}'.format(
            song_url=song_url))
        return

    song = match.group('song')

    try:
        with (yield from semaphore):
            rsp = yield from aiohttp.request('GET', song)
        if rsp.status != http.client.OK:
            logging.warning('Cannot GET {song}, status is {status}'.format(
                song=song,
                status=rsp.status))
            return

        body = yield from rsp.read()

        song_name = os.path.join(output_dir, song.split('/')[-1])

        with open(song_name, 'wb') as f:
            logging.debug('song_name = {song_name}'.format(
                song_name=song_name))
            f.write(body)

    except Exception:
        logging.exception('Cannot retrive song from {song}'.format(
            song=song))
        return


@asyncio.coroutine
def download_single_album(*, output_dir, album_url, semaphore):
    logging.debug('output_dir = {output_dir}, album_url = {album_url}'.format(
        output_dir=output_dir,
        album_url=album_url))

    album_name = album_url.split('/')[-1]

    album_dir = os.path.join(output_dir, album_name)
    os.makedirs(album_dir, exist_ok=True)

    urls = yield from find_all_match_in_page(url=album_url, pattern='href="(.*\.mp3)"')

    tasks = []
    for url in set(urls):
        task = asyncio.ensure_future(
            download_single_song(output_dir=album_dir,
                                 song_url=url,
                                 semaphore=semaphore))
        tasks.append(task)

    yield from asyncio.wait(tasks)


def get_config(args):
    config = {}

    if args.config:
        with open(args.config, 'r') as f:
            config.update(yaml.load(f.read()))

    return config


@asyncio.coroutine
def run():
    args = get_args()
    config = get_config(args)
    logging.config.dictConfig(config['logging'])

    semaphore = asyncio.Semaphore(config['general']['maximum_concurrent_download'])

    output_dir = args.output[0]

    os.makedirs(output_dir, exist_ok=True)
    logging.debug('output_dir = {}'.format(output_dir))

    tasks = []

    for url in args.url:
        task = asyncio.ensure_future(
            download_single_album(output_dir=output_dir,
                                  album_url=url,
                                  semaphore=semaphore))
        tasks.append(task)

    yield from asyncio.wait(tasks)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

    return 0
