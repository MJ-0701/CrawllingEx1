import glob
import os

from django.test import TestCase
import re
import pandas as pd

# Create your tests here.
PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}/download'

xlsx_dir_path = f'{DOWNLOAD_DIR}/test'
xlsx_list = glob.glob(f'{xlsx_dir_path}/*.xlsx')


# print(pd.read_excel(xlsx_list))

def get_file_info(xlsx_list: list) -> list:
    info_list = []

    for xlsx_path in xlsx_list:
        try:
            print("try")
            info = pd.read_excel(xlsx_path)
            file_name = xlsx_path.split('/')[-1]
            print(file_name, ':')
            print(info)
        except FileNotFoundError:
            print("catch")
            continue

    return info_list


get_file_info(xlsx_list)
