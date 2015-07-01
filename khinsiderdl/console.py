#!/usr/bin/env python3
import argparse

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
        default='output',
        type=str,
        nargs=1,
        help='Output directory')

    return parser.parse_args()

def main():
    args = get_args()

    return 0
