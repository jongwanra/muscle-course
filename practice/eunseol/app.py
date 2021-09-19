from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

# mongoDB setting
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course

# client = MongoClient('localhost', 27017)
# db = client.db_muscles

driver = webdriver.Chrome('./chromedriver')

url = "https://www.youtube.com/results?search_query=가슴+운동&sp=CAM%253D"

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


for card in cards:
    title = card.select_one('#video-title > yt-formatted-string').text.strip()
    count = card.select_one('#metadata-line').text.split()[1]
    creator = card.select_one('#text > a').text
    content_url = card.find("a", attrs={"class": 'yt-simple-endpoint style-scope ytd-video-renderer'})["href"]
    descript = card.select_one('#dismissible > div > div.metadata-snippet-container.style-scope.ytd-video-renderer > yt-formatted-string')
    if descript is not None:
        desc = descript.text.strip()

        doc = {
            'title': title,
            'count': count,
            'creator': creator,
            'content_url': content_url,
            'desc': desc,
            'comment':[]
        }
        db.chest.insert_one(doc)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/ms', methods=['GET'])
def muscle_tag():
    muscles = list(db.abs.find({}, {'_id': False}))
    return jsonify({'result':'success', 'all_muscles': muscles})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)