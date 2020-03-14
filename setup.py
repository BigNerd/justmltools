import setuptools
from version import get_version


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="justmltools",
    version=get_version(),
    author="Matthias Burbach",
    author_email="matthias.burbach@web.de",
    description="A library for recurring tasks in machine learning projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BigNerd/justmltools",
    packages=setuptools.find_packages(include=("justmltools", "justmltools.*")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
