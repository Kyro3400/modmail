from discord import Message, TextChannel, Guild
from discord import Color, Member, User, CategoryChannel, DMChannel
from discord.ext import commands

import abc
import asyncio
from typing import *
from datetime import datetime

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient


class Bot(abc.ABC, commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = datetime.utcnow()

    @property
    def uptime(self) -> str:
        now = datetime.utcnow()
        delta = now - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @property
    @abc.abstractmethod
    def version(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def db(self) -> Optional[AsyncIOMotorClient]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def self_hosted(self) -> bool:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def config(self) -> 'ConfigManagerABC':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def session(self) -> ClientSession:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def api(self) -> 'UserClient':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def threads(self) -> 'ThreadManagerABC':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def log_channel(self) -> Optional[TextChannel]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def snippets(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def aliases(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def token(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def guild_id(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def guild(self) -> Optional[Guild]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def modmail_guild(self) -> Optional[Guild]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def using_multiple_server_setup(self) -> bool:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def main_category(self) -> Optional[TextChannel]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def blocked_users(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def prefix(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def mod_color(self) -> Union[Color, int]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def recipient_color(self) -> Union[Color, int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def process_modmail(self, message: Message) -> None:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def overwrites(ctx: commands.Context) -> dict:
        raise NotImplementedError

    # Broken.
    @abc.abstractmethod
    async def get_latest_updates(self, limit: int = 3) -> NoReturn:
        raise NotImplementedError


class UserClient(abc.ABC):
    @property
    @abc.abstractmethod
    def token(self) -> Optional[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user_info(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_repository(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user_logs(self, user_id: Union[str, int]) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    async def validate_token(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_log(self, channel_id: Union[str, int]) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_config(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_config(self, data: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_log_url(self,
                          recipient: Member,
                          channel: TextChannel,
                          creator: Member) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def append_log(self,
                         message: Message,
                         channel_id: Union[str, int] = '',
                         type_: str = 'thread_message') -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def post_log(self,
                       channel_id: Union[int, str],
                       data: dict) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_metadata(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def post_metadata(self, data: dict) -> dict:
        raise NotImplementedError


class ConfigManagerABC(abc.ABC):
    @property
    @abc.abstractmethod
    def api(self) -> 'UserClient':
        raise NotImplementedError

    @abc.abstractmethod
    def populate_cache(self) -> dict:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def ready_event(self) -> asyncio.Event:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache(self) -> dict:
        raise NotImplementedError

    @cache.setter
    @abc.abstractmethod
    def cache(self, val: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, data: Optional[dict] = None) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def refresh(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def wait_until_ready(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: str, default: Any = None):
        raise NotImplementedError

    @abc.abstractmethod
    def __getattr__(self, value: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, item: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError


class ThreadABC(abc.ABC):
    @abc.abstractmethod
    async def wait_until_ready(self) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def id(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def channel(self) -> Union[TextChannel, DMChannel]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def recipient(self) -> Union[User, Member]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def ready(self) -> bool:
        raise NotImplementedError

    @ready.setter
    @abc.abstractmethod
    def ready(self, flag: bool):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def close_task(self) -> asyncio.TimerHandle:
        raise NotImplementedError

    @close_task.setter
    def close_task(self, val: asyncio.TimerHandle):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self, *, closer: Union[Member, User],
                    after: int = 0,
                    silent: bool = False,
                    delete_channel: bool = True,
                    message: str = None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def cancel_closure(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def edit_message(self, message_id: Union[int, str], message: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def note(self, message: Message) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def reply(self, message: Message,
                    anonymous: bool = False) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, message: Message,
                   destination: Union[TextChannel, DMChannel,
                                      User, Member] = None,
                   from_mod: bool = False,
                   note: bool = False,
                   anonymous: bool = False) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_notifications(self) -> str:
        raise NotImplementedError


class ThreadManagerABC(abc.ABC):
    @abc.abstractmethod
    async def populate_cache(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self) -> Iterator:
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, item: str) -> 'ThreadABC':
        raise NotImplementedError

    @abc.abstractmethod
    async def find(self, *,
                   recipient: Union[Member, User] = None,
                   channel: TextChannel = None) -> \
            Optional['ThreadABC']:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, recipient: Union[Member, User], *,
                     creator: Union[Member, User] = None,
                     category: CategoryChannel = None) -> 'ThreadABC':
        raise NotImplementedError

    @abc.abstractmethod
    async def find_or_create(self,
                             recipient: Union[Member, User]) -> 'ThreadABC':
        raise NotImplementedError

    @abc.abstractmethod
    async def get_dominant_color(self,
                                 url: str = None,
                                 quality: float = 10) -> Color:
        raise NotImplementedError