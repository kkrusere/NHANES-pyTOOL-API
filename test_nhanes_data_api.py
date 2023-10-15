import unittest
from unittest.mock import patch

import pandas as pd
import numpy as np

from NHANES_data_API import NHANESDataAPI

class TestNHANESDataAPI(unittest.TestCase):
    def setUp(self):
        self.api = NHANESDataAPI()

    def test_list_data_categories(self):
        data_categories = self.api.list_data_categories()
        expected_categories = ["demographics", "dietary", "examination", "laboratory", "questionnaire", "limitedaccess"]
        self.assertEqual(data_categories, expected_categories)

    def test_list_cycle_years(self):
        expected_cycle_years = ['1999-2000','2001-2002','2003-2004','2005-2006','2007-2008',
                                '2009-2010','2011-2012','2013-2014','2015-2016','2017-2018'
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

    def test_common_variables(self):
        data_category = "demographics"
        cycle_years = ['2009-2010', '2011-2012']
        common, uncommon, variable_cycles_dict = self.api.common_variables(data_category, cycle_years)
        self.assertIsInstance(common, list)
        self.assertIsInstance(uncommon, list)
        self.assertIsInstance(variable_cycles_dict, dict)

if __name__ == '__main__':
    unittest.main()