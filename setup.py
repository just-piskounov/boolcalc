from setuptools import setup

setup(
    name="boolcalc",
    version="1.0.0",
    packages=["boolcalc"],
    package_dir={"": "src"},
    install_requires=["textual>=0.34.0"],
)
