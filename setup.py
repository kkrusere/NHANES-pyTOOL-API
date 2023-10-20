from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NHANES-DATA-API",
    version="0.1.2",
    author="Kuzi Rusere",
    author_email="kkrusere@gmail.com",
    description="A tool for programmatic access to NHANES downloadable datasets",
    long_description=long_description,  # Use the content of README.md
    long_description_content_type="text/markdown",  # Specify the content type
    url="https://github.com/kkrusere/NHANES-Data-API",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
    ],
    extras_require={
        'test': ['pytest']
    },
    project_urls={
        "Documentation": "https://github.com/kkrusere/NHANES-Data-API/blob/main/docs/index.md",
        "Bug Tracker": "https://github.com/kkrusere/NHANES-Data-API/blob/main/issues/NHANE-DATA-API_issues.md",
    },
)
