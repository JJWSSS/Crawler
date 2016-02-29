import requests
from bs4 import BeautifulSoup
import os
from threading import Thread

def download_photo(photo_url, photo_name, dir):
    """download photo by url"""
    response = requests.get(photo_url)
    suffix = photo_url.rsplit('.',1)[-1]
    if suffix == 'gif':
        return
    content = response.content
    with open(os.path.join(dir, photo_name + '.jpg'), 'wb') as file:
        file.write(content)

def get_photo_url(url, page_number):
    """get photo url and mkdir for page"""
    response = requests.get(url)
    # print(response.encoding)
    # print(response.text.encode('ISO-8859-1').decode('gbk', 'ignore'))
    soup = BeautifulSoup(response.text.encode('ISO-8859-1').decode('gbk', 'ignore'), 'html5lib')
    photos = soup.find_all('div', style='text-align: center;')
    directory_path = os.path.join(r'F:\qiubai-photo', str(page_number))
    os.mkdir(directory_path)
    for photo in photos:
        photo_name = photo.a.img['alt']
        photo_url = photo.a.img['src']
        # print(photo_name.encode('ISO-8859-1'))
        download_photo(photo_url, photo_name, directory_path)

if __name__ == "__main__":
    total_url = 'http://www.qiubaichengren.com/'
    for page_num in range(1,618):
        url = total_url + str(page_num) + '.html'
        t = Thread(target=get_photo_url, args=(url, page_num))
        t.start()
        t.join()
