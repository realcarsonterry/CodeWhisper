"""Setup script for No Chat Bot."""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="nochatbot",
    version="0.1.0",
    description="AI-powered codebase analysis and recommendation tool",
    author="Terry",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'nochatbot=nochatbot.cli:cli',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
