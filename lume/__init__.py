import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

with open(f"{ROOT_PATH}/VERSION", "r") as f:
    __version__ = f.read().rstrip()
