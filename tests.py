import glob
import os


from django.test import TestCase
import re
import pandas as pd
import time

# Create your tests here.
from openpyxl import load_workbook

PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}/download'

xlsx_dir_path = f'{DOWNLOAD_DIR}/test'
xlsx_list = glob.glob(f'{xlsx_dir_path}/*.xlsx')    # 리스트 형태(여러 엑셀파일이 존재할때 사용)

df_value = xlsx_list[0]
df = pd.read_excel(df_value, sheet_name=0)
print(df_value.split("/")[-1], ':')
df_sample = df.iloc[15, 5]

print(df.iloc[0, 48])   # AW2
print(df_sample)
df.iloc[0, 49] = 24.0
print(df.iloc[0, 49])
print(df.iloc[15, 5])

# load_wb = load_workbook(df_value, data_only=True)
# load_ws = load_wb["렌터카_일반"]
# F17 = load_ws['F17']
# print(F17.value())




# def get_file_info(xlsx_list: list) -> list:
#     info_list = []
#
#     for xlsx_path in xlsx_list:
#
#         try:
#             start = time.time()
#             info = pd.read_excel(xlsx_path,
#                                  sheet_name=1)  # pd.read_excel(excel_name, sheet_name=1) = 인덱스로 시트 지정 //
#             # pd.read_excel(excel_name, sheet_name='sheetName') = 시트 이름으로 시트 지정
#             file_name = xlsx_path.split('/')[-1]
#             print(file_name, ':')
#             print(info)
#             end = time.time()
#             print((end - start))
#             print(info['F17'].value())
#         except FileNotFoundError:
#             continue
#
#     return info_list
#
#
# get_file_info(xlsx_list)
