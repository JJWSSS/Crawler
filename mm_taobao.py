"""docstring crawler mm_taobao"""
import os
import time
import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

@asyncio.coroutine
def download_page(page_url, mmtb_name, d_path):
    """download page from url"""
    print('download')
    page_url = 'https:' + page_url
    response = requests.get(page_url)
    content = response.content
    with open(os.path.join(d_path, mmtb_name + '.jpg'), 'wb') as file:
        file.write(content)

def page_control(client, page_num, loop):
    """control the page to the next page"""
    scroll_js = """
    (function () {
      var y = 0;
      var step = 100;
      window.scroll(0, 0);
 
      function f() {
        if (y < document.body.scrollHeight) {
          y += step;
          window.scroll(0, y);
          setTimeout(f, 50);
        } else {
          window.scroll(0, 0);
          document.title += "scroll-done";
        }
      }
 
      setTimeout(f, 1000);
    })();
    """
    client.execute_script(scroll_js)
    time.sleep(4)
    soup = BeautifulSoup(client.page_source, 'html5lib')
    lis = soup.find_all('li', class_='item')
    page_num += 1
    directory_path = os.path.join(r'C:\Users\JJW\Desktop\photo', str(page_num))
    os.mkdir(directory_path)
    tasks = [download_page(image.img['src'], image.a.find_all('div')[2].span.string, directory_path) for image in lis]
    loop.run_until_complete(asyncio.wait(tasks))
    """
    for image in lis:
        mm_name = image.a.find_all('div')[2].span.string
        url = image.img['src']
        download_page(url, mm_name, directory_path)
        print(url)
    """
    button = client.find_element_by_link_text('下一页 >')
    if button.get_attribute('class') == 'page-next':
        print('find')
        button.click()
        page_control(client, page_num, loop)
    else:
        return

if __name__ == "__main__":
    CLIENT = webdriver.Firefox()
    CLIENT.get('https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.4a8o4H')
    LOOP = asyncio.get_event_loop()
    page_control(CLIENT, 0, LOOP)
    LOOP.close()
    CLIENT.close()
