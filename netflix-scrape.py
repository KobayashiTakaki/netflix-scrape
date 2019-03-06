from bs4 import BeautifulSoup as bs
import requests
import json
import os
import re

video_sets_filepath = os.path.dirname(os.path.abspath(__file__)) + '/video_sets.csv'
videos_filepath = os.path.dirname(os.path.abspath(__file__)) + '/videos.csv'
video_sets_header = ["netflix_id", "title", "video_type"]
videos_header = ["video_sets_netflix_id", "netflix_id", "season", "episode", "runtime"]

filename = input('input filename: ')
input_urls = [line.strip() for line in open(filename).readlines()]

with open(video_sets_filepath, mode='w', encoding='utf-8') as vsf, \
    open(videos_filepath, mode='w', encoding='utf-8') as vf:

    # video_sets header
    vsf.write(','.join(video_sets_header))
    vsf.write('\n')

    # videos header
    vf.write(','.join(videos_header))
    vf.write('\n')

    for input_url in input_urls:
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
            ### video_sets ###
            # netflix_id
            vsf.write(topLevelVideoId)
            vsf.write(',')

            # title
            vsf.write(title)
            vsf.write(',')

            # video_type
            vsf.write("show")
            vsf.write('\n')

            ### videos ###
            seasons = re.search(r'"seasons":\[\{(.*?\}\]\}\])', reactContext).group()
            seasons_val = seasons.encode().decode('unicode-escape')
            seasons_val = re.sub('"synopsis":"(.+?)",', '', seasons_val)
            seasons = json.loads('{' + seasons_val + '}')['seasons']

            for i in range(len(seasons)):
                episodes = seasons[i]['episodes']

                for episode in episodes:
                    # video_sets_netflix_id
                    vf.write(topLevelVideoId)
                    vf.write(',')

                    # netflix_id
                    vf.write(str(episode['episodeId']))
                    vf.write(',')

                    # season
                    vf.write(str(seasons[i]['num']))
                    vf.write(',')

                    # episode
                    vf.write(str(episode['episodeNum']))
                    vf.write(',')

                    # rumtime
                    vf.write(str(episode['runtime']))
                    vf.write('\n')

        if re.search(r'"type":"movie"', reactContext):
            pattern = r'"metaData":.+"topLevelVideoId":[0-9]+.+"runtime":[0-9]+'
            metaData = re.search(pattern, reactContext).group() + '}'
            metaData = json.loads('{' + metaData + '}')['metaData']

            ### video_sets ###
            # netflix_id
            vsf.write(str(metaData['topLevelVideoId']))
            vsf.write(',')

            # title
            vsf.write(title)
            vsf.write(',')

            # video_type
            vsf.write("movie")
            vsf.write('\n')

            ### videos ###
            # video_sets_netflix_id
            vf.write(str(metaData['topLevelVideoId']))
            vf.write(',')

            # netflix_id
            vf.write(str(metaData['topLevelVideoId']))
            vf.write(',')

            # season
            vf.write(str(1))
            vf.write(',')

            # episode
            vf.write(str(1))
            vf.write(',')

            # rumtime
            vf.write(str(metaData['runtime']))
            vf.write('\n')
