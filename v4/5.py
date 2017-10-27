import requests
import json


def get_links():
    links = []
    nummber = 61158073
    while nummber < 61158172:
        nummber = nummber + 1
        urls = 'https://www.zhihu.com/question/' + str(nummber)
        links.append(urls)
    return links

def write_to_file(content):
    with open('19550224.txt', 'a', encoding='utf-8') as f: 
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  
        f.close()

def main():    
    links = get_links()
    for link in links:
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            print(link)
            write_to_file(link)
    

if __name__ == '__main__':
    main()