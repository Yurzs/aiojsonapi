from setuptools import setup, find_packages


with open("README.rst") as description_file:
    setup(
        name="aiojson",
        version="0.1",
        description=description_file.read(),
        packages=find_packages(),
        url="https://git.yurzs.dev/yurzs/aiojson",
    )
