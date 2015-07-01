#!/usr/bin/env python3

import os
from distutils.core import setup

def main():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()

    setup(
        name='khinsider-dl',
        version='0.0.0',
        author='ChangZhuo Chen (陳昌倬)',
        author_email='czchen@gmail.com',
        url='https://github.com/czchen/khinsider-dl.git',
        description='KHInsider Downloader',
        long_description=long_description,
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'License :: OST Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.3',
        ]
    )

if __name__ == '__main__':
    main()
