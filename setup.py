from setuptools import setup, find_packages

setup(
    name="cybershoke",
    version="0.1.5",
    description="",
    author="marklanselot",
    author_email="markrybitskij@gmail.com",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.11.11",
        "Brotli==1.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.1',
)