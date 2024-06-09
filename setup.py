#!/usr/bin/env python3

import os

from setuptools import setup, find_packages

required_dirs = [
    "data_files",
    "data_files/big_buy",
    "data_files/input_data",
    "data_files/output_data",
    "data_files/vida_xl",
]

for dir_path in required_dirs:
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="ecom_automation",
    version="0.0.1",
    packages=find_packages(),
    python_requires=">=3.12, <4",
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
