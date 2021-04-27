import requests
from bs4 import BeautifulSoup

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
READFILE = 'read_column.txt'

def main():
    fileobj = open(READFILE, 'r', encoding="utf_8")
    row_no = 0

    while True:
        line = fileobj.readline()
        if line:
            #dom取得
            line = line.replace("\n", "")

            html = requests.get(line, headers=HEADERS)
            soup = BeautifulSoup(html.content, "html.parser")
            #さらに絞る
            soup = soup.find(class_="articleMain")
            #ターゲットurlを取得
            image_target_link, button_href_target_link = get_target_link(soup)

            get_url_status_result(image_target_link)
            get_url_status_result(button_href_target_link)
            #該当itemを取得して、linkもしくは画像urlを取得
            row_no += 1
            print(row_no, ":", line)
        else:
            break

def get_dom():
    print('get_dom')

#domから画像urlとアフィurlを取得する
def get_target_link(soup):
    image_target_link = []
    button_href_target_link = []

    #サムネ
    div = soup.find(class_="article-introduction__left__thumb")
    img = div.find('img')
    image_target_link.append(img['src'])

    #画像アイテム
    divs = soup.find_all(class_="type-image")
    for div in divs:
        img = div.find('img')
        image_target_link.append(img['src'])

    #商品のボタン
    pro_buttons = soup.find_all(class_="rankingProduct__body__right__itemListButton")
    for button in pro_buttons:
        button_href_target_link.append(button['href'])

    return image_target_link, button_href_target_link

def get_url_status_result(targets):
    for target in targets:
        result = requests.get(target, headers=HEADERS)
        if result.status_code == requests.codes.ok:
            # print('ok : ' + target)
            pass
        else:
            print('ng : ' + target)

if __name__ == "__main__":
    main()
