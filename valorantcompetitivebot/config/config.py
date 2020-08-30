from __future__ import annotations

from dataclasses import dataclass
from typing import List

import yaml


@dataclass
class BotConfig:
    discord_config: DiscordConfig
    reddit_config: RedditConfig

    @staticmethod
    def parse_from_file(file_location: str) -> BotConfig:
        with open(file_location, 'r') as data:
            data_loaded = yaml.safe_load(data)
            return BotConfig.parse_from(data_loaded)

    @staticmethod
    def parse_from(config: dict) -> BotConfig:
        return BotConfig(
            discord_config=DiscordConfig.parse_from(config["discord"]),
            reddit_config=RedditConfig.parse_from(config["reddit"])
        )


@dataclass
class DiscordConfig:
    token: str
    allowed_roles: List[str]

    @staticmethod
    def parse_from(config: dict) -> DiscordConfig:
        return DiscordConfig(
            token=config["token"],
            allowed_roles=config["allowed_roles"]
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
            subreddit=config["subreddit"]
        )
