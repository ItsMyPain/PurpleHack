from config import get_tg_token
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import assistant, commands
import logging
logging.basicConfig(level=logging.INFO)

def get_bot_commands():
    bot_commands = [
        types.BotCommand(command="/info", description="Информация о боте"),
        types.BotCommand(command="/mode", description="Изменить режим получения ответа"),
        types.BotCommand(command="/feedback", description="Контакты команды"),
    ]
    return bot_commands


async def main():
    token = get_tg_token()
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(
        commands.router,
        assistant.router,
        )
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=get_bot_commands())
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())