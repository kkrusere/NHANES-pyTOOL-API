import os
import pandas as pd

class NHANESDataAPI:
    """
    NHANESDataAPI provides an interface for accessing and manipulating data from the National Health and Nutrition Examination Survey (NHANES).

    The NHANES dataset consists of various data categories collected over multiple cycles. This API allows users to retrieve data by specifying data categories, cycle years, and data file descriptions, and perform common data operations.

    Args:
    data_directory (str, optional): The directory where data will be stored or retrieved. Defaults to 'data/'.

    Attributes:
    __cycle_list (list of str): A list of available NHANES cycle years.
    __data_category_list (list of str): A list of available NHANES data categories.

    Methods:
    - list_data_categories(): List the available NHANES data categories.
    - list_cycle_years(): List the available NHANES cycle years.
    - _retrieve_variable_table(data_category): Retrieve the variable table for a specific data category.
    - list_file_names(data_category, cycle_years=None): Get a list of unique values in the 'Data File Description' column for a specific data category and optional cycle years.
    - retrieve_cycle_data_file_name_mapping(variable_table, file_name): Retrieve a dictionary of years and Data File Names based on a given "Data File Description."
    - _check_cycle(input_cycle): Check the validity of a cycle and return valid cycle(s) based on input.
    - _check_in_between_cycle(start_year, end_year): Check for valid cycles within a range.
    - _get_data_filename(data_category, cycle_year, data_file_description): Get the data file name for a specific cycle year and data file description.
    - get_common_and_uncommon_variables(data_category, cycle_years): Find common and uncommon variables across multiple cycle years for a specific data category.
    - retrieve_data(data_category, cycle, filename, include_uncommon_variables=True): Retrieve data for a specific data category, cycle year(s), and data file description.
    - join_data_files(cycle_year, data_category1, file_name1, data_category2, file_name2, include_uncommon_variables=True): Join two data files from specified data categories and file names based on the common variable SEQN.

    """

    __cycle_list = [
        '1999-2000',
        '2001-2002',
        '2003-2004',
        '2005-2006',
        '2007-2008',
        '2009-2010',
        '2011-2012',
        '2013-2014',
        '2015-2016',
        '2017-2018'
    ]

    __data_category_list = [
        "demographics",
        "dietary",
        "examination",
        "laboratory",
        "questionnaire",
        "limitedaccess"
    ]

    def __init__(self, data_directory="data/"):
        """
        Initialize the NHANES Data API.

        Args:
        data_directory (str): Directory where data will be stored.
        """
        self.data_directory = data_directory

    def list_data_categories(self):
        """
        List the available NHANES data categories.

        Returns:
        list: List of available data categories.
        """
        return self.__data_category_list
    
    def list_cycle_years(self):
        """
        List the available NHANES cycle years.

        Returns:
        list: List of available cycle years.
        """
        return self.__cycle_list
    


    def _retrieve_variable_table(self, data_category):
        """
        Retrieve the variable table for a specific data category.

        Args:
        data_category (str): The data category for which you want the variable table.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the variable table or None if no table is found.

        Raises:
        Exception: If there is an error fetching the variable table or if the website's format has changed.
        """
        url = f"https://wwwn.cdc.gov/nchs/nhanes/search/variablelist.aspx?Component={data_category}"

        try:
            variable_table = pd.read_html(url)[0]  # Assuming the table is the first one on the page
        except (ValueError, IndexError) as e:
            # If no tables are found, return None
            print(f"Exception raised: {type(e).__name__} - {str(e)}")
            return None

        if "Begin Year" in variable_table.columns and "EndYear" in variable_table.columns:
            variable_table["Years"] = variable_table.apply(lambda row: f"{row['Begin Year']}-{row['EndYear']}", axis=1)
            variable_table.drop(["Begin Year", "EndYear", "Component", "Use Constraints"], axis=1, inplace=True)
            variable_table = variable_table.loc[variable_table["Years"].isin(self.__cycle_list)]

            if variable_table.empty:
                # If no matching cycle years are found, return None
                return None

            variable_table.reset_index(drop=True, inplace=True)
        else:
            raise Exception("The variable table format has changed. Please update the code to match the new format.")

        # Replace 'Data File Description' with 'Demographic Variables & Sample Weights' if data_category is 'demographics'
        if data_category == 'demographics':
            variable_table['Data File Description'] = 'Demographic Variables & Sample Weights'

        return variable_table


    def list_file_names(self, data_category, cycle_years=None):
        """
        Get a list of unique values in the 'Data File Description' column for a specific data category and optional cycle years.

        Args:
        data_category (str): The data category for which you want to retrieve unique data file descriptions.
        cycle_years (str or list of str, optional): The specific year-cycles to filter the variable table. If not specified, all available cycles are considered.

        Returns:
        list: A list of unique data file descriptions for the specified data category and cycle years.

        Raises:
        Exception: If there is an error fetching the variable table, if no data is available, or if the data category is not recognized.
        """
        try:
            variable_table = self._retrieve_variable_table(data_category)
        except Exception as e:
            raise Exception(f"Error while retrieving the variable table: {e}")

        if variable_table is None:
            raise Exception("No data available for the specified data category and cycle years.")

        if cycle_years is not None:
            # Filter the variable table based on specified year-cycles
            valid_cycles = self._check_cycle(cycle_years)
            variable_table = variable_table[variable_table['Years'].isin(valid_cycles)]

            if variable_table.empty:
                raise Exception("No data available for the specified data category and cycle years.")

        try:
            unique_descriptions = variable_table["Data File Description"].unique().tolist()
        except KeyError:
            raise Exception("The variable table format has changed. Please update the code to match the new format.")

        return unique_descriptions
    


    def retrieve_cycle_data_file_name_mapping(self, variable_table, file_name):
        """
        Retrieve a dictionary of years and Data File Names based on a given "Data File Description."

        Args:
        data_file_description (str): The "Data File Description" to filter the variable table.

        Returns:
        dict: A dictionary mapping years to Data File Names.

        Raises:
        ValueError: If no data matches the provided "Data File Description."
        """
        filtered_data = variable_table[variable_table["Data File Description"] == file_name]

        if filtered_data.empty:
            raise ValueError(f"No data found for the specified 'Data File Description': {file_name}")

        years_data_files_dict = {}
        for index, row in filtered_data.iterrows():
            years = row["Years"]
            data_file_name = row["Data File Name"]
            years_data_files_dict[years] = data_file_name

        return years_data_files_dict


    def _check_cycle(self, input_cycle):
        """
        Check the validity of a cycle and return valid cycle(s) based on input.

        Args:
        input_cycle (str or list): The input cycle year(s), range(s), or list of valid cycles.

        Returns:
        list: List of valid cycle(s) based on input.

        Acceptable input formats:
        - Single cycle year as a string, e.g., '2005'
        - List of single cycle years, e.g., ['2005', '2007']
        - Cycle range in the form 'start_year'-'end_year', e.g., '2005'-'2006'
        - List of cycle ranges, e.g., ['2005'-'2006', '2007'-'2008']

        Returns a list of valid cycle years or an empty list if the input is not recognized.
        """
        if not isinstance(input_cycle, list):
            input_cycle = [input_cycle]  # Convert a single cycle year into a list
        valid_cycles = []

        for cycle in input_cycle:
            if isinstance(cycle, str):
                if '-' in cycle:
                    start_year, end_year = cycle.split('-')
                    valid_cycles.extend(self._check_in_between_cycle(start_year, end_year))
                elif cycle in self.__cycle_list:
                    valid_cycles.append(cycle)
                else:
                    for cycle_year in self.__cycle_list:
                        if cycle in cycle_year:
                            valid_cycles.append(cycle_year)

        return valid_cycles

    


    def _check_in_between_cycle(self, start_year, end_year):
        """
        Check for valid cycles within a range.

        Args:
        start_year (str): The start year of the range.
        end_year (str): The end year of the range.

        Returns:
        list: List of valid cycle(s) within the specified range or an empty list if no valid cycles are found.
        """
        valid_cycles = []
        found_start = False

        for cycle in self.__cycle_list:
            if start_year in cycle:
                found_start = True
            if found_start:
                valid_cycles.append(cycle)
            if end_year in cycle:
                break

        return valid_cycles


    def _get_data_filename(self, data_category, cycle_year, data_file_description):
        """
        Get the data file name for a specific cycle year and data file description.

        Args:
        data_category (str): The data category for which data is requested.
        cycle_year (str): The year or cycle for which data is requested.
        data_file_description (str): The data file description.

        Returns:
        str: The data file name or None if no match is found.
        
        Raises:
        ValueError: If no matching data file name is found.
        """
        variable_table = self._retrieve_variable_table(data_category)

        try:
            data_file_name = variable_table.loc[(variable_table['Years'] == cycle_year) & (variable_table['Data File Description'] == data_file_description), 'Data File Name'].values[0]
            return data_file_name
        except IndexError:
            raise ValueError(f"No data file found for Data Category: {data_category}, Year: {cycle_year}, Data File Description: {data_file_description}")



    def get_common_and_uncommon_variables(self, data_category, cycle_years):
        """
        Find common and uncommon variables across multiple cycle years for a specific data category.

        Args:
        data_category (str): The data category for which data is requested.
        cycle_years (str or list of str): Either a single cycle year or a list of cycle years.

        Returns:
        list: List of common variables found across the specified cycle years.
        list: List of uncommon variables not found in all of the specified cycle years.
        dict: A dictionary of {variable (Variable Description): [cycles]} showing which cycles each variable appears in.
        
        Raises:
        ValueError: If the specified cycle years are invalid or if there is only one cycle specified.
        """
        if isinstance(cycle_years, str):
            cycle_years = [cycle_years]

        common_variables = None
        variable_cycles_dict = {}
        all_variables = list()  # Initialize a list for all variables
        variable_table = self._retrieve_variable_table(data_category)  # Retrieve the variable table once

        valid_cycles = list()
        for cycle in cycle_years:
            valid_cycles = valid_cycles + self._check_cycle(cycle)

        if valid_cycles == []:
            raise ValueError(f"You have entered an Invalid cycle. Below is a list of valid cycles: \n {self.__cycle_list}")

        if len(valid_cycles) < 2:
            raise ValueError("There is only one cycle here. This function can only be performed for 2 or more cycle years.")

        for valid_cycle in valid_cycles:
            variables = [row['Variable Name'] for index, row in variable_table.iterrows() if row['Years'] == valid_cycle]


            if common_variables is None:
                common_variables = set(variables)
            else:
                common_variables.intersection_update(variables)

            for variable in variables:
                if variable in variable_cycles_dict:
                    variable_cycles_dict[variable].append(valid_cycle)
                else:
                    variable_cycles_dict[variable] = [valid_cycle]

            all_variables = all_variables + variables

        common_variables = list(common_variables)
        all_variables = list(set(all_variables))
        uncommon_variables = [variable for variable in all_variables if variable not in common_variables]


        return common_variables, uncommon_variables, variable_cycles_dict


    # def get_common_and_uncommon_variables(self, data_category, cycle_years):
    #     """
    #     Find common and uncommon variables across multiple cycle years for a specific data category.

    #     Args:
    #     data_category (str): The data category for which data is requested.
    #     cycle_years (str or list of str): Either a single cycle year or a list of cycle years.

    #     Returns:
    #     list: List of common variables found across the specified cycle years.
    #     list: List of uncommon variables not found in all of the specified cycle years.
    #     dict: A dictionary of {variable (Variable Description): [cycles]} showing which cycles each variable appears in.
        
    #     Raises:
    #     ValueError: If the specified cycle years are invalid or if there is only one cycle specified.
    #     """
    #     if isinstance(cycle_years, str):
    #         cycle_years = [cycle_years]

    #     common_variables = None
    #     variable_cycles_dict = {}
    #     all_variables = list()  # Initialize a list for all variables
    #     variable_table = self._retrieve_variable_table(data_category)  # Retrieve the variable table once

    #     valid_cycles = list()
    #     for cycle in cycle_years:
    #         valid_cycles = valid_cycles + self._check_cycle(cycle)

    #     if valid_cycles == []:
    #         raise ValueError(f"You have entered an Invalid cycle. Below is a list of valid cycles: \n {self.cycle_list}")

    #     if len(valid_cycles) < 2:
    #         raise ValueError("There is only one cycle here. This function can only be performed for 2 or more cycle years.")

    #     for valid_cycle in valid_cycles:
    #         variables = [(row['Variable Name'] + ' (' + row['Variable Description'] + ')') for index, row in variable_table.iterrows() if row['Years'] == valid_cycle]

    #         if common_variables is None:
    #             common_variables = set(variables)
    #         else:
    #             common_variables.intersection_update(variables)

    #         for variable in variables:
    #             if variable in variable_cycles_dict:
    #                 variable_cycles_dict[variable].append(valid_cycle)
    #             else:
    #                 variable_cycles_dict[variable] = [valid_cycle]

    #         all_variables = all_variables + variables

    #     common_variables = list(common_variables)
    #     all_variables = list(set(all_variables))
    #     uncommon_variables = [variable for variable in all_variables if variable not in common_variables]

    #     return common_variables, uncommon_variables, variable_cycles_dict



    def retrieve_data(self, data_category, cycle, filename, include_uncommon_variables=True):
        """
        Retrieve data for a specific data category, cycle year(s), and data file description.

        Args:
        data_category (str): The data category for which you want to retrieve data.
        cycle (str or list): The cycle year(s) for which you want to retrieve data.
        filename (str): The data file description for which you want to retrieve data.
        include_uncommon_variables (bool, optional): Whether to include uncommon variables. Defaults to True.
        specific_variables (list of str, optional): List of specific variables to retrieve. Defaults to None, meaning all variables will be retrieved.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.

        Raises:
        Exception: If there is an error retrieving the data.
        """
        temp_cycle_list = self._check_cycle(cycle)
        if not temp_cycle_list:
            raise ValueError("Invalid cycle input.")
        
        if len(temp_cycle_list) == 1:
            data_file_name = self._get_data_filename(data_category, temp_cycle_list[0], filename)
            if data_file_name is None:
                raise ValueError(f"No data file found for Data Category: {data_category}, Year: {temp_cycle_list[0]}, Data File Description: {filename}")
            data = pd.read_sas(f"https://wwwn.cdc.gov/Nchs/Nhanes/{temp_cycle_list[0]}/{data_file_name}.XPT")
            data['year'] = temp_cycle_list[0]
            return data

        data_frames = []  # List to store individual data frames from different cycles

        common_variables, uncommon_variables, _ = self.get_common_and_uncommon_variables(data_category, temp_cycle_list)

        for cycle_year in temp_cycle_list:
            try:
                data_file_name = self._get_data_filename(data_category, cycle_year, filename)
                if data_file_name is None:
                    continue  # Skip this cycle if the data file name is not found
                data = pd.read_sas(f"https://wwwn.cdc.gov/Nchs/Nhanes/{cycle_year}/{data_file_name}.XPT")
                
                # Include or exclude uncommon variables based on the parameter
                if include_uncommon_variables is False:
                    data = data[common_variables]

                # Add a 'year' column indicating the cycle year
                data['year'] = cycle_year

                data_frames.append(data)
            except Exception as e:
                raise ValueError(f"Error fetching data for cycle {cycle_year}: {str(e)}")

        if not data_frames:
            raise ValueError(f"No data available for the specified data category and cycle years.")
        
        # Concatenate data frames from different cycles
        concatenated_data = pd.concat(data_frames, ignore_index=True)
        return concatenated_data

    def join_data_files(self, cycle_year, data_category1, file_name1, data_category2, file_name2, include_uncommon_variables=True):
        """
        Join two data files from specified data categories and file names based on the common variable SEQN.

        Args:
        cycle_year (str): The cycle year to retrieve data.
        data_category1 (str): The first data category to retrieve data from.
        file_name1 (str): The data file description for the first data file.
        data_category2 (str): The second data category to retrieve data from.
        file_name2 (str): The data file description for the second data file.
        include_uncommon_variables (bool, optional): Whether to include uncommon variables. Defaults to True.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the joined data.

        Raises:
        Exception: If there is an error joining the data or if data retrieval fails for either of the data categories.
        """
        try:
            # Check if the specified data file names are available in the given cycle year
            data_file_names1 = self.list_file_names(data_category1, cycle_year)
            data_file_names2 = self.list_file_names(data_category2, cycle_year)
            
            if file_name1 not in data_file_names1:
                raise ValueError(f"Data file name '{file_name1}' is not available in the specified cycle year '{cycle_year}' for data category '{data_category1}'.")
            if file_name2 not in data_file_names2:
                raise ValueError(f"Data file name '{file_name2}' is not available in the specified cycle year '{cycle_year}' for data category '{data_category2}'.")
            
            # Retrieve data for the first data file
            data1 = self.retrieve_data(data_category1, cycle_year, file_name1, include_uncommon_variables)
            
            # Retrieve data for the second data file
            data2 = self.retrieve_data(data_category2, cycle_year, file_name2, include_uncommon_variables)
            
            # Perform inner join on the common variable SEQN
            joined_data = pd.merge(data1, data2, on='SEQN', how='inner')
            
            # Drop the 'year_x' and 'year_y' columns
            joined_data = joined_data.drop(['year_x', 'year_y'], axis=1)
            
            return joined_data
        except Exception as e:
            raise ValueError(f"Error while joining data files: {str(e)}")
