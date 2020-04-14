import os

import setuptools
from setuptools import setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "lume"
VERSION = open("lume/VERSION", "r").read()

# The text of the README file
with open(os.path.join(CURRENT_DIR, "README.md")) as fid:
    README = fid.read()

with open("requirements/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Lume",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["lume"],
    url="https://github.com/alice-biometrics/lume",
    author="ALiCE Biometrics",
    author_email="support@alicebiometrics.com",
    license="MIT",
    install_requires=required,
    entry_points={"console_scripts": ["lume = lume.src.application.cli.lume:main"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
)
