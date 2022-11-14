# https://www.inflearn.com/course/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%AC%EB%A1%A4%EB%A7%81-%EA%B8%B0%EC%B4%88/unit/93650?tab=curriculum

from tkinter import *
import warnings
import csv
import pyautogui

import clipboard

from selenium import webdriver

from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


def add_keyword(event):
    input_keyword = entry1.get()
    if not input_keyword:
        return
    keywords.append(input_keyword)
    label2.config(text=str(keywords)[1:len(str(keywords)) - 1])
    entry1.delete(0, len(input_keyword))
    # entry1.focus()


def delete_keyword():
    keywords.pop()
    label2.config(text=str(keywords)[1:len(str(keywords)) - 1])


def start_crawling():
    # 설정
    chrome_options = Options()

    # 브라우저 자동 종료 방지
    chrome_options.add_experimental_option("detach", True)

    # 불필요한 에러 메시지 미출력
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 셀레니움 로그 무시
    warnings.filterwarnings("ignore", category=DeprecationWarning)  # Deprecated warning 무시

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    action = ActionChains(driver)

    # 웹페이지 이동
    driver.get('https://www.bigkinds.or.kr/v2/news/index.do')
    driver.implicitly_wait(5)  # 로딩까지 5초간 대기
    driver.maximize_window()  # 화면 최대화

    driver.find_element(By.LINK_TEXT, '기간').click()
    driver.find_element(By.CSS_SELECTOR, '.radio-btn:nth-child(2)').click()

    f = open(r"./data.csv", 'w', encoding='utf8', newline='')
    csv_writer = csv.writer(f)

    for keyword in keywords:

        search = driver.find_element(By.CSS_SELECTOR, '#total-search-key')
        search.click()
        search.clear()
        search.send_keys(keyword)
        search.send_keys(Keys.ENTER)

        csv_writer.writerow([keyword])

        for ii in range(0, 2):
            for i in range(1, 11):
                try:
                    result_tag_name = '#news-results > div:nth-child(' + str(i) + ')'
                    result_tag = driver.find_element(By.CSS_SELECTOR, result_tag_name + ' > div')
                    action.move_to_element(result_tag).perform()

                    title_element = driver.find_element(By.CSS_SELECTOR,
                                                        result_tag_name + ' > div > div.cont > a > div > strong > span')
                    title = title_element.text
                    content_element = driver.find_element(By.CSS_SELECTOR,
                                                          result_tag_name + ' > div > div.cont > div > div > a')
                    press_element = driver.find_element(By.CSS_SELECTOR,
                                                        result_tag_name + '> div > div.cont > div > div > a')
                    press = content_element.text
                    link = content_element.get_attribute('href')

                    csv_writer.writerow([title, press, link])
                except Exception as e:
                    pass
            next_btn = driver.find_element(By.CSS_SELECTOR,
                                           '#news-results-tab > div.data-result-ac.pc-only.paging-v2-wrp.btm > div.data-result-btm > div > div > div > div > div:nth-child(7) > a')
            action.move_to_element(next_btn).perform()
            next_btn.click()

        step1_element = driver.find_element(By.CSS_SELECTOR, '#collapse-step-1')
        # action.move_to_element(step1_element).perform()
        step1_element.click()

    f.close()
    driver.quit()
    pyautogui.alert('크롤링이 완료되었습니다.')


def start_formatting():
    f = open(r"./data.csv", 'r', encoding='utf8', newline='')
    csv_reader = csv.reader(f)
    result = ''
    for line in csv_reader:
        if len(line) < 2:
            result += '▶ ' + line[0] + '\n'
        else:
            result += '- ' + line[0] + ' / ' + line[1] + ' / ' + line[2] + '\n'
    f.close()
    # print(result)
    clipboard.copy(result)
    pyautogui.alert('결과가 클립보드에 복사되었습니다.')


keywords = []

root = Tk()
root.title("뉴스 크롤러")
root.geometry("360x75")

label1 = Label(root, width=10, text="검색어 입력:")
label1.grid(row=1, column=1)
entry1 = Entry(root, width=20)
entry1.grid(row=1, column=2)
button1 = Button(root, width=6, text="추가", command=lambda: add_keyword(event=""))
button1.grid(row=1, column=3)
button2 = Button(root, width=6, text="삭제", command=lambda: delete_keyword())
button2.grid(row=1, column=4)

label2 = Label(root, width=50, text="(검색어를 입력하세요.)")
label2.grid(row=2, column=1, columnspan=4)

button3 = Button(root, text="크롤링 시작", command=lambda: start_crawling())
button3.grid(row=3, column=3)
button4 = Button(root, text="포맷 지정", command=lambda: start_formatting())
button4.grid(row=3, column=4)

entry1.bind("<Return>", add_keyword)
root.mainloop()
