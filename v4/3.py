import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
from multiprocessing import Pool

def get_one_page(url):
	try:
		headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

def parse_one_page(html):
	pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)@.*?'
						+ 'movie-item-info.*?title="(.*?)".*?'
						+ 'star">(.*?)</p>.*?releasetime">(.*?)</p>.*?</dd>', re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield{
			'序列': item[0],
			'电影名': item[2],
			'主演': item[3].strip()[3:],
			'上映时间': item[4].strip()[5:],
			'图片': item[1]

		}
def write_to_file(content):
	with open('gut.txt','a', encoding= 'utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n')
		f.close()


def main(offset):
	url = 'https://maoyan.com/board/6?offset=' + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		print(item)
		write_to_file(item)

if __name__ == '__main__':
	pool=Pool()
	pool.map(main, [i*10 for i in range(10)])
