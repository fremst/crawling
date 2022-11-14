from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings

# https://www.inflearn.com/course/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%AC%EB%A1%A4%EB%A7%81-%EA%B8%B0%EC%B4%88/unit/93650?tab=curriculum

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 셀레니움 로그 무시
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Deprecated warning 무시

driver = webdriver.Chrome("/Users/chankyu/Documents/chromedriver", options=chrome_options)
driver.get('https://www.naver.com/')
driver.implicitly_wait(10)

driver.find_element(By.LINK_TEXT, '블로그').click()

# search = browser.find_element(By.CLASS_NAME, '_searchInput_search_text_3CUDs')
# search.click()