import discord
import asyncio
from discord.ext import commands
import os

from myserver import server_on

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

allowed_channel_id = 1357168494810103919

channel_ids = [1357145310262071525, 1357147666953535570]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def move(ctx, member: discord.Member, move_times: int):

    if ctx.channel.id != allowed_channel_id:

        message = await ctx.send(f"{ctx.author.mention} มึงใช้ผิดห้องไอควาย",delete_after=5)

        await ctx.message.delete()
        return

    try:
        await ctx.message.delete()

        if member.voice:

            start_channel = member.voice.channel

            for _ in range(move_times):
                for channel_id in channel_ids:

                    channel = bot.get_channel(channel_id)

                    if isinstance(channel, discord.VoiceChannel):
                        await member.move_to(channel)
                        await asyncio.sleep(1)

            if isinstance(start_channel, discord.VoiceChannel):
                await member.move_to(start_channel)

            message = await ctx.send(
                f'{ctx.author.mention} You have done poke {member.mention}'
            )

            await asyncio.sleep(60)
            await message.delete()

        else:
            await ctx.send(f'{member.mention} is not in a voice channel.')

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

server_on

bot.run(os.getenv('TOKEN'))