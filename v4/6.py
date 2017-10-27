import requests
import json
from pyquery import PyQuery as pq


url = 'https://www.zhihu.com/question/19550225'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
response = requests.get(url, headers=headers)
html = response.text
doc = pq(html)
antwort = doc('.RichContent-inner')
antwort.replace("<br/><br/>", "")
print(antwort)

'''



def main():    
    links = get_links()
    for link in links:
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            return response.text

if __name__ == '__main__':
    main()
'''

