import os
import pandas as pd

class NHANESDataAPI:
    cycle_list = [
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

    data_category_list = [
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
        return self.data_category_list
    
    def list_cycle_years(self):
        """
        List the available NHANES cycle years.

        Returns:
        list: List of available cycle years.
        """
        return self.cycle_list

    def _retrieve_variable_table(self, data_category):
        """
        Retrieve the variable table for a specific data category.

        Args:
        data_category (str): The data category for which you want the variable table.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the variable table.

        Raises:
        Exception: If there is an error fetching the variable table or if no data is available.
        """

        url = f"https://wwwn.cdc.gov/nchs/nhanes/search/variablelist.aspx?Component={data_category}"

        try:
            variable_table = pd.read_html(url)[0]  # Assuming the table is the first one on the page
        except (ValueError, IndexError):
            raise Exception("Error fetching the variable table. Please check the data category or the website's format.")

        # Perform data cleaning
        if "Begin Year" in variable_table.columns and "EndYear" in variable_table.columns:
            variable_table["Years"] = variable_table.apply(lambda row: f"{row['Begin Year']}-{row['EndYear']}", axis=1)
            variable_table.drop(["Begin Year", "EndYear", "Component", "Use Constraints"], axis=1, inplace=True)
            variable_table = variable_table.loc[variable_table["Years"].isin(self.cycle_list)]

            if variable_table.empty:
                raise Exception("No data available for the specified data category and cycle years.")

            variable_table.reset_index(drop=True, inplace=True)
        else:
            raise Exception("The variable table format has changed. Please update the code to match the new format.")

        # Replace 'Data File Description' with 'Demographic Variables & Sample Weights' if data_category is 'demographics'
        if data_category == 'demographics':
            variable_table['Data File Description'] = 'Demographic Variables & Sample Weights'

        return variable_table


    def list_file_names(self, data_category):
        """
        Get a list of unique values in the 'Data File Description' column for a specific data category.

        Args:
        data_category (str): The data category for which you want to retrieve unique data file descriptions.

        Returns:
        list: A list of unique data file descriptions.

        Raises:
        Exception: If there is an error fetching the variable table, if no data is available, or if the data category is not recognized.
        """
        try:
            variable_table = self._retrieve_variable_table(data_category)
        except Exception as e:
            raise Exception(f"Error while retrieving the variable table: {e}")

        if variable_table is None:
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
        input_cycle (str): The input cycle year or range.

        Returns:
        list: List of valid cycle(s) based on input.
        """
        if '-' in input_cycle:
            start_year, end_year = input_cycle.split('-')
            the_cycle_list = self._check_in_between_cycle(start_year, end_year, self.cycle_list)
            return the_cycle_list
        elif input_cycle in self.cycle_list:
            return [input_cycle]
        elif any(input_cycle in cycles for cycles in self.cycle_list):
            return [cycle for cycle in self.cycle_list if input_cycle in cycle]
        else:
            return []

    def _check_in_between_cycle(self, start_year, end_year, cycle_list):
        """
        Check for valid cycles within a range.

        Args:
        start_year (str): The start year of the range.
        end_year (str): The end year of the range.
        cycle_list (list): List of available cycle years.

        Returns:
        list: List of valid cycle(s) within the range.
        """
        list_of_cycles_to_be_worked_on = []
        flager = 0
        for cycle in cycle_list:
            if start_year in cycle:
                flager = 1
            if flager == 1:
                list_of_cycles_to_be_worked_on.append(cycle)
            if end_year in cycle:
                return list_of_cycles_to_be_worked_on
        return list_of_cycles_to_be_worked_on


    def _get_data_filename(self, data_category, cycle_year, data_file_description):
        """
        Get the data file name for a specific cycle year and data file description.

        Args:
        data_category (str): The data category for which data is requested.
        cycle_year (str): The year or cycle for which data is requested.
        data_file_description (str): The data file description.

        Returns:
        str: The data file name.
        
        Raises:
        ValueError: If no matching data file name is found.
        """
        variable_table = self._retrieve_variable_table(data_category)

        try:
            data_file_name = variable_table.loc[(variable_table['Years'] == cycle_year) & (variable_table['Data File Description'] == data_file_description), 'Data File Name'].values[0]
            return data_file_name
        except IndexError:
            raise ValueError(f"No data file found for Data Category: {data_category}, Year: {cycle_year}, Data File Description: {data_file_description}")






    def common_variables(self, data_category, cycle_years):
        """
        Find common and uncommon variables across multiple cycle years for a specific data category.

        Args:
        data_category (str): The data category for which data is requested.
        cycle_years (str or list of str): Either a single cycle year or a list of cycle years.

        Returns:
        list: List of common variables found across the specified cycle years.
        list: List of uncommon variables not found in all of the specified cycle years.
        dict: A dictionary of {variable: [cycles]} showing which cycles each variable appears in.
        
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
            raise ValueError(f"You have entered an Invalid cycle. Below is a list of valid cycles: \n {self.cycle_list}")

        if len(valid_cycles) < 2:
            raise ValueError("There is only one cycle here. This function can only be performed for 2 or more cycle years.")

        for valid_cycle in valid_cycles:
            print("Valid Cycle:", valid_cycle)
            print("Variable Table Columns:", variable_table.columns)
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


    # def common_variables(self, data_category, cycle_years):
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
        data_category (str): The data category for which data is requested.
        cycle (str or list): The year or cycle(s) for which data is requested.
        filename (str): The data file description.
        include_uncommon_variables (bool, optional): Whether to include uncommon variables in the concatenated data.

        Returns:
        pd.DataFrame: The retrieved data as a pandas DataFrame containing concatenated data from multiple cycles.
        
        Raises:
        ValueError: If there is an error fetching the data or if no data is available.
        """
        cycle_list = self._check_cycle(cycle)
        if not cycle_list:
            raise ValueError("Invalid cycle input.")

        data_frames = []  # List to store individual data frames from different cycles

        common_variables, uncommon_variables, _ = self.common_variables(data_category, cycle_list)

        for cycle_year in cycle_list:
            try:
                data_file_name = self._get_data_filename(data_category, cycle_year, filename)
                data = pd.read_sas(f"https://wwwn.cdc.gov/Nchs/Nhanes/{cycle_year}/{data_file_name}.XPT")
                
                # Include or exclude uncommon variables based on the parameter
                if include_uncommon_variables == False:
                    data = data[common_variables]

                data_frames.append(data)
            except Exception as e:
                raise ValueError(f"Error fetching data for cycle {cycle_year}: {str(e)}")

        # Concatenate data frames from different cycles
        concatenated_data = pd.concat(data_frames, ignore_index=True)
        return concatenated_data



    def join_data_files(self, cycle_year, data_category1, file_name1, data_category2, file_name2, include_uncommon_variables=True):
        """
        Join two data files from specified data categories and file names based on the common variable SEQN.

        Args:
        cycle_year (str): The year or cycle for which data is requested.
        data_category1 (str): The first data category for the first file.
        file_name1 (str): The data file description for the first file.
        data_category2 (str): The second data category for the second file.
        file_name2 (str): The data file description for the second file.
        include_uncommon_variables (bool, optional): Whether to include uncommon variables in the joined data.

        Returns:
        pd.DataFrame: The joined data as a pandas DataFrame.

        Raises:
        ValueError: If there is an error fetching the data or if no data is available.
        """
        try:
            # Retrieve data for the first data file
            data1 = self.retrieve_data(data_category1, cycle_year, file_name1, include_uncommon_variables)
            
            # Retrieve data for the second data file
            data2 = self.retrieve_data(data_category2, cycle_year, file_name2, include_uncommon_variables)
            
            # Perform inner join on the common variable SEQN
            joined_data = pd.merge(data1, data2, on='SEQN', how='inner')
            
            return joined_data
        except Exception as e:
            raise ValueError(f"Error while joining data files: {str(e)}")