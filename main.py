import sys
import os
import time
from chromedriver import generate_chrome
from selenium import webdriver
import ssl
import chromedriver_autoinstaller

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
time.sleep(3) # 3초 딜레이