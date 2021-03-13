import requests
from bs4 import BeautifulSoup
from reppy.robots import Robots
import urllib
from html.parser import HTMLParser
import re

# 歌ネットの検索テーブル用パーサー


class UtanetHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_song = False
        self.found_artist = False
        self.song_name = []
        self.artist_name = []
        self.song_uri = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        # 曲名
        if re.match('td', tag) and "td1" in d.get("class", ""):
            self.found_song = True
        # アーティスト名
        if re.match('td', tag) and "td2" in d.get("class", ""):
            self.found_artist = True
        # 歌詞のURL
        if self.found_song == True and re.match('a', tag):
            d = dict(attrs)
            self.song_uri.append(d.get("href", ""))

    def handle_data(self, data):
        if self.found_song:
            self.song_name.append(data)
            self.found_song = False
        if self.found_artist:
            self.artist_name.append(data)
            self.found_artist = False


def isValidResponse(uri):
    # 正常なhttp応答か確認
    response = requests.get(uri)
    code = response.status_code
    if code == 200:
        return True
    else:
        return False


def isAllowedAccess(uri, base_uri):
    # robotsで禁止されているアクセスでないか確認
    robots = Robots.fetch(base_uri+"/robots.txt")
    agent = robots.agent("*")
    if agent.allowed(uri):
        return True
    else:
        return False


def searchLyricsBySongAndArtist(song_name, artist_name):
    BASE_URI = "https://www.uta-net.com/"
    search_uri = "https://www.uta-net.com/search/?Aselect=2&Bselect=3&Keyword=" + \
        song_name+"&sort=4"
    # 正常にhttp接続できたか確認
    if isValidResponse(BASE_URI):
        pass
    else:
        print("Invalid Response")
        exit(1)

    if isAllowedAccess(search_uri, BASE_URI):
        pass
    else:
        print("Disallowed Access")
        exit(1)

    # 曲名で検索する
    response = requests.get(search_uri)
    soup = BeautifulSoup(response.content, "html.parser")

    search_results = soup.find("tbody")
    # tr タグで分割した配列
    try:
        search_results_list = search_results.find_all("tr")
    except AttributeError:
        print("Not found")
        return False

    parser = UtanetHTMLParser()
    for search_result in search_results_list:
        parser.feed(str(search_result))

    if len(search_results_list) == 1:
        song_uri = parser.song_uri[0]
    else:
        song_index = parser.artist_name.index(artist_name)
        song_uri = parser.song_uri[song_index]

    long_song_uri = urllib.parse.urljoin(BASE_URI, song_uri)

    if isAllowedAccess(long_song_uri, BASE_URI):
        pass
    else:
        print("This access is disallowed")
        return False

    response = requests.get(long_song_uri)
    soup = BeautifulSoup(response.content, "html.parser")
    lyrics_html = soup.find("div", attrs={"id": "kashi_area"})
    re_pattern = "<div id=\"kashi_area\" itemprop=\"text\">(.+)</br></br></div>"
    lyrics_re_match_result = re.match(re_pattern, str(lyrics_html))
    lyrics_re_sub_result = re.sub(
        "<br>|<br/>", "\n", lyrics_re_match_result.group(1))
    print(lyrics_re_sub_result)
    return lyrics_re_sub_result


if __name__ == "__main__":
    # change song_name and artist_name
    song_name = "春雷"
    artist_name = "The Birthday"
    searchLyricsBySongAndArtist(song_name, artist_name)
