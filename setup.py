#!/usr/bin/env python3

import setuptools

def main():
    setuptools.setup(
        name='khinsider-dl',
        version='0.0.0',
        author='ChangZhuo Chen (陳昌倬)',
        author_email='czchen@gmail.com',
        url='https://github.com/czchen/khinsider-dl.git',
        description='KHInsider Downloader',
        long_description=read('README.rst'),
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
