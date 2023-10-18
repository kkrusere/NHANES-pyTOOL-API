# NHANES Data API Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Quick Start](#quick-start)
3. [API Reference](#api-reference)
   - [NHANESDataAPI Class](#nhanesdataapi-class)
      - [Initialization](#initialization)
      - [List Data Categories](#list-data-categories)
      - [List Cycle Years](#list-cycle-years)
      - [List File Names](#list-file-names)
      - [Retrieve Cycle Data File Name Mapping](#retrieve-cycle-data-file-name-mapping)
      - [Get Common and Uncommon Variables](#get-common-and-uncommon-variables)
      - [Retrieve Data](#retrieve-data)
      - [Join Data Files](#join-data-files)
4. [Examples](#examples)
   - [List Data Categories](#list-data-categories-example)
   - [List Cycle Years](#list-cycle-years-example)
   - [Retrieve Data](#retrieve-data-example)
   - [Join Data Files](#join-data-files-example)
5. [Unit Tests](#unit-tests)
6. [Contributing](#contributing)
7. [License](#license)

## 1. Introduction <a name="introduction"></a>
The NHANES Data 'API' is a Python library designed to simplify the process of accessing and analyzing data from the National Health and Nutrition Examination Survey (NHANES). NHANES is a program of studies conducted by the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC), to assess the health and nutritional status of adults and children in the United States.

This 'API' provides an easy-to-use interface for retrieving NHANES datasets, allowing researchers, data science professionals, health professionals, developers and other stakeholders to explore NHANES data efficiently, enabling a wide range of health-related analyses and applications.


## 2. Getting Started <a name="getting-started"></a>

### 2.1 Installation <a name="installation"></a>
To install the NHANES Data API, you can use pip:

```bash
pip install NHANES-Data-API
