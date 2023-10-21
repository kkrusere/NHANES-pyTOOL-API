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
   - [List Operations](#list-operations)
      - [List Data Categories and Cycle Years](#list-data-categories-and-cycle-years)
      - [List File Names](#list-file-names-example)
   - [Data Retrieval](#data-retrieval)
      - [Retrieve Cycle Data File Name Mapping](#retrieve-cycle-data-file-name-mapping-example)
      - [Get Common and Uncommon Variables](#get-common-and-uncommon-variables-example)
      - [Retrieve Data](#retrieve-data-example)
      - [Join Data Files](#join-data-files-example)
5. [Troubleshooting](#troubleshooting)
   - [Error Handling](#error-handling)
   - [Error Messages](#error-messages)

## 1. Introduction <a name="introduction"></a>
The NHANES Data 'API' is a Python library designed to simplify the process of accessing and analyzing data from the National Health and Nutrition Examination Survey (NHANES). NHANES is a program of studies conducted by the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC), to assess the health and nutritional status of adults and children in the United States.

This 'API' provides an easy-to-use interface for retrieving NHANES datasets, allowing researchers, data science professionals, health professionals, developers and other stakeholders to explore NHANES data efficiently, enabling a wide range of health-related analyses and applications.


## 2. Getting Started <a name="getting-started"></a>

### 2.1 Installation <a name="installation"></a>
To install the NHANES Data API, you can use pip:

```bash
pip install nhanes_data_api
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


### 4. Examples <a name="examples"></a>

### 4.1 List Operations <a name="list-operations"></a>

#### 4.1.1 List Data Categories and Cycle Years <a name="list-data-categories-and-cycle-years"></a>

```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
nhanes_api = NHANESDataAPI()

# List available data categories
data_categories = api.list_data_categories()
print("Data Categories:", data_categories)

# List available cycle years
cycle_years = nhanes_api.list_cycle_years()
print("Cycle Years:", cycle_years)
```

#### 4.1.2 List File Names <a name="list-file-names-example"></a>

```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
nhanes_api = NHANESDataAPI()

# Specify the data category and cycle years (optional)
data_category = "examination"
cycle_years = ["2005-2006", "2007-2008"]

# List unique data file descriptions
file_names = nhanes_api.list_file_names(data_category, cycle_years)
print("Unique Data File Descriptions:", file_names)
```

### 4.2 Data Retrieval <a name="data-retrieval"></a>

#### 4.2.1 Retrieve Cycle Data File Name Mapping <a name="retrieve-cycle-data-file-name-mapping-example"></a>

```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
nhanes_api = NHANESDataAPI()

# Specify the data category and file name
data_category = "examination"
file_name = "Body Measures"

# Retrieve a dictionary of years and Data File Names
file_name_mapping = nhanes_api.retrieve_cycle_data_file_name_mapping(data_category, file_name)
print("Cycle Data File Name Mapping:", file_name_mapping)

```

#### 4.2.2 Get Common and Uncommon Variables <a name="get-common-and-uncommon-variables-example"></a>
```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
nhanes_api = NHANESDataAPI()

# Specify the data category and cycle years
data_category = "examination"
cycle_years = ["2005-2006", "2007-2008"]

# Find common and uncommon variables
common_variables, uncommon_variables, variable_cycles_dict = nhanes_api.get_common_and_uncommon_variables(data_category, cycle_years)
print("Common Variables:", common_variables)
print("Uncommon Variables:", uncommon_variables)
print("Variable Cycles Dictionary:", variable_cycles_dict)

```

#### 4.2.3 Retrieve Data <a name="retrieve-data-example"></a>

```python 
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
nhanes_api = NHANESDataAPI()

# Specify the data category, cycle year, and data file description
data_category = "examination"
cycle = "2005-2006"
file_name = "Body Measures"

# Retrieve data
data = nhanes_api.retrieve_data(data_category, cycle, file_name)
print("Retrieved Data:")
print(data.head())

```

#### 4.2.4 Join Data Files <a name="join-data-files-example"></a>
```python
from NHANES_data_API import NHANESDataAPI

# Initialize the NHANESDataAPI
nhanes_api = NHANESDataAPI()

# Specify the cycle year, data categories, and file names
cycle_year = "2005-2006"
data_category1 = "examination"
file_name1 = "Body Measures"
data_category2 = "demographics"
file_name2 = "Demographic Variables & Sample Weights"

# Join data files
joined_data = nhanes_api.join_data_files(cycle_year, data_category1, file_name1, data_category2, file_name2)
print("Joined Data:")
print(joined_data.head())

```


### 5. Troubleshooting <a name="troubleshooting"></a>

#### 5.1 Handling Errors <a name="error-handling"></a>

The NHANES Data API includes error handling to manage various issues that might arise during usage. Below are some common error scenarios and how they are handled:

- **Data Category Not Found:** If you specify an invalid or unrecognized data category, the API will raise an exception indicating that the data category is not recognized.

- **Invalid Cycle Year:** If you provide an invalid cycle year or range of years, the API will raise a ValueError, indicating that the cycle is invalid. It will also suggest valid cycle years for your reference.

- **Data File Not Found:** If you request data from a specific data file description that is not available for a given data category and cycle year, the API will raise a ValueError. It will inform you that the data file name is not available in the specified cycle year and data category.

- **No Data Available:** If there is no data available for the specified data category, cycle year, and file name, the API will raise a ValueError indicating that no data is available for the provided criteria.

- **Variable Table Format Change:** If the structure of the variable table on the NHANES website changes, the API may raise an exception. You will need to update the code to match the new format.

#### 5.2 Error Messages <a name="error-messages"></a>

Here are some common error messages you may encounter when using the NHANES Data API:

- "Data category not recognized. Please provide a valid data category."

- "Invalid cycle year. Please provide a valid cycle year."

- "Data file name not available in the specified cycle year and data category."

- "No data available for the specified criteria."

- "Error fetching variable table from the NHANES website."

- "The structure of the variable table has changed. Please update the code accordingly."


# Important Note

**Attention:** In the current version of the NHANES Data API (version 0.1.0), we do not provide a command-line interface (CLI) for direct use from the terminal. This means that you cannot run the API from the command line to access NHANES data. Instead, the API is designed for use as a library in Python scripts or applications.
###### Future Updates - We are continuously improving the NHANES Data API, and in future versions, we may consider adding a command-line interface for easier interaction with the API from the terminal. Until then, please use the API in your Python scripts or applications.


## Additional Resources

For more details on how to use the NHANES Data API, please refer to the official API documentation on our GitHub repository: API [Documentation](https://github.com/kkrusere/NHANES-Data-API/blob/main/docs/index.md).

For reporting issues or requesting new features, please visit our [Bug Tracker](https://github.com/kkrusere/NHANES-Data-API/blob/main/issues/NHANE-DATA-API_issues.md).

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/kkrusere/NHANES-Data-API/blob/main/LICENSE) file for details.

