from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import openpyxl
import time
from tkinter import *

root = Tk()
root.geometry("600x400")
root.title("crawling")
root.resizable(False, False)


# 크롤링 함수
def crawling(keyword):
    # Workbook 생성
    wb = openpyxl.Workbook()

    #  Sheet 활성화
    sheet = wb.active

    # 데이터프레임 내 header(변수명)생성
    sheet.append(["상품명", "가격", "주소"])

    # 브라우저 생성
    browser = webdriver.Chrome(executable_path="C:/chromedriver.exe")

    # 웹 사이트 열기
    browser.get("https://shopping.naver.com/home/p/index.naver")
    browser.implicitly_wait(10)  # 로딩 끝날 때 까지 10초 기다려줌

    # 검색창 클릭
    search = browser.find_element_by_css_selector("input.co_srh_input._input")
    search.click()

    # 검색어 입력
    search.send_keys(keyword)
    search.send_keys(Keys.ENTER)

    # PAGE_DOWN버튼을 7번 눌러 아래로 스크롤
    for i in range(0, 7):
        # 맨 아래로 스크롤을 내린다
        browser.find_element_by_css_selector("body").send_keys(Keys.PAGE_DOWN)

        # 스크롤 사이 페이지 로딩 시간
        time.sleep(1)

    # 상품 정보 div
    items = browser.find_elements_by_css_selector(".basicList_item__2XT81")

    # 정보 크롤링
    for item in items:
        name = item.find_element_by_css_selector(".basicList_title__3P9Q7").text
        price = item.find_element_by_css_selector(".price_num__2WUXn").text
        link = item.find_element_by_css_selector(
            ".basicList_title__3P9Q7 > a"
        ).get_attribute("href")

        # sheet 내 각 행에 데이터 추가
        sheet.append([name, price, link])

    # 엑셀파일로 저장
    wb.save(f"crawling_{keyword}.xlsx")

    # 크롬 드라이버 종료
    browser.quit()

    e_state.delete(0, "end")
    e_state.insert(0, "크롤링 완료")


def crawling_ready():
    # 검색어 받아오기
    keyword = e_keyword.get()

    # 크롤링 시작
    crawling(keyword)


# 상태알림 엔트리
e_state = Entry(root, relief="solid")
e_state.pack(pady=60)

# 레이블
lb = Label(root, text="검색어 :", bg="white")
lb.pack(side="top", pady=10)

# 검색어 엔트리
e_keyword = Entry(root, relief="solid")
e_keyword.pack(side="top")

# 크롤링 시작 버튼
btn = Button(
    root,
    text="크롤링 시작",
    width=10,
    height=2,
    overrelief="solid",
    command=crawling_ready,
    bg="white",
)
btn.pack(pady=40)


root.configure(bg="white")
root.mainloop()
