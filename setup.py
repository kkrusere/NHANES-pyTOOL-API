from setuptools import setup, find_packages

setup(
    name="NHANES-DATA-API",
    version="0.1.0",
    author="Kuzi Rusere",
    author_email="kkrusere@gmail.com",
    description="A tool for programmatic access to NHANES downloadable datasets",
    long_description="See README.md for details",
    url="https://github.com/kkrusere/NHANES-Data-API",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy",
        "pandas",
    ],
    package_data={'': ['*.md']},  # Include all .md files
    extras_require={
        'test': ['pytest']
    },
    project_urls={
        "Documentation": "https://github.com/kkrusere/NHANES-Data-API/blob/main/docs/index.md",
        "Bug Tracker": "https://github.com/kkrusere/NHANES-Data-API/blob/main/issues/NHANE-DATA-API_issues.md",
    },
)
