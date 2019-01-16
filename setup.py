from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="noaareport",
    version="0.2",
    author="Edison Neto",
    author_email="ednetoali@gmail.com",
    description="A package to read noaa solar reports",
    long_description=long_description,
    url="https://github.com/3ldr0n/noaa-report",
    packages=['noaareport'],
    include_package_data=True,
    install_requires=[
        'pandas>=0.21'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
