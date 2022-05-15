from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import openpyxl
import time
from tkinter import *

root = Tk()
root.geometry("600x400")
root.title("crawling product")
root.resizable(False, False)


def btnpress():
    btn.config(text=ent.get())


ent = Entry(root)
ent.pack()

btn = Button(root)
btn.config(text="search")
btn.config(width=10)
btn.config(command=btnpress)
btn.pack()


# 크롤링할 상품의 검색어를 입력받음
keyword = input("검색어를 입력하세요.\n검색어 : ")


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


root.mainloop()
