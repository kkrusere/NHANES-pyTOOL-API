import unittest
import pandas as pd
from nhanes_pytool_api.nhanes_data.nhanes_data_api import NHANESDataAPI  # Import from the src directory


class TestNHANESDataAPI(unittest.TestCase):
    def setUp(self):
        self.api = NHANESDataAPI()

    def test_list_data_categories(self):
        data_categories = self.api.list_data_categories()
        expected_categories = ["demographics", "dietary", "examination", "laboratory", "questionnaire", "limitedaccess"]
        self.assertEqual(data_categories, expected_categories)

    def test_list_cycle_years(self):
        expected_cycle_years = [
            '1999-2000', '2001-2002', '2003-2004', '2005-2006', '2007-2008',
            '2009-2010', '2011-2012', '2013-2014', '2015-2016', '2017-2018'
        ]
        cycle_years = self.api.list_cycle_years()

        self.assertIsInstance(cycle_years, list)
        self.assertTrue(len(cycle_years) > 0)
        self.assertEqual(cycle_years, expected_cycle_years)

    def test_retrieve_variable_table(self):
        data_category = "demographics"
        variable_table = self.api._retrieve_variable_table(data_category)
        self.assertIsInstance(variable_table, pd.DataFrame)
        self.assertTrue(len(variable_table) > 0)

    def test_list_file_names(self):
        data_category = "demographics"
        file_names = self.api.list_file_names(data_category)
        self.assertIsInstance(file_names, list)
        self.assertTrue(len(file_names) > 0)

    def test_check_single_cycle(self):
        input_cycle = '2005'
        expected_output = ['2005-2006']
        result = self.api._check_cycle(input_cycle)
        self.assertEqual(result, expected_output)

    def test_check_single_cycle_list(self):
        input_cycle = ['2005']
        expected_output = ['2005-2006']
        result = self.api._check_cycle(input_cycle)
        self.assertEqual(result, expected_output)

    def test_check_cycle_range(self):
        input_cycle = ['2005-2006']
        expected_output = ['2005-2006']
        result = self.api._check_cycle(input_cycle)
        self.assertEqual(result, expected_output)

    def test_check_cycle_range_list(self):
        input_cycle = ['2005-2009']
        expected_output = ['2005-2006', '2007-2008', '2009-2010']
        result = self.api._check_cycle(input_cycle)
        self.assertEqual(result, expected_output)

    def test_get_common_and_uncommon_variables(self):
        data_category = "demographics"
        cycle_years = ['2009-2010', '2011-2012']
        common, uncommon, variable_cycles_dict = self.api.get_common_and_uncommon_variables(data_category, cycle_years)
        self.assertIsInstance(common, list)
        self.assertIsInstance(uncommon, list)
        self.assertIsInstance(variable_cycles_dict, dict)

    def test_invalid_data_category(self):
        with self.assertRaises(Exception):
            data_category = "invalid_category"
            self.api._retrieve_variable_table(data_category)

    def test_invalid_file_name(self):
        with self.assertRaises(Exception):
            data_category = "demographics"
            file_name = "invalid_file_name"
            self.api.retrieve_cycle_data_file_name_mapping(data_category, file_name)

    def test_invalid_data_category_for_data_file(self):
        with self.assertRaises(ValueError):
            data_category = "data_category"
            file_name = "Demographic Variables & Sample Weights"
            cycle = '2005-2006'
            self.api._get_data_filename(data_category, cycle, file_name)

    def test_retrieve_data_valid(self):
        data_category = "examination"
        cycle = "2005-2006"
        file_name = "Body Measures"
        include_uncommon = True
        data = self.api.retrieve_data(data_category, cycle, file_name, include_uncommon)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(len(data) > 0)

    def test_retrieve_data_invalid_cycle(self):
        data_category = "examination"
        cycle = "2022-2023"
        file_name = "Body Measures"
        with self.assertRaises(ValueError):
            self.api.retrieve_data(data_category, cycle, file_name)

    def test_retrieve_data_invalid_category(self):
        data_category = "invalid_category"
        cycle = "2005-2006"
        file_name = "Body Measures"
        with self.assertRaises(Exception):
            self.api.retrieve_data(data_category, cycle, file_name)

    def test_join_data_files_valid(self):
        cycle = "2005-2006"
        data_category1 = "examination"
        file_name1 = "Body Measures"
        data_category2 = "demographics"
        file_name2 = "Demographic Variables & Sample Weights"
        include_uncommon = True
        joined_data = self.api.join_data_files(cycle, data_category1, file_name1, data_category2, file_name2, include_uncommon)
        self.assertIsInstance(joined_data, pd.DataFrame)
        self.assertTrue(len(joined_data) > 0)

    def test_join_data_files_invalid(self):
        cycle = "2007-2008"
        data_category1 = "demographics"
        file_name1 = "Demographic Variables & Sample Weights"
        data_category2 = "laboratory"
        file_name2 = "invalid_file_name"
        with self.assertRaises(ValueError):
            self.api.join_data_files(cycle, data_category1, file_name1, data_category2, file_name2)

    def test_data_retrieval_for_specific_variables(self):
        data_category = "laboratory"
        cycle = "2017-2018"
        file_name = "Laboratory and Examination Data"
        include_uncommon = True
        # Specify specific variables to retrieve
        specific_variables = ['SEQN', 'LBXCRP', 'LBXGH']
        data = self.api.retrieve_data(data_category, cycle, file_name, include_uncommon, specific_variables)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(len(data) > 0)
        self.assertTrue(all(variable in data.columns for variable in specific_variables))

if __name__ == '__main__':
    unittest.main()