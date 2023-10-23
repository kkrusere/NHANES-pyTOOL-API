from setuptools import setup, find_packages

# Read the long description from a file (if available)
with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="nhanes_pytool_api",
    version="0.1.1",
    author="Kuzi Rusere",
    author_email="kkrusere@gmail.com",
    description="A tool for programmatic access to NHANES downloadable datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkrusere/NHANES-pyTOOL-API",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
    ],
    extras_require={
        'test': ['pytest']
    },
        project_urls={
        "Documentation": "https://kkrusere.github.io/NHANES-pyTOOL-API/",
        "Bug Tracker": "https://github.com/kkrusere/NHANES-pyTOOL-API/issues"
    }
)
