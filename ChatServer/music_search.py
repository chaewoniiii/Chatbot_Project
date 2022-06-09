from datetime import datetime
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import os


def music_search(search):

    url = f'https://www.genie.co.kr/search/searchMain?query={search}'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    e = dom.select('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr.list')




    song = []
    art = []
    rank = []
    soundtrack = []
    link = []
    alink = []
    for i in e:
        title = i.select_one('.title.ellipsis').text.strip()
        title = title.strip('TITLE').strip()
        if "19금" in title:
            title = title.strip("19금")
            title = title.strip()
        song.append(title)
        # art.append(i.select_one('.artist.ellipsis').text.strip())
        # rank.append(i.select_one('.number').text[:3].strip())
        # soundtrack.append(i.select_one('.albumtitle.ellipsis').text.strip())
        # link.append(i.select_one('.link').a.attrs['onclick'].strip("fnViewSongInfo('").strip("');return false;"))
        # alink.append(i.select_one('.cover').attrs['onclick'].strip("fnViewAlbumLayer('").strip("');return false;"))
        
        
    res = {'곡': song, 
            # '아티스트': art, '순위':rank, '음원': soundtrack, '링크':link, '앨범링크':alink
            }
    df = pd.DataFrame(res)

    a = random.randrange(0,16)

    df = df['곡'].iloc[a]
    return df