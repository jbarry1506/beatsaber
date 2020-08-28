# venv virtual environment
# TODO:  clear files before importing data
# TODO:  remove trailing comma at the end of JSON files
# TODO:  remove white space from difficulties
# TODO:  check to see if songs are already present in mongo db
# TODO:  update song ranking and other variables, if the song is in db
# TODO:  if song is not in db, save data to mongo db
# TODO:  schedule cron job to run daily
# TODO:  create added song list
# TODO:  email added song list
# TODO:  check to see if song is already downloaded - requires oculus server - not sure i want to do this, yet
# TODO:  if new song is not downloaded, download - requires oculus server - not sure i want to do this, yet
# TODO:  create webpage output with player, optional email / phone, score, and highest level, auto-record time and date
# TODO:  create players database
# TODO:  if player is not in database, add
# TODO:  sms text message or email congratulations for personal best score


import requests
from bs4 import BeautifulSoup as soup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
import pprint
import json
import jsonlines
# https://jsonlines.readthedocs.io/en/latest/
import datetime


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
    with jsonlines.open("./beatsaber_top_songs_inside.json", "a") as f:
        f.write_all(song_object)
    f.close()

    return song_json


def __main__():
    n = 0
    while n < 100:
        page = get_page_data(n)
        print("n: ", n, ", page_data: ", page)
        n += 20

    inside = open("./beatsaber_top_songs_inside.json", "r")
    final = open("./beatsaber_top_songs.jsonl", "a")
    final.write("[{")
    for l, line in enumerate(inside):
        today = datetime.datetime.today().__format__("%Y%m%d")
        idnum = str(l+1)
        song_id = (today+"_"+idnum)
        this_line = ("\""+song_id+"\": "+line.strip("\r\n")+",\r")
        final.write(this_line)
    final.write("}]")
    inside.close()
    final.close()

    finalread = open("./beatsaber_top_songs.jsonl", "r")
    for l in finalread:
        l_json = json.dumps(l)
        print(l_json)


__main__()
