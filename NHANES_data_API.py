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

