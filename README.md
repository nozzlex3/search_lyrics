# pylyrics

## 機能
歌ネット(https://www.uta-net.com/)をスクレイピングして, 歌詞を表示する.  

## 使い方
`search_lyrics_by_song_and_artisit(song_name, artist_name)`  
song_nameに曲名, artist_nameに歌手名を入れると, 歌詞をstr型で返す.
見つからない場合, Falseを返す.  
**曲名, 歌手名ともに完全一致でないと正しく検索できない.**  
(大文字小文字の区別や空白も正しく入力する必要がある)  

## 注意
reppyモジュールは, python 3.9以降では機能しない.
