from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nhanes_data_api",
    version="0.1.0",
    author="Kuzi Rusere",
    author_email="kkrusere@gmail.com",
    description="A tool for programmatic access to NHANES downloadable datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkrusere/NHANES-Data-API",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
    ],
    extras_require={
        'test': ['pytest']
    },
)
