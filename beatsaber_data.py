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

import mysql.connector
from mysql.connector import errors
import requests
from bs4 import BeautifulSoup as soup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
import pprint
import json
import datetime



def song_titles(trs):
    for d in trs:
        if d.text.__contains__("Song"):
            pprint.pprint(d.text)


def get_page_data(song_number):
    song_object = []
    r_string = ('https://beatsaver.com/browse/rated/'+str(song_number))
    #pprint.pprint(r_string)
    r = requests.get(r_string)
    print(r.status_code)
    # pprint.pprint(r.text)

    page_html = r.text
    #print(page_html)
    page_soup = soup(page_html, "html.parser")
    #print(page_soup)
    page_tables = page_soup.findAll("table", {"class": "table"})
    pprint.pprint(page_tables)

    for table in page_tables:
        song = table.contents[3].text
        split_song = str(song).split("\n")
        #print(split_song)

        author_diff = table.contents[5].text

        author_split = author_diff.split("\n")
        difficulty_split = str(author_split[2]).split()

        song_object.append({
            "song": split_song[1],
            "version": split_song[2],
            "author": author_split[1],
            "difficulty": difficulty_split
        })

    with open("./beatsaber_top_songs_inside.json", "a") as f:
        f.write(str(song_object))  #write_all(song_object)
    f.close()
    pprint.pprint(song_object)
    return song_object


def __main__():
    today = datetime.datetime.today().__format__("%Y%m%d")
    n = 0
    c = 0
    final = open("./beatsaber_top_songs.py", "a")
    while n < 20:
        page = get_page_data(n)

        # print("n: ", n, ", page_data: ", page)
        n += 20
        page_items = []
        for p in page:
            idnum = str(c + 1)
            c+=1

            song_id = today + "_" + idnum

            this_song = {song_id: p}
            pprint.pprint(this_song)
            #page_items.append(this_song)
            final.write(str(this_song))
            if n < 19:
                final.write(",\n")

    final.close()

    finalread = open("./beatsaber_top_songs.py", "r")
    for i in finalread:
        pprint.pprint(i)

__main__()
