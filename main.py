import sys
import os
import time
from chromedriver import generate_chrome
from selenium import webdriver
import ssl
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys  # 키이벤트 발생

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
elm.send_keys('깃허브 패스워드')

# 로그인 정보를 입력후 로그인 요청을 위해 엔터키 이벤트를 발생 시켜야함. 클릭 이벤트로 하는 방법도 있지만 전에 해봤으므로, 키이벤트로 처리해보겠다.
elm.send_keys(Keys.RETURN)

time.sleep(5)

url = 'https://github.com/MJ-0701/CrawllingEx1/tree/master'
chrome.get(url)
time.sleep(5)

# 다운로드 토글 xpath
elm = chrome.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[2]/span/get-repo/feature-callout/details/summary')
elm.click()

# 다운로드 xpath
elm = chrome.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[2]/span/get-repo/feature-callout/details/div/div/div[1]/ul/li[3]')
elm.click()
time.sleep(5)
