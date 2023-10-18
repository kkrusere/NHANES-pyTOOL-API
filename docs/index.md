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
```
### 2.2 Quick Start <a name="quick-start"></a>
You can get started quickly with the NHANES Data API by following these steps:

```python

from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI object
nhanes_api = NHANESDataAPI()

# Explore NHANES data
# ...

```

### 3. API Reference <a name="api-reference"></a>

### 3.1 NHANESDataAPI Class <a name="nhanesdataapi-class"></a>

#### 3.1.1 Initialization <a name="initialization"></a>

##### `NHANESDataAPI(data_directory="data/")`
Initialize the NHANESDataAPI.

- `data_directory` (str, optional): Directory where data will be stored (default is "data/").

> **Note:** The initialization of the `NHANESDataAPI` class with `data_directory` is not necessary for users to start utilizing the tool. You can directly create an instance of the class as shown in the [Quick Start](#quick-start) section.


#### 3.1.2 List Data Categories <a name="list-data-categories"></a>

##### `list_data_categories()`
List the available NHANES data categories.

**Returns:**
- List of available data categories.

#### 3.1.3 List Cycle Years <a name="list-cycle-years"></a>

##### `list_cycle_years()`
List the available NHANES cycle years.

**Returns:**
- List of available cycle years.

#### 3.1.4 List File Names <a name="list-file-names"></a>

##### `list_file_names(data_category, cycle_years=None)`
Get a list of unique values in the 'Data File Description' column for a specific data category and optional cycle years.

- `data_category` (str): The data category for which you want to retrieve unique data file descriptions.
- `cycle_years` (str or list of str, optional): The specific year-cycles to filter the variable table. If not specified, all available cycles are considered.

**Returns:**
- List of unique data file descriptions for the specified data category and cycle years.

**Raises:**
- Exception: If there is an error fetching the variable table, if no data is available, or if the data category is not recognized.

#### 3.1.5 Retrieve Cycle Data File Name Mapping <a name="retrieve-cycle-data-file-name-mapping"></a>

##### `retrieve_cycle_data_file_name_mapping(data_category, file_name)`
Retrieve a dictionary of years and Data File Names based on a given "Data File Description."

- `data_category` (str): The data category to filter the variable table.
- `file_name` (str): The "Data File Description" to filter the variable table.

**Returns:**
- Dictionary mapping years to Data File Names.

**Raises:**
- ValueError: If no data matches the provided "Data File Description."

#### 3.1.6 Get Common and Uncommon Variables <a name="get-common-and-uncommon-variables"></a>

##### `get_common_and_uncommon_variables(data_category, cycle_years)`

Find common and uncommon variables across multiple cycle years for a specific data category.

- `data_category` (str): The data category for which data is requested.
- `cycle_years` (str or list of str): Either a single cycle year or a list of cycle years.

**Returns:**
- List of common variables found across the specified cycle years.
- List of uncommon variables not found in all of the specified cycle years.
- Dictionary of {variable (Variable Description): [cycles]} showing which cycles each variable appears in.

**Raises:**
- ValueError: If the specified cycle years are invalid or if there is only one cycle specified.

#### 3.1.7 Retrieve Data <a name="retrieve-data"></a>

##### `retrieve_data(data_category, cycle, filename, include_uncommon_variables=True, specific_variables=None)`

Retrieve data for a specific data category, cycle year(s), and data file description.

- `data_category` (str): The data category for which data is requested.
- `cycle` (str): The cycle year for which data is requested.
- `filename` (str): The specific "Data File Description" for the requested data file.
- `include_uncommon_variables` (bool, optional): Whether to include uncommon variables when joining data files (default is `True`).
- `specific_variables` (list of str, optional): List of specific variables to retrieve. If not specified, all variables are retrieved.

**Returns:**
- Pandas DataFrame containing the requested data.

**Raises:**
- ValueError: If the specified data category, cycle, or filename is invalid, or if no data matches the provided criteria.

#### 3.1.8 Join Data Files <a name="join-data-files"></a>

##### `join_data_files(cycle_year, data_category1, file_name1, data_category2, file_name2, include_uncommon_variables=True)`

Join two data files from specified data categories and file names based on the common variable SEQN.

- `cycle_year` (str): The cycle year to retrieve data for both data categories.
- `data_category1` (str): The first data category.
- `file_name1` (str): The "Data File Description" for the first data category.
- `data_category2` (str): The second data category.
- `file_name2` (str): The "Data File Description" for the second data category.
- `include_uncommon_variables` (bool, optional): Whether to include uncommon variables when joining data files (default is `True`).


### 3.2 Examples <a name="examples"></a>

#### 3.2.1 List Data Categories and Cycle Years <a name="list-data-categories-and-cycle-years"></a>

```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
api = NHANESDataAPI()

# List available data categories
data_categories = api.list_data_categories()
print("Data Categories:", data_categories)

# List available cycle years
cycle_years = api.list_cycle_years()
print("Cycle Years:", cycle_years)
```

#### 3.2.2 List File Names <a name="list-file-names-example"></a>

```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
api = NHANESDataAPI()

# Specify the data category and cycle years (optional)
data_category = "examination"
cycle_years = ["2005-2006", "2007-2008"]

# List unique data file descriptions
file_names = api.list_file_names(data_category, cycle_years)
print("Unique Data File Descriptions:", file_names)


```