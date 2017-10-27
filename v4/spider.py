import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
    	yield{
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],  #.strip() 去掉换行符
            'time': item[4].strip()[5:],    #[5:]去掉前面的5个字符，包括冒号
            'score': item[5]+item[6]
    	}

def write_to_file(content):
	with open('rusult.txt', 'a', encoding='utf-8') as f:   # 为了输出汉字 encoding='utf-8'
		f.write(json.dumps(content, ensure_ascii=False) + '\n')   #为了输出汉字 ensure_ascii=False
		f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
    	print(item)
    	write_to_file(item)


if __name__ == '__main__':
	pool = pool()
	pool.map(main, [i*10 for i in range(10)])