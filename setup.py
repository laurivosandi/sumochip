#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

setup(
    name = "sumochip",
    version = "1.1.1",
    author = u"Lauri Võsandi",
    author_email = "lauri.vosandi@gmail.com",
    description = "SumoCHIP is an extremely low-budget robotics platform based on CHIP single-board computer",
    license = "MIT",
    keywords = "sumorobot robot nextthingco getchip allwinner arm python flask",
    url = "http://github.com/laurivosandi/sumochip",
    packages=[
        "sumochip",
    ],
    long_description="SumoCHIP is an extremely low-budget robotics platform based on CHIP single-board computer",
    install_requires=[
        "axp209",
        "chip-io",
        "flask",
        "flask-sockets"
    ],
    include_package_data = True,
    entry_points={'console_scripts': ['sumochip_web = sumochip.webapp:main', 'sumochip_test = sumochip.sumorobot:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 2.7",
    ],
    data_files=[
        ("lib/systemd/system", ["sumochip.service"])
    ]
)
