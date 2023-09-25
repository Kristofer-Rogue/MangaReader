import requests
import json
from bs4 import BeautifulSoup

url = 'https://readmanga.live/list?sortType=created'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '
                  'Safari/537.36'
}
req = requests.get(url, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'lxml')

page_count = int(soup.find('a', class_='nextLink').previous_element)
offset = 50
max_offset = (page_count - 1) * 50

all_manga_dict = {}
while offset <= max_offset + 50:
    manga_hrefs = soup.find_all(class_="desc")
    for item in manga_hrefs:
        manga = item.find('a')
        manga_title = manga.get('title')
        manga_href = 'https://readmanga.live' + manga.get('href')
        all_manga_dict[manga_title] = manga_href
        print(f'{manga_title} - {manga_href}')


    url = f'https://readmanga.live/list?sortType=DATE_CREATE&offset={offset}'
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    offset += 50

with open('all_manga_dict.json', 'w', encoding='UTF-8') as file:
    json.dump(all_manga_dict, file, indent=4, ensure_ascii=False)
