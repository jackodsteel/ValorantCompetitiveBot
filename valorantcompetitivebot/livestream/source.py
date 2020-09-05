from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


@dataclass
class Livestream:
    link: str
    thumbnail_link: str
    title: str
    viewer_count: int


class LivestreamSource(ABC):

    @abstractmethod
    async def get_top_livestreams(self) -> List[Livestream]:
        pass
