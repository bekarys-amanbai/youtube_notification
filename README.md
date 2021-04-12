## Описание
Библиотека создана для уведомления о новых видео без api токена

### Установка
```python
from youtube import youtube
```
У него есть всего три методы
- get_channel(url: str) -> Channel
- get_videos(elf, channel_id: str) -> list[Video]
- get_new_videos(self, channel: Channel) -> list[Video]

### Методы класса

**get_channel**
- youtube url
- - https://www.youtube.com/user/ikakProsto
- - https://www.youtube.com/user/ikakProsto/videos
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos

Вернет -> экземпляр класса Channel

**get_videos** - вернет не более 15 последних видео с канала
- youtube URL
- - https://www.youtube.com/user/ikakProsto
- - https://www.youtube.com/user/ikakProsto/videos
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g
- - https://www.youtube.com/channel/UCQWeDEwQruA_CcyR08bIE9g/videos
- channel_id
- - UCQWeDEwQruA_CcyR08bIE9g
- - UCfdgIq01iG92AXBt-NxgPkg

Вернет -> лист с экземплярами класса Video

**get_new_videos**
- Экземпляр класса Channel

Вернет -> лист с экземплярами класса Video

### Классы данные

Channel:
- name: str
- id: str
- last_video_id: str

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

### Минусы
- get_new_videos сравнивает только с последним video_id, из-за чего, после скрытые последнего видео возвращается все видео, хотя они уже не новые