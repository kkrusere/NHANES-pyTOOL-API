import os
import pandas as pd

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


class NHANESDataAPI:
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
        return data_category_list


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
            variable_table = variable_table.loc[variable_table["Years"].isin(cycle_list)]

            if variable_table.empty:
                raise Exception("No data available for the specified data category and cycle years.")

            variable_table.reset_index(drop=True, inplace=True)
        else:
            raise Exception("The variable table format has changed. Please update the code to match the new format.")

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