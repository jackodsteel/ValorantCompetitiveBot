from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import yaml


@dataclass
class BotConfig:
    discord_config: DiscordConfig
    reddit_config: RedditConfig
    sidebar_config: Optional[SidebarConfig]

    @staticmethod
    def parse_from_file(file_location: str) -> BotConfig:
        with open(file_location, 'r') as data:
            data_loaded = yaml.safe_load(data)
            return BotConfig.parse_from(data_loaded)

    @staticmethod
    def parse_from(config: dict) -> BotConfig:
        return BotConfig(
            discord_config=DiscordConfig.parse_from(config["discord"]),
            reddit_config=RedditConfig.parse_from(config["reddit"]),
            sidebar_config=SidebarConfig.parse_from(config["sidebar"]) if "sidebar" in config else None,
        )


@dataclass
class DiscordConfig:
    token: str
    allowed_roles: List[str]

    @staticmethod
    def parse_from(config: dict) -> DiscordConfig:
        return DiscordConfig(
            token=config["token"],
            allowed_roles=config["allowed_roles"],
        )


@dataclass
class RedditConfig:
    username: str
    password: str
    client_id: str
    client_secret: str
    subreddit: str

    @staticmethod
    def parse_from(config: dict) -> RedditConfig:
        return RedditConfig(
            username=config["username"],
            password=config["password"],
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            subreddit=config["subreddit"],
        )


@dataclass
class SidebarConfig:
    livestream_config: Optional[LivestreamConfig]

    @staticmethod
    def parse_from(config: dict) -> SidebarConfig:
        return SidebarConfig(
            livestream_config=LivestreamConfig.parse_from(config["livestream"]) if "livestream" in config else None,
        )


@dataclass
class LivestreamConfig:
    include_thumbnails: bool
    num_streams: int
    twitch_config: Optional[TwitchConfig]

    @staticmethod
    def parse_from(config: dict) -> LivestreamConfig:
        return LivestreamConfig(
            include_thumbnails=config["include_thumbnails"],
            num_streams=config["num_streams"],
            twitch_config=TwitchConfig.parse_from(config["twitch_config"]) if "twitch_config" in config else None,
        )


@dataclass
class TwitchConfig:
    client_id: str
    client_secret: str
    game_ids: List[str]
    languages: Optional[List[str]]

    @staticmethod
    def parse_from(config: dict) -> TwitchConfig:
        return TwitchConfig(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            game_ids=config["game_ids"],
            languages=config.get("languages", None),
        )
