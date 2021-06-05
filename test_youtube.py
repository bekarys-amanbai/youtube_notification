import pytest
from youtube import youtube


def test_get_channel():
    url = 'https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos/'

    channel = youtube.get_channel(url)

    assert channel.name
    assert channel.id
    assert channel.video_id


def test_get_videos():
    url = 'https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos/'
    videos = youtube.get_videos(url)

    assert videos

    last_video = videos[0]

    assert last_video.id
    assert last_video.title
    assert last_video.link
    assert last_video.thumbnail
    assert last_video.author_name
    assert last_video.author_id
    assert last_video.author_link
    assert last_video.description
    assert last_video.published
    assert last_video.updated
    assert last_video.views >= 0

# def test_get_new_videos():
#     pass
