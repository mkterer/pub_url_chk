import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
READFILE = 'read_column.txt'


def main():
    """エントリー
    """
    fileobj = open(READFILE, 'r', encoding="utf_8")
    row_no = 0

    while True:
        result_img_status = []
        result_href_status = []
        line = fileobj.readline()
        if line:
            #dom取得
            line = line.replace("\n", "")

            soup = get_dom(line)
            if soup == None:
                output_html_src_is_not_found(line)
                continue

            #ターゲットurlを取得　ここで、追加urlあるならばget_target_link関数で処理して、返す
            image_target_link = get_target_link(soup)

            #ターゲットurlのステータスチェック(追加可能)
            result_img_status = get_url_status_result(image_target_link)

            #書き込み
            output_result(line, result_img_status, "画像")
            output_result(line, result_href_status, "url")
        else:
            break

def get_dom(line: str):
    """htmlを取得

    Args:
        line (str): READFILEから読み込んだ１行のurl

    Returns:
        soup (BeautifulSoup): domデータ
    """
    html = requests.get(line, headers=HEADERS)
    #ある程度、範囲を絞る
    soup = BeautifulSoup(html.content, "html.parser")
    # soup = soup.find(class_="") その他、必要であれば絞る処理追加
    return soup

def get_target_link(soup):
    """htmlから特定のurlを取得

    Args:
        soup (BeautifulSoup): BeautifulSoupで取得したdomデータ

    Returns:
        image_target_link (list): 画像url
    """
    image_target_link = []

    #サムネ
    div = soup.find(class_="p-intro__imgbox")
    if div != None:
        img = div.find('img')
        append_data = ['サムネ', img['src']]
        image_target_link.append(append_data)

    #画像アイテム
    divs = soup.find_all(class_="p-item-image__image-block")
    for div in divs:
        if div != None:
            img = div.find('img')
            append_data = ['画像', img['src']]
            image_target_link.append(append_data)

    #その他、必要であればアイテム検索する処理追加

    return image_target_link

def get_url_status_result(targets :list):
    """urlのステータスをチェック

    Args:
        targets (list): ターゲットurlのリスト

    Returns:
        result_list (list): ターゲットurlのステータス結果のリスト
    """
    result_list = []
    #特定urlを回す
    for target in targets:
        target_url = target[1]
        #urlが空の場合があるのでチェック
        if chk_find_string(target_url):
            try:
                result = requests.get(target_url, headers=HEADERS)
                if result.status_code == requests.codes.ok:
                    # print('ok : ' + target_url)
                    pass
                else:
                    # print('ng : ' + target_url)
                    #リスト毎いれる
                    result_list.append(target)
            except Exception as e:
                #リスト毎いれる
                result_list.append(target)
        else:
            #リスト毎いれる
            result_list.append(target)
    return result_list

def chk_find_string(target: str):
    """urlにhttp文字列があるか確認

    Args:
        target (str): チェックするurl

    Returns:
        result (bool): 結果
    """
    result = True
    if target in 'http':
        result = False
    return result

def output_result(target: list, target_url_info: list, name: str):
    """結果を出力

    Args:
        target (list): 調査url
        target_url_info (list): urlの情報
        name (str): 画像かhrefか
    """
    f = open('myfile.txt', 'a')
    for val in target_url_info:
        if val[1] == '':
            val[1] = 'リンクが空'
        f.write(target+ "," + name + "," + val[0] + "," + val[1] + "\n")
    f.close()

def output_html_src_is_not_found(target: str):
    """出力結果（エラー

    Args:
        target (str): 調査url
    """
    f = open('myfile.txt', 'a')
    f.write(target+ ",記事が見当たらない\n")
    f.close()


if __name__ == "__main__":
    main()
