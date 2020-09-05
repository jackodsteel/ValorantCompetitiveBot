from typing import List, Dict

from pprint import pprint

import aiohttp
import requests
from multidict import MultiDict

from valorantcompetitivebot.config.config import TwitchConfig, LivestreamConfig
from valorantcompetitivebot.livestream.source import LivestreamSource, Livestream


class TwitchLivestreamSource(LivestreamSource):
    BASE_URL: str = "https://api.twitch.tv/helix"
    OAUTH_URL: str = "https://id.twitch.tv/oauth2"

    def __init__(self, livestream_config: LivestreamConfig):
        self.config: TwitchConfig = livestream_config.twitch_config
        self.livestream_config: LivestreamConfig = livestream_config
        self.access_token: str = self._get_oauth_token()

    def _get_oauth_token(self) -> str:
        params = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "client_credentials"
        }
        r = requests.post(url=f"{self.OAUTH_URL}/token", params=params)
        return r.json()["access_token"]

    async def get_top_livestreams(self) -> List[Livestream]:
        async with aiohttp.ClientSession(headers=self._get_auth_headers()) as session:
            params = self._assemble_params_for_get_top_livestreams()
            async with session.get(f"{self.BASE_URL}/streams", params=params) as response:
                # TODO: Handle 401 and try to refresh token
                # TODO: Literally any error handling
                print(response.request_info)
                print(response.status)
                pprint(await response.json())
                assert response.status == 200
                return self._convert_stream_json_to_objects(await response.json())
        pass

    def _assemble_params_for_get_top_livestreams(self) -> MultiDict[str, str]:
        params: MultiDict[str, str] = MultiDict()
        params.add("first", str(self.livestream_config.num_streams))
        if self.config.game_ids:
            for game_id in self.config.game_ids:
                params.add("game_id", game_id)
        if self.config.languages:
            for lang in self.config.languages:
                params.add("language", lang)
        return params

    def _get_auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Client-ID": self.config.client_id,
        }

    @staticmethod
    def _convert_stream_json_to_objects(json: dict) -> List[Livestream]:
        streams = json["data"]
        return [
            Livestream(
                link=f"http://twitch.tv/{stream['user_name']}",
                title=stream["title"],
                viewer_count=stream["viewer_count"],
                # TODO: These have placeholders for width and height atm. Handle that somehow.
                thumbnail_link=stream["thumbnail_url"]
            )
            for stream in streams
        ]
