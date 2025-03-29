from setuptools import setup, find_packages

setup(
    name="algorithm_animation",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "manim>=0.18.0",
        "numpy",
    ],
)