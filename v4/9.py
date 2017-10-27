import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import re


def get_page_index(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None



def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('gallery: (.*?)"]},', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            return {
                'title': title,
                'images': images
            }

def main():
    url = "http://toutiao.com/group/6480644486006309389/"
    html = get_page_index(url)
    html = parse_page_detail(html)
    if html:
        result = parse_page_detail(html, url)
        print(result)

if __name__ == '__main__':
    main()

