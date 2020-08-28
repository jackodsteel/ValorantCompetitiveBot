from __future__ import annotations

from dataclasses import dataclass
from typing import List

import yaml


@dataclass
class BotConfig:
    discord_config: DiscordConfig

    @staticmethod
    def parse_from_file(file_location: str) -> BotConfig:
        with open(file_location, 'r') as data:
            data_loaded = yaml.safe_load(data)
            return BotConfig.parse_from(data_loaded)

    @staticmethod
    def parse_from(config: dict) -> BotConfig:
        return BotConfig(
            discord_config=DiscordConfig.parse_from(config["discord"])
        )


@dataclass
class DiscordConfig:
    token: str
    allowed_roles: List[str]
    allowed_servers: List[str]

    @staticmethod
    def parse_from(discord_config: dict) -> DiscordConfig:
        return DiscordConfig(
            token=discord_config["token"],
            allowed_roles=discord_config["allowed_roles"],
            allowed_servers=discord_config["allowed_servers"]
        )