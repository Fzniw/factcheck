import csv
import time

import requests
from bs4 import BeautifulSoup
import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "close",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "Trailers",
}


def get_html(page_num):
    for i in tqdm.tqdm(range(page_num)):
        url = f"https://navi.fij.info/factchecks/page/{i+1}/"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        contents = soup.find("main", class_="site-main").find_all("div", class_="cont")
        write_to_csv(contents)

        time.sleep(2)


def write_to_csv(contents):
    with open("fact_check.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for content in contents:
            date = content.find("p", class_="time").text.replace(".", "/")
            a = content.find("a")
            title = a.text
            try:
                tag = content.find("p", class_="icon").text
            except:
                pass
            link = a.get("href")

            row = [date, title, tag, link]
            writer.writerow(row)


def get_article_link():
    with open("fact_check.csv", "r") as f:
        reader = csv.reader(f)
        for line in tqdm.tqdm(reader):
            url = line[3]
            if "infact" in url:
                print(f"get content : {url}")

                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                link = soup.find("div", class_="links_btn").find("a").get("href")

                r = requests.get(link, headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                content = soup.find("div", class_="entry-content")
                content.find("div", class_="box").extract()

                with open("infact_articles.txt", mode="a") as f:
                    f.write(content.text)

            time.sleep(2)

if __name__ == "__main__":
    get_article_link()