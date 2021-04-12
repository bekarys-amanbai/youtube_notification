# version 0.4

import json

import requests
from bs4 import BeautifulSoup

from .my_data_classes import Video, Channel
from .exception import ThisIsNotAYoutubeLink


class Youtube:
    def get_videos(self, channel_id: str) -> list[Video]:
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

    def get_new_videos(self, channel: Channel) -> list[Video]:
        videos = self.get_videos(channel.id)

        new_videos = []
        for video in videos:
            if video.id == channel.last_video_id:
                break
            else:
                new_videos.append(video)
        return new_videos

    @staticmethod
    def get_channel(url: str) -> Channel:

        if not url.startswith(('https://www.youtube.com/',
                               'http://www.youtube.com/',
                               'https://youtube.com/',
                               'http://youtube.com/',
                               'https://youtu.be/',
                               'http://youtu.be/')):
            raise ThisIsNotAYoutubeLink(f'This is not a Youtube link {url}')

        # добавление в конец 'videos' если нету
        url_arr = url.split('/')
        if not url_arr[-1]:
            if url_arr[-2] != 'videos':
                url += 'videos'
        elif url_arr[-1] != 'videos':
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

        last_video_id = (channel_raw['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']
                                    ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]
                                    ['gridRenderer']['items'][0]['gridVideoRenderer']['videoId'])

        channel = Channel(
            name=channel_raw['microformat']['microformatDataRenderer']['title'],
            id=channel_raw['microformat']['microformatDataRenderer']['urlCanonical'].split('/')[-1],
            last_video_id=last_video_id
        )

        return channel
