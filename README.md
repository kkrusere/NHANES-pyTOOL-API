# NHANES Data API

The NHANES Data API is a Python library that provides a convenient interface for accessing and analyzing data from the National Health and Nutrition Examination Survey (NHANES). NHANES is a program of studies designed to assess the health and nutritional status of adults and children in the United States. This API allows researchers and developers to explore NHANES data efficiently, enabling a wide range of health-related analyses and applications.

## Features

- Retrieve data for specific data categories, cycle years, and data file descriptions.
- Find common and uncommon variables across multiple cycle years for a specific data category.
- Join data files from different data categories based on a common variable.
- List available data categories and cycle years.
- Explore unique data file descriptions for a specific data category and cycle years.

## Installation

To install the NHANES Data API, use `pip`:

```bash
pip install nhanes-data-api
```

## Getting Started

```python
from nhanes_data_api import NHANESDataAPI

# Initialize the NHANES Data API
api = NHANESDataAPI()

# Example usage
data_categories = api.list_data_categories()
cycle_years = api.list_cycle_years()
# ... (see documentation for more examples)

```

## Documentation

For detailed information on how to use the NHANES Data API, check out the official documentation.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.