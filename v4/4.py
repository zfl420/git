import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import re



def get_page_index(offset, keyword):
	data = {
		'offset': offset,
		'format': 'json',
		'keyword': keyword,
		'autoload': 'true',
		'count': '20',
		'cur_tab': 3
	}
	url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		print('请求索引页出错')
		return None

def parse_page_index(html):
	try:
		data = json.loads(html)
		if data and 'data' in data.keys():
			for item in data.get('data'):
				yield item.get('article_url')
	except JSONDecodeError:
		pass

def get_page_detail(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except ConnectionError:
		print('请求详情页出错', url)
		return None

def parse_page_detail(html):
	soup = BeautifulSoup(html, 'lxml')
	title = soup.select('title')[0].get_text()
	images_patern = re.compile


'''
def parse_page_datail(html, url):
	soup = BeautifulSoup(html, 'lxml')
	title = soup.select('title')[0].get_text()
	print(title)
	images_patern = re.compile('var gallery = (.*?);', re.S)
	result = re.search(images_patern, html)
	if result:
		data = json.loads(result.group(1))
		if data and 'sub_images' in data.keys():
			sub_images = data.get('sub_images')
			images = [item.get('url') for item in sub_images]
			print(images)
			return {
				'title': title,
				'url': url,
				'images': images
			}
'''

'''
def parse_page_datail(html,url):
	try:
		data = json.loads(html)
		if gallery and 'gallery' in data.keys():
			for item in data.get('gallery'):
				yield item.get('gallery')
	except JSONDecodeError:
		pass	


def main():
	html = get_page_index(0, '街拍')
	for url in parse_page_index(html):
		html = get_page_detail(url)
		if html:
			result = parse_page_datail(html, url)
			print(result)
'''
def main():
	html = get_page_index(0, '街拍')
	for url in parse_page_index(html):
		html = get_page_detail(url)

if __name__ == '__main__':
	main()

