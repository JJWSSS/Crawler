import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
    response = requests.get('http://proxy.ipcn.org/country/', headers=headers)
    print(response.encoding)
    soup = BeautifulSoup(response.text.encode('ISO-8859-1').decode('gbk', 'ignore'), 'html5lib')
    tbody = soup.find('table', attrs={'border': '1'})
    with open('proxy_idhost.txt', 'w') as f:
        proxys = tbody.find_all('td')
        num = 0
        for proxy in proxys:
            #print(proxy)
            if isinstance(proxy.string, str):
                f.write(proxy.string)
            #print(proxy)
            num += 1
        print(num)