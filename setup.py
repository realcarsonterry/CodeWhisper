"""Setup script for CodeWhisper."""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="codewhisper",
    version="0.2.0",
    description="Zero-barrier AI assistant for intelligent codebase understanding",
    author="Terry",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'codewhisper=codewhisper.cli:cli',
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
