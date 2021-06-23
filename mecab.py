import csv
import MeCab
import re
import japanize_matplotlib

import collections

import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def create_wordcloud(text):
    fpath = "SourceHanSerifK-Light.otf"

    # ストップワードの設定
    stop_words = [u'もの', u'ため', u'確認', u'人', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
                  u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した', u'思う', \
                  u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て', u'に', u'を', u'は', u'の', u'が', u'と', u'た', u'し', u'で', \
                  u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

    wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500, stopwords=set(stop_words)).generate(text)

    plt.figure(figsize=(15, 12))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

mt = MeCab.Tagger("mecabrc")
words = []

f = open('infact_articles.txt')  # f = open('test.txt', 'rt'):
s = f.read()
f.close()

node = mt.parseToNode(s.replace("*", ""))
while node:
    hinshi = node.feature.split(",")[0]
    if hinshi in ["名詞"]:
        origin = node.feature.split(",")[6]
        words.append(origin)
    node = node.next
create_wordcloud(" ".join(words))



