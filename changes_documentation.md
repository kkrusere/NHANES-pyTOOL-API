# Changes Documentation 

## NHANES pyTOOL API for Version 0.1.0 to 0.1.1

### Class: NHANESDataAPI

### Added Features:
- **Private Class Attributes:** Made `cycle_list` and `data_category_list` private class attributes by adding double underscores before their names. This ensures they are only accessible within the class.

### Modified Methods:
- **`list_file_names(data_category, cycle_years=None)` Method:** Updated the method to handle private class attributes by using the double underscores before `cycle_list` and `data_category_list` names within the class.

### New Methods:

- **`_check_cycle(input_cycle)` and `_check_in_between_cycle(start_year, end_year)` Private Methods:** Added private methods to check the validity of input cycle years and return valid cycles based on input. These methods handle single cycle years, lists of single cycle years, cycle ranges, and lists of cycle ranges as acceptable input formats.

- **`_get_data_filename(data_category, cycle_year, data_file_description)` Private Method:** Added a private method to get the data file name for a specific cycle year and data file description. It handles private class attributes by using the double underscores before `cycle_list` and `data_category_list` names within the class.

### Updated Documentation:
- **Class Description:** Added detailed class description including constructor information, available attributes, and methods with their descriptions.

- **Method Descriptions:** Updated method descriptions to provide clear explanations of the functionality, parameters, and return values of each method.

- **Exception Handling:** Documented exceptions raised in methods and provided explanations for possible errors.

- **Input Formats:** Explained acceptable input formats for methods that require cycle years input, making it clearer for users how to provide valid input.

- **GitHub Integration:** Provided instructions on how to create a GitHub repository, clone it, add a documentation file (`changes_documentation.md`), and push changes to GitHub.

These changes enhance the functionality of the `NHANESDataAPI` class, improve code organization, and provide comprehensive documentation for users. Users can now easily understand the class's purpose, available methods, and how to interact with the API effectively.
