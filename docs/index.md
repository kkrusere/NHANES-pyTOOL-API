## NHANES Data API Documentation

[GitHub](https://github.com/kkrusere/NHANES-pyTOOL-API) | [PyPI](https://pypi.org/project/nhanes-pytool-api/)

**Attention:** Please take a look at the [Disclaimer](#disclaimer) before using the tool

### Table of Contents
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
The NHANES pyTOOL 'API' is a Python library designed to simplify the process of accessing and analyzing data from the National Health and Nutrition Examination Survey (NHANES). NHANES is a program of studies conducted by the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC), to assess the health and nutritional status of adults and children in the United States.

This tool provides an easy-to-use interface for retrieving NHANES datasets, allowing researchers, data science professionals, health professionals, developers and other stakeholders to explore NHANES data efficiently, enabling a wide range of health-related analyses and applications.


## 2. Getting Started <a name="getting-started"></a>

### 2.1 Installation <a name="installation"></a>
To install the NHANES pyTOOL API, you can use pip:

```bash
pip install nhanes_pytool_api
```
### 2.2 Quick Start <a name="quick-start"></a>
You can get started quickly with the NHANES Data API by following these steps:

```python

from nhanes_data.nhanes_data_api import NHANESDataAPI

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
from nhanes_data.nhanes_data_api import NHANESDataAPI

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
from nhanes_data.nhanes_data_api import NHANESDataAPI

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
from nhanes_data.nhanes_data_api import NHANESDataAPI

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
from nhanes_data.nhanes_data_api import NHANESDataAPI

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
from nhanes_data.nhanes_data_api import NHANESDataAPI

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
from nhanes_data.nhanes_data_api import NHANESDataAPI

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

For more details on how to use the NHANES Data API, please refer to the official API documentation on our GitHub repository: API [Documentation](https://kkrusere.github.io/NHANES-pyTOOL-API/).

For reporting issues or requesting new features, please visit our [Bug Tracker](https://github.com/kkrusere/NHANES-pyTOOL-API/blob/main/issues/NHANE-pyTOOL-API_issues.md).

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/kkrusere/NHANES-pyTOOL-API/blob/main/LICENSE.txt) file for details.


## GitHub Issue

If you encounter any issues, bugs, or have suggestions for improvements, please use our [GitHub Issue](https://github.com/kkrusere/NHANES-pyTOOL-API/issues). Our development team actively monitors this repository, and this is the recommended way to report problems or suggest enhancements. To help us address your issue effectively, please follow these guidelines:

1. **Search Existing Issues:** Before creating a new issue, please search the existing issues to check if someone has already reported a similar problem or request. If you find a related issue, you can contribute to the existing discussion.

2. **Provide Details:** When reporting a bug, provide as much detail as possible about the problem you encountered. Include information about your environment, code, and any error messages you received. For feature requests, explain your use case and how the proposed feature would benefit the project.

3. **Be Respectful:** Remember to be respectful and constructive in your interactions with other contributors. A positive and collaborative environment helps improve the project for everyone.

4. **Use Labels:** Our issue tracker uses labels to categorize and prioritize issues. These labels help us identify the nature of each issue. You can use labels such as "bug," "enhancement," or "question" to classify your issue.

Our team will review and respond to issues as soon as possible. Thank you for your contributions and feedback!

[**GitHub Issue**](https://github.com/kkrusere/NHANES-pyTOOL-API/issues)




## Disclaimer <a name="disclaimer"></a>

**Current Limitation**

The NHANES pyTOOL API is designed to work exclusively with NHANES data from pre-pandemic cycle years (1999-2000 to 2017-2018). Please note that the tool does not currently support NHANES data from the COVID-19 pandemic and post-pandemic eras.

**Reasoning**

The COVID-19 pandemic has had a significant impact on NHANES data collection. 

**NHANES data collection during the COVID-19 pandemic**

In March 2020, the NHANES program suspended field operations due to the COVID-19 pandemic. This meant that data collection for the 2019-2020 cycle was not completed. As a result, data collected from 2019 to March 2020 were combined with data from the 2017-2018 cycle to form a nationally representative sample of NHANES 2017-March 2020 pre-pandemic data.

Data collection for the 2019-2022 cycle resumed in September 2020, but with some modifications to reduce the risk of COVID-19 transmission. These modifications included:

* Reducing the number of participants recruited from each location.
* Implementing additional safety protocols at the MEC, such as requiring masks and social distancing.
* Offering participants the option to complete the interview and physical examination remotely.

**Impact of the COVID-19 pandemic on NHANES data**

The COVID-19 pandemic has had a number of impacts on NHANES data, including:

* **Reduced sample size:** The sample size for the 2019-2022 cycle is smaller than the sample size for previous cycles. This is due to the suspension of field operations in 2020 and the modifications implemented to reduce the risk of COVID-19 transmission.
* **Increased variability:** The variability of NHANES estimates may be higher for the 2019-2022 cycle and future cycles due to the smaller sample size and the modifications to data collection procedures.
* **Data gaps:** There are some data gaps for the 2019-2020 cycle, such as data on COVID-19 infection and vaccination status. These data gaps will be filled as data from the 2019-2022 cycle and future cycles is released.


These changes to NHANES data collection make it more difficult to develop and maintain a tool that can reliably work with data from both the pre-pandemic and pandemic eras. For this reason, we have decided to focus on supporting NHANES data from the pre-pandemic cycle years in the first version of the NHANES pyTOOL API.


**Future Plans**

We are committed to making the NHANES pyTOOL API the most comprehensive and user-friendly tool for working with NHANES data. To this end, we plan to add support for NHANES data from the COVID-19 pandemic and post-pandemic eras in future versions of the tool. We will also continue to monitor the NHANES data collection process and make updates to the tool as needed.

**Downloading Data**

If you require NHANES data from during the COVID-19 pandemic and post-pandemic eras (2019-2020 +), you can manually download it from the NHANES webpage. Visit the following link: [NHANES Data Download](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx).

**More Information**

For additional information about NHANES, please visit the official NHANES website: [NHANES Information](https://www.cdc.gov/nchs/nhanes/index.htm).

**User Support**

If you have questions or need support related to the NHANES pyTOOL API, please feel free to contact us.

**Legal Notices**

Before using NHANES data, please ensure that you comply with all legal and usage restrictions associated with NHANES datasets. Please be aware of your responsibilities regarding data usage and distribution.

We apologize for any inconvenience this may cause, and we appreciate your understanding.

