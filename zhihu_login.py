"""docstring This script is used to login www.zhihu.com"""
import time
import requests
from bs4 import BeautifulSoup

def login():
    """log in zhihu"""
    session = requests.session()
    email = 'email'
    password = 'password'
    login_source = session.get('http://www.zhihu.com/#signin').content
    _xsrf = BeautifulSoup(login_source, 'html5lib').find('input', attrs={'name': '_xsrf'})['value']
    data = {
        '_xsrf': _xsrf, 
        'email': email, 
        'password': password, 
        'remember': 'true'
    }
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
    response = session.post('https://www.zhihu.com/login/email', data=data).content
    assert b'\u767b\u9646\u6210\u529f' in response
    return session

if __name__ == "__main__":
    session = login()
    zhihu = session.get("https://www.zhihu.com").content
    soup = BeautifulSoup(zhihu, 'html5lib')
    print(soup.find('span', attrs={'class': 'name'}).string)