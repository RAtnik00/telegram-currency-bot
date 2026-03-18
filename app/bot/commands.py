from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help information"),
        BotCommand(command="rate", description="Get exchange rates: /rate USD buy"),
        BotCommand(command="convert", description="Convert currency"),
        BotCommand(command="cancel", description="Cancel current action"),
    ]

    await bot.set_my_commands(commands)