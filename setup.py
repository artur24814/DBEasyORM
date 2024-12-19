from setuptools import setup, find_packages

with open("README-PYPI.md", "r") as f:
    long_description = f.read()

setup(
    name="dbeasyorm",
    version="0.0.0",
    author="artur24814",
    author_email="artur24814@gmail.com",
    description="DBEasyORM is a lightweight and intuitive Object-Relational Mapping (ORM) library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artur24814/DBEasyORM",
    packages=find_packages(exclude=["docs", "tests", "app", ".github", "env"]),
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["colorama >= 0.4.6"],
    extras_require={
        "dev": ["pytest>=8.3.4", "twine>=6.0.1"]
    },
    python_requires='>=3.8',
    project_urls={
        "Documentation": "https://dbeasyorm.readthedocs.io",
        "Source": "https://github.com/artur24814/DBEasyORM",
        "Bug Tracker": "https://github.com/artur24814/DBEasyORM/issues",
    },
)
