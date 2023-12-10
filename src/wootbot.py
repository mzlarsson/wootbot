import datetime
import asyncio

import discord
from discord.ext import commands, tasks
import discord

import summary

class WootBot(commands.Bot):

    current_bot = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        post_summary.start()

    async def on_message(self, message):
        if message.author.bot:
            # Ignore bot messages
            return
        print(f'Message from {message.author}: {message.content}')

    @staticmethod
    def create_instance():
        if not WootBot.current_bot:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            WootBot.current_bot = WootBot(command_prefix="/", intents=intents)
        return WootBot.current_bot


@tasks.loop(hours=24)
async def post_summary():
    bot : WootBot = WootBot.current_bot
    yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    for guild in bot.guilds:
        print(f"Processing {guild.name}")
        await guild.fetch_channels()
        message_channel_name = "daily-highscores"
        channel = next((channel for channel in guild.channels if channel.name == message_channel_name), None)
        if channel:
            messages = [msg async for msg in channel.history(limit=200, after=yesterday)]
            messages = list(filter(lambda msg: not msg.author.bot, messages))
            message_data = [(msg.author.id, msg.author.display_name, msg.content) for msg in messages]
            result = summary.get_statistics(message_data)
            if result:
                await channel.send(f"```\n{result}\n```")

@post_summary.before_loop
async def before_post_summary():
    TIME_TO_POST = (24, 0, 0)  # post at midnight
    now = datetime.datetime.now()
    now_in_seconds = now.hour * 3600 + now.minute * 60 + now.second
    timetopost_in_seconds = TIME_TO_POST[0] * 3600 + TIME_TO_POST[1] * 60 + TIME_TO_POST[2]
    if now_in_seconds > timetopost_in_seconds:
        timetopost_in_seconds += 24*60*60  # first time to post is tomorrow
    seconds_left = timetopost_in_seconds - now_in_seconds

    print(f"Waiting {seconds_left} seconds before posting first post")
    await asyncio.sleep(seconds_left)