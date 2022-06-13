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

def music_act_search(word):
    tags = {
        '작업' : 'ST0037',
        '일' : 'ST0034',
    }
    if word == '일':
        url = f"https://www.genie.co.kr/playlist/tags?tags={tags[word]}%7C%7C{word}/공부"
    elif word == '출근' or word == '퇴근':
        url = f"https://www.genie.co.kr/playlist/tags?tags=ST0005%7C%7C%EC%B6%9C%2F%ED%87%B4%EA%B7%BC%EA%B8%B8"
    else:
        url = f"https://www.genie.co.kr/playlist/tags?tags={tags[word]}%7C%7C집중"
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    e = dom.select('#showTagList > div.recom-wrap > ul.md_playlist > li > div.item_info')

    res = [
        {
            '제목' : i.select_one('.title').text.strip(),
            '링크' : i.select_one('.title').a.attrs['onclick'].strip("javascript:playlistLogNDetailView(").strip(",'V',''); return false")
        }
        for i in e
    ]

    df = pd.DataFrame(res)
    
    a = random.randint(0,len(df))
    
    return df[['제목','링크']].iloc[a]

def music_act_result(word):
    res = music_act_search(word).링크
    url = f'https://www.genie.co.kr/playlist/detailView?plmSeq={res}'

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    # e = dom.select('body-content > div.songlist-box > div.music-list-wrap > table > tbody')
    e = dom.select('#body-content > div.songlist-box > div.music-list-wrap > table > tbody > tr.list')
    #body-content > div.songlist-box > div.music-list-wrap > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis



    song = []
    art = []
    # rank = []
    # soundtrack = []
    # link = []
    # alink = []
    rest = {}
    for i in e:
        title = i.select_one('.title.ellipsis').text.strip()
        title = title.strip('TITLE').strip()
        if "19금" in title:
            title = title.strip("19금")
            title = title.strip()
        song.append(title)
        art.append(i.select_one('.artist.ellipsis').text.strip())
        # rank.append(i.select_one('.number').text[:3].strip())
        # soundtrack.append(i.select_one('.albumtitle.ellipsis').text.strip())
        # link.append(i.select_one('.link').a.attrs['onclick'].strip("fnViewSongInfo('").strip("');return false;"))
        # alink.append(i.select_one('.cover').attrs['onclick'].strip("fnViewAlbumLayer('").strip("');return false;"))
        

    rest = {'곡': song, '아티스트': art}
    df_1 = pd.DataFrame(rest)
    a = random.randint(0, len(df_1))
    return df_1.iloc[a]




