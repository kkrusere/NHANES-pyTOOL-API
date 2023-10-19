from setuptools import setup, find_packages

setup(
    name="NHANES-DATA-API",
    version="0.1.0",
    author="Kuzi Rusere",
    author_email="kkrusere@gmail.com",
    description="A tool for programmatic access to NHANES downloadable datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kkrusere/NHANES-Data-API",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy==1.26.0",
        "pandas==2.1.1"
    ],
)
