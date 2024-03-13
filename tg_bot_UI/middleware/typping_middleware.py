from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with ChatActionSender(
                bot=event.bot,
                action='typing', 
                chat_id=event.chat.id
                                    ):
            return await handler(event, data)