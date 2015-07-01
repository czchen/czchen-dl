#!/usr/bin/env python3
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


import os

from distutils.core import setup
from pip.req import parse_requirements

def main():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()

    install_reqs = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))

    setup(
        name='khinsider-dl',
        version='0.0.0',
        author='ChangZhuo Chen (陳昌倬)',
        author_email='czchen@gmail.com',
        url='https://github.com/czchen/khinsider-dl.git',
        description='KHInsider Downloader',
        long_description=long_description,
        packages = [
            'khinsiderdl'
        ],
        install_reqs=install_reqs,
        entry_points={
            'console_scripts': [
                'khinsider-dl = khinsiderdl.console:main',
            ],
        },
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'License :: OST Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.4',
        ]
    )

if __name__ == '__main__':
    main()
