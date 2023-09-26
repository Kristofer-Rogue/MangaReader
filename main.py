import requests
from DBMangaIO import DBMangaIO
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '
                  'Safari/537.36',
}


def get_page_count(url: str) -> int:
    with requests.get(url, headers=headers) as req:
        soup = BeautifulSoup(req.text, 'lxml')
        return int(soup.find('a', class_='nextLink').previous_element.text)


def parse_data(db: DBMangaIO):
    offset = 0

    base_url = 'https://readmanga.live/list?sortType=DATE_CREATE&offset='
    url_with_offset = base_url + str(offset)

    page_count = get_page_count(url_with_offset)
    last_url = base_url + str(page_count)

    manga_on_last_page = len(find_all_manga_on_page(last_url))
    for page in range(page_count, -1, -1):
        url = f'https://readmanga.live/list?sortType=DATE_CREATE&offset={page * 50}'

        get_manga_on_page(db, url)
        print(f'Страница {page} получена!')

    if (manga_on_last_page - len(find_all_manga_on_page(last_url))) != 0:
        print('База манги была обновлена! Придется начать сначала :(')
        parse_data(db)


def get_manga_on_page(db: DBMangaIO, url):
    manga_hrefs = find_all_manga_on_page(url)
    for item in manga_hrefs:
        manga = item.find('a')
        manga_title = manga.get('title')
        manga_href = 'https://readmanga.live' + manga.get('href')
        db.add_to_table(manga_title, manga_href)


def find_all_manga_on_page(url: str):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    manga_hrefs = soup.find_all(class_="desc")
    manga_hrefs.reverse()
    return manga_hrefs


def main():
    db = DBMangaIO()
    parse_data(db)


if __name__ == '__main__':
    main()