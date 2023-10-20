"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="minitel",
    author="korfuri",
    author_email="korfuri@gmail.com",
    url="https://github.com/korfuri/asterisk-minitel",
    description="Python application layer for a minitel-over-VoIP setup",
    version="0.0.1",
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Environment :: Console",
        "Environment :: Other Environment",
    ],
    scripts=["minitel/main.py"],
)
