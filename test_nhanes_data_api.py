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


if __name__ == '__main__':
    unittest.main()