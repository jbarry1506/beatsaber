import requests
from bs4 import BeautifulSoup as soup
import pprint


def get_page_data(song_number):
    r = requests.get('https://beatsaver.com/browse/rated/'+song_number)
    pprint.pprint(r.status_code)
    # pprint.pprint(r.text)

    page_html = r.text
    page_soup = soup(page_html, "html.parser")
    page_trs = page_soup.findAll("td")
    return page_trs


def song_titles(trs):
    for d in trs:
        if d.text.__contains__("Song"):
            pprint.pprint(d.text)


def song_author(trs):
    for d in trs:
        if d.text.__contains__("Author"):
            pprint.pprint(d.text)


def song_difficulties(trs):
    for d in trs:
        if d.text.__contains__("Difficulties"):
            pprint.pprint(d.text)


# iterate pages for top 100 songs of the day
def top_100():
    song_list = []
    song_objects = {}
    songs = 0
    while songs < 100:
        song_list.append(get_page_data(songs))
        songs += 20


    return song_objects


all_songs = top_100()

def __main__():


