# version 0.5

import re
import json
from typing import Union

import requests
from bs4 import BeautifulSoup

from .my_data_classes import Video, Channel
from .exception import ThisIsNotAYoutubeLink


class Youtube:
    def get_videos(self, channel_id: str) -> list[Video]:
        """
        Will return no more than 15 recent videos from the channel

        :param channel_id:
            channel_id
                UCQWeDEwQruA_CcyR08bIE9g
            or link to YouTube channel
                https://www.youtube.com/user/ikakProsto
                https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g
                https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos

        :return list[Video]:
        """
        if channel_id.startswith(('https://', 'http://')):
            channel_id = self.get_channel(channel_id).id

        link = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        }

        xml = requests.get(link, headers=headers)
        xml.raise_for_status()

        xml_text = xml.text

        soup = BeautifulSoup(xml_text, 'lxml-xml')

        videos_xml = soup.find_all('entry')
        videos = []

        for video_xml in videos_xml:
            video = Video(
                id=video_xml.videoId.get_text(),
                title=video_xml.title.get_text(),
                link=video_xml.link['href'],
                thumbnail=video_xml.group.thumbnail['url'],
                author_name=soup.title.get_text(),
                author_id=soup.channelId.get_text(),
                author_link=soup.link['href'],
                description=video_xml.group.description.get_text(),
                published=video_xml.published.get_text(),
                updated=video_xml.updated.get_text(),
                views=int(video_xml.community.statistics['views'])
            )
            videos.append(video)

        return videos

    def get_new_videos(self, channel: Union[Channel, tuple[str, list[str]]]) -> list[Video]:
        if isinstance(channel, tuple):
            channel = Channel(name='None', id=channel[0], video_id=channel[1])

        videos = self.get_videos(channel.id)

        new_videos = []
        for video in videos:
            if video.id in channel.video_id:
                break
            else:
                new_videos.append(video)
        return new_videos

    @staticmethod
    def get_channel(url: str) -> Channel:

        if not re.match(r'(https?://)(www.)?(youtube\.com/)', url):
            raise ThisIsNotAYoutubeLink(f'This is not a Youtube link {url}')

        # добавление в конец 'videos' если нету
        if url[-6:] != 'videos' and url[-7:] != 'videos/':
            if url[-1] == '/':
                url += 'videos'
            else:
                url += '/videos'

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        }

        html = requests.get(url, headers=headers)
        html.raise_for_status()
        html_text = html.text

        start = html_text.index('{"responseContext":{"serviceTrackingParams":[{"')
        end = html_text.index('"}]}}};') + 6

        channel_raw = json.loads(html_text[start:end])

        video_id = [channel_raw['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']
                    ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]
                    ['gridRenderer']['items'][0]['gridVideoRenderer']['videoId'],
                    channel_raw['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']
                    ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]
                    ['gridRenderer']['items'][1]['gridVideoRenderer']['videoId'],
                    channel_raw['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']
                    ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]
                    ['gridRenderer']['items'][2]['gridVideoRenderer']['videoId']]

        channel = Channel(
            name=channel_raw['microformat']['microformatDataRenderer']['title'],
            id=channel_raw['microformat']['microformatDataRenderer']['urlCanonical'].split('/')[-1],
            video_id=video_id
        )

        return channel
