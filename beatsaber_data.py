import requests
from bs4 import BeautifulSoup as soup
import pprint
import json
import jsonlines


def song_titles(trs):
    for d in trs:
        if d.text.__contains__("Song"):
            pprint.pprint(d.text)


def get_page_data(song_number):
    song_object = []
    r_string = ('https://beatsaver.com/browse/rated/'+str(song_number))
    print(r_string)
    r = requests.get(r_string)
    pprint.pprint(r.status_code)
    # pprint.pprint(r.text)

    page_html = r.text
    page_soup = soup(page_html, "html.parser")
    page_tables = page_soup.findAll("table", {"class": "table"})
    pprint.pprint(page_tables)

    for table in page_tables:

        song = table.contents[3].text
        print(song)

        author_diff = table.contents[5].text
        print(author_diff, "\n")

        song_object.append({
            "song": song,
            "author": author_diff,
        })

    song_json = json.dumps(song_object)
    with jsonlines.open("./beatsaber_top_songs_inside.jsonl", "a") as f:
        f.write_all(song_object)
    f.close()

    return song_json


def __main__():
    n = 0
    while n < 100:
        page = get_page_data(n)
        print("n: ", n, ", page_data: ", page)
        n += 20

    inside = open("./beatsaber_top_songs_inside.jsonl", "r")
    final = open("./beatsaber_top_songs.jsonl", "a")
    final.write("[")
    for line in inside:
        thisline = (line+",")
        final.write(thisline.strip("\n"))
    final.write("]")
    inside.close()
    final.close()


__main__()
