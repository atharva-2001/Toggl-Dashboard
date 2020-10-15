import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="toggldash",
    version="1.0.0",
    description="plots data from toggl track",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bigpappathanos-web/Toggl-Dashboard",
    author="Atharva Arya",
    author_email="aryaatharva18@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["toggldash"],
    include_package_data=True,
    install_requires=["dash", "plotly", "plotly_express", "pandas", "numpy", "requests"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)