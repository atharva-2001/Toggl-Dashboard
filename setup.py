import pathlib
from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# This call to setup() does all the work
setup(
    name="toggldash",
    version="1.0.0",
    description="plots data from toggl track",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atharva-2001/Toggl-Dashboard",
    author="Atharva Arya",
    author_email="aryaatharva18@gmail.com",
    license="MIT",
    python_requires='>=3.7',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["dash", "plotly", "pandas", "numpy", "requests"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)