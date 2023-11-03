from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

city = 'ahmedabad'
restaurant_name = 'coffee-culture'
area = 'bodakdev'

options = Options()
options.add_argument('--headless=new')
path = 'C:/webdrivers/chromedriver.exe'
driver = webdriver.Chrome(path)
link = f'https://www.zomato.com/{city}/{restaurant_name}-{area}/reviews'
driver.get(link)
time.sleep(2)
reviews = []

for page in range(1,20):
    time.sleep(2)
    reviews_block = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/div/div/section/div[2]/p')
    for i in reviews_block:
        reviews.append(i.text)
    driver.find_element(By.LINK_TEXT, f'{page}').click()

res = {}
res[restaurant_name] = reviews


with open('reviews.json', 'r') as f:
    data  = json.load(f)
data.append(res)

with open('reviews.json', 'w') as file:
    json.dump(data, file)

