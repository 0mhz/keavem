from setuptools import find_packages, setup

setup(
    name="keavem",
    version="0.0.1",
    packages=find_packages(exclude=["test/*"]),
    install_requires=["x690"],
)
