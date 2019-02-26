from bs4 import BeautifulSoup as bs
import requests
import json
import os
import re

video_sets_filepath = os.path.dirname(os.path.abspath(__file__)) + '/video_sets.csv'
videos_filepath = os.path.dirname(os.path.abspath(__file__)) + '/videos.csv'
video_sets_header = ["netflix_id", "title", "video_type"]
videos_header = ["video_sets_netflix_id", "netflix_id", "season", "episode", "runtime"]

input_url = input('input url: ')
clean_url = re.sub('\?.+', '', input_url)
netflix_id = re.search(r"[0-9]+$", clean_url).group()
url = "https://www.netflix.com/jp/title/" + netflix_id
headers = { 'Accept-Language': "ja,en-US" }
res = requests.get(url, headers=headers)



reactContext = res.text \
    .split("netflix.reactContext = ")[1] \
    .split(';')[0]

soup = bs(res.content, "lxml")
title = soup.find("h1", class_="title-title").text.strip()

if re.search(r'"type":"show"', reactContext):
    topLevelVideoId = re.search(r'"topLevelVideoId":[0-9]+', reactContext).group() \
                        .split(":")[1]
    # video_sets
    with open(video_sets_filepath, mode='w', encoding='utf-8') as f:
        f.write(','.join(video_sets_header))
        f.write('\n')

        # netflix_id
        f.write(topLevelVideoId)
        f.write(',')

        # title
        f.write(title)
        f.write(',')

        # video_type
        f.write("show")
        f.write('\n')

    seasons = re.search(r'"seasons":\[\{(.*?\}\]\}\])', reactContext).group()
    seasons_val = seasons.encode().decode('unicode-escape')
    seasons_val = re.sub('"synopsis":"(.+?)",', '', seasons_val)
    seasons = json.loads('{' + seasons_val + '}')['seasons']

    # videos
    with open(videos_filepath, mode='w', encoding='utf-8') as f:
        f.write(','.join(videos_header))
        f.write('\n')

        for i in range(len(seasons)):
            episodes = seasons[i]['episodes']

            for episode in episodes:
                # video_sets_netflix_id
                f.write(topLevelVideoId)
                f.write(',')

                # netflix_id
                f.write(str(episode['episodeId']))
                f.write(',')

                # season
                f.write(str(seasons[i]['num']))
                f.write(',')

                # episode
                f.write(str(episode['episodeNum']))
                f.write(',')

                # rumtime
                f.write(str(episode['runtime']))
                f.write('\n')

if re.search(r'"type":"movie"', reactContext):
    pattern = r'"metaData":.+"topLevelVideoId":[0-9]+.+"runtime":[0-9]+'
    metaData = re.search(pattern, reactContext).group() + '}'
    metaData = json.loads('{' + metaData + '}')['metaData']

    # video_sets
    with open(video_sets_filepath, mode='w', encoding='utf-8') as f:
        f.write(','.join(video_sets_header))
        f.write('\n')

        # netflix_id
        f.write(str(metaData['topLevelVideoId']))
        f.write(',')

        # title
        f.write(title)
        f.write(',')

        # video_type
        f.write("movie")
        f.write('\n')

    # videos
    with open(videos_filepath, mode='w', encoding='utf-8') as f:
        f.write(','.join(videos_header))
        f.write('\n')

        # video_sets_netflix_id
        f.write(str(metaData['topLevelVideoId']))
        f.write(',')

        # netflix_id
        f.write(str(metaData['topLevelVideoId']))
        f.write(',')

        # season
        f.write(str(1))
        f.write(',')

        # episode
        f.write(str(1))
        f.write(',')

        # rumtime
        f.write(str(metaData['runtime']))
        f.write('\n')
