## Описание
Позволяет получить базовую информацию о канале и 15 последних видео.

### Установка
```python
from youtube import youtube
```
У него есть всего три методы
- get_channel(url: str) -> Channel
- get_videos(self, channel_id: str) -> list[Video]
- get_new_videos(self, channel: Union[Channel, tuple[str, list[str]]]) -> list[Video]

### Методы класса

**get_channel(url: str) -> Channel**
- пример аргументов url
- - https://www.youtube.com/user/ikakProsto
- - https://www.youtube.com/user/ikakProsto/videos
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos


**get_videos(elf, channel_id: str) -> list[Video]** - вернет не более 15 последних видео с канала
- примеры channel_id
- - UCQWeDEwQruA_CcyR08bIE9g
- - UCfdgIq01iG92AXBt-NxgPkg
- - https://www.youtube.com/user/ikakProsto
- - https://www.youtube.com/user/ikakProsto/videos
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos


### Классы данные

Channel:
- name: str
- id: str
- video_id: list

Video:
- id: str
- title: str
- link: str
- description: str
- thumbnail: str
- author_name: str
- author_id: str
- author_link: str
- published: str
- updated: str
- views: int