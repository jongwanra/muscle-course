from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

from flask import Flask, render_template, request, jsonify, redirect, url_for

client = MongoClient('localhost', 27017)
db = client.db_test

driver = webdriver.Chrome('./chromedriver')

url = "https://www.youtube.com/results?search_query=복근+운동&sp=CAM%253D"

driver.get(url)
time.sleep(5)

# 페이지 소스를 가져오기 전에 더보기 버튼
# btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
# btn_more.click()
# time.sleep(5)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

cards = soup.select('#contents > ytd-video-renderer')
# places = soup.select('ul.restaurant_list > div > div > li > div > a')
print(len(cards))

for card in cards:
    title = card.select_one('#video-title > yt-formatted-string').text.strip()
    count = card.select_one('#metadata-line').text.split()[1]
    cr = card.select_one('#text > a').text
    content_url = card.find("a", attrs={"class": 'yt-simple-endpoint style-scope ytd-video-renderer'})["href"]


    descrip = card.select_one('#dismissible > div > div.metadata-snippet-container.style-scope.ytd-video-renderer > yt-formatted-string')
    if descrip is not None:
        desc = descrip.text.strip()

        print(title)
        print(count)
        print(desc)
        print(cr)
        print(content_url)



@scraping.route('/')
def main():
    return render_template("index.html")


if __name__ == '__main__':
    scraping.run('0.0.0.0', port=5000, debug=True)