import requests
import json

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
'''
def get_url():
    nummber = 61158073
    while nummber >= 61158073:
        nummber = nummber + 1
        url = 'https://www.zhihu.com/question/' + str(nummber)
        response = requests.get(url, headers=headers)
#        if response.status_code == 200:
#            print(url)
'''

def write_to_file(content):
    with open('nihao.txt', 'a', encoding='utf-8') as f: 
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  
        f.close()


def main():
    nummber = 61158073
    while nummber >= 61158073:
        nummber = nummber + 1
        url = 'https://www.zhihu.com/question/' + str(nummber)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(url)
            write_to_file(url)

if __name__ == '__main__':
    main()