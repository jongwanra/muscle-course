# from bs4 import BeautifulSoup
# from selenium import webdriver
# from time import sleep
#
#
# driver = webdriver.Chrome('./chromedriver')
#
# url = "https://www.youtube.com/results?search_query=복근+운동&sp=CAM%253D"
# driver.get(url)
# sleep(10)
# driver.execute_script("window.scrollTo(0, 1000)")  # 1000픽셀만큼 내리기
# sleep(1)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# sleep(10)
#
#
# req = driver.page_source
# driver.quit()
#
# soup = BeautifulSoup(req, 'html.parser')
# images = soup.select(".tile_item._item ._image._listImage")
# print(len(images))
#
# for image in images:
#     src = image["src"]
#     print(src)

