from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import pymysql.cursors
import time
import os
import json

# Create your views here.
def genine(page=1):
    date = datetime.today().strftime("%Y%m%d")
    url = f'https://www.genie.co.kr/chart/top200?ditc=D&ymd={date}&hh=11&rtm=Y&pg={page}'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    e = dom.select('#body-content > div.newest-list > div > table > tbody > tr')

    song = []
    art = []
    rank = []
    soundtrack = []
    link = []
    albumlink = []
    for i in e:
        title = i.select_one('.title.ellipsis').text.strip()
        if "19금" in title:
            title = title.strip("19금")
            title = title.strip()
        song.append(title)
        art.append(i.select_one('.artist.ellipsis').text.strip())
        rank.append(i.select_one('.number').text[:3].strip())
        soundtrack.append(i.select_one('.albumtitle.ellipsis').text.strip())
        link.append(i.select_one('.link').a.attrs['onclick'].strip("fnViewSongInfo('").strip("');return false;"))
        albumlink.append(i.select_one('.cover').attrs['onclick'].strip("fnViewAlbumLayer('").strip("');return false;"))

    return {'곡': song, '아티스트': art, '순위':rank, '음원':soundtrack, '링크':link, '앨범링크':albumlink}

def main(request):
    page1 = pd.DataFrame(genine(1))
    page2 = pd.DataFrame(genine(2))
    df = pd.concat([page1,page2], ignore_index=True)
    
    a = df.to_json(orient = 'records')
    arr = []
    arr = json.loads(a)
    context = {'song': arr}
    
    return render(request, 'main.html', context)