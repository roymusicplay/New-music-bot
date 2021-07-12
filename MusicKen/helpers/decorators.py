from typing import Callable
from pyrogram import Client
from pyrogram.types import Message
from MusicKen.config import SUDO_USERS
from MusicKen.config import SUB_GROUP
from MusicKen.helpers.admins import get_administrators


def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply(f"{type(e).__name__}: {e}")

    return decorator


def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator


def subcribe(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
       if not message.from_user.id in SUB_GROUP:
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply_text(f"[" + user_name + "](tg://user?id=" + str(user_id) + ") Anda harus bergabung dulu di https://t.me/c/{SUB_GROUP} agar bisa menggunakan bot ini")

    return decorator
