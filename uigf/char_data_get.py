import os
import requests
from bs4 import BeautifulSoup

url = 'https://wiki.biligame.com/ys/%E7%A5%88%E6%84%BF'
respone = requests.get(url)
soup = BeautifulSoup(respone.content, 'html.parser')
sort_contexts = soup.find_all('table', class_="wikitable")
sort_contexts_ = soup.find_all('tbody')
# print(sort_contexts)
for element in sort_contexts:
    element_name = element._all_strings
    element_cont = str(element_name)
    bodys = element.find_all('tr')
    print()