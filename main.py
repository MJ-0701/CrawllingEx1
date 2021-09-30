import glob
import shutil
import sys
import os
import time
from chromedriver import generate_chrome
from selenium import webdriver
import ssl
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys  # 키이벤트 발생
import zipfile  # 집파일 해제를 위한 파이썬 내장 모듈
from xlsxhandler import get_dir_update_info, get_file_diff_info_list


ssl._create_default_https_context = ssl._create_unverified_context

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]   # 크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')  # 해당경로에 드라이버가 있으면 불러오고
    driver.close()  # 현재 탭 닫기 quit() 사용시 브라우저 닫기

except:
    chromedriver_autoinstaller.install(True)    # False 입력시 파이썬 site-packages/chromedriver_autoinstaller 이하 폴더에 크롬드라이버가 설치됩니다.
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')  # 없으면 설치
    driver.close()

PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}/download'    # 비교 분석 해야되는 자료를 다운로드 받을 폴더(디렉토리) 지정
driver_path = f'./{chrome_ver}/'    # 크롬 드라이버 오토 인스톨 디렉토리 경로
# driver_path = f'{PROJECT_DIR}/lib/webDriver/'   # 크롬 드라이버 직접 다운받은 디렉토리 경로




#platform = sys.platform
# if platform == 'darwin':    # 크롬 오토 인스톨을 사용했을시엔 필요 없어보임.
#     print('System platform : Darwin')
#     #driver_path += 'chromedriverMac'
#     driver_path += 'chromedriver'
#
# elif platform == 'linux':
#     print('System platform : Linux')
#     #driver_path += 'chromedriverLinux'
#     driver_path += 'chromedriver'
#
# elif platform == 'win32':
#     print('System platform : Window')
#     #driver_path += 'chromedriverWindow'
#     driver_path += 'chromedriver'
#
# else:
#     print(f'[{sys.platform}] not supported. Check your system platform.')
#     raise Exception()

driver_path += 'chromedriver'

# 크롬 드라이버 인스턴스 생성
chrome = generate_chrome(
    driver_path=driver_path,
    headless=False,
    download_path=DOWNLOAD_DIR)

#페이지 요청
url = 'https://github.com/login'
chrome.get(url)
time.sleep(3)   # 기다리는 시간 3초

#  selector: login_field
elm = chrome.find_element_by_id('login_field')
elm.send_keys('깃허브 아이디')

#  selector: password
elm = chrome.find_element_by_id('password')
elm.send_keys('깃허브 패스워드') #

# 로그인 정보를 입력후 로그인 요청을 위해 엔터키 이벤트를 발생 시켜야함. 클릭 이벤트로 하는 방법도 있지만 전에 해봤으므로, 키이벤트로 처리해보겠다.
elm.send_keys(Keys.RETURN)

time.sleep(5)




url = 'https://github.com/modeal-mj/Dummydata'

chrome.get(url)
time.sleep(5)

# 다운로드 토글 xpath
elm = chrome.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[2]/span/get-repo/feature-callout/details/summary')
elm.click()

# 다운로드 xpath
elm = chrome.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[2]/span/get-repo/feature-callout/details/div/div/div[1]/ul/li[3]')
elm.click()
time.sleep(5)



# zip 파일 경로와 압축해제 후 디렉토리 경로 셋팅
repo_name = 'Dummydata-master'
zip_file_path = f'{DOWNLOAD_DIR}/{repo_name}.zip'
xlsx_dir_path = f'{DOWNLOAD_DIR}/{repo_name}'

# 압축해제 전 디렉토리가 존재한다면 먼저 삭제하는 코드 추가
if os.path.isdir(xlsx_dir_path):
    shutil.rmtree(xlsx_dir_path)    # shutill.rmtree() 함수를 사용하여 삭제할 디렉토리와 그 하위 항목들 전체 삭제.

# os.path.isfile() 함수를 통해 파일 존재여부를 확인
if os.path.isfile(zip_file_path):
    z = zipfile.ZipFile(zip_file_path)
    z.extractall(DOWNLOAD_DIR)  # extractall() 함수로 압축을 푼다.
    z.close()
    os.remove(zip_file_path)    # zip 파일은 더이상 필요 없으니 삭제.

# 파일 찾기 glob 사용

# 압축 해제한 파일 디렉토리의 경로 선언
before_dir_path = f'{xlsx_dir_path}/Before'
after_dir_path = f'{xlsx_dir_path}/After'

# 파일 경로의 리스트 조회
# glob 은 와일드카ㅡ 문자를 사용해서 일ㅈ어한 패턴을 가진 파일 이름들을 지정하기 위한 패턴을 의미한다.
before_xlsx_list = glob.glob(f'{before_dir_path}/*.xlsx')
after_xlsx_list = glob.glob(f'{after_dir_path}/*.xlsx')

# 파일 삭제, 추가 정보 비교 분석
deleted_file_list, new_file_list = get_dir_update_info(before_xlsx_list, after_xlsx_list)
print('삭제된 파일 :', deleted_file_list)
print('추가된 파일 :', new_file_list)

# 파일 비교 분석 후 가져오기
file_diff_info_list = get_file_diff_info_list(after_xlsx_list, before_dir_path)

print('파일 변경 정보: ')
for f in file_diff_info_list:
    print(f'{f.file_name} : \n', f.get_diff_row_format_str())


