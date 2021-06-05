from dataclasses import dataclass


@dataclass
class Video:
    id: str
    title: str
    link: str
    thumbnail: str
    author_name: str
    author_id: str
    author_link: str
    description: str
    published: str
    updated: str
    views: int


@dataclass
class Channel:
    name: str
    id: str
    video_id: list
