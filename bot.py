import discord
from main import game_function, create_gifs, Choice
from discord.ext import commands
from time import sleep
import os
import json

import functools
import typing
import asyncio

nmb_storage_gif = 4
path_gifs = 'gifs_storage'

# execute sync funct in async programe 
def to_thread(func : typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

default_intend = discord.Intents.all()
bot = commands.Bot(intents=default_intend, command_prefix="!")

@bot.event
async def on_ready():
    print("Le bot est prêt !")

@bot.command(name="simulate")
async def simulate(ctx):

    embed = discord.Embed(
        title="Paper Rock Scissors Simulator",
        color= discord.Color.orange()
    )
    with open('score_save.json', 'r') as file: dict_games = json.load(file)
    with open('score_save.json', 'w') as file:
        if len(dict_games) > 0:
            dict_games = await game_generate(ctx, embed, dict_games)
        else : 
            await no_game_generate(ctx, embed)
        json.dump(dict_games, file)

async def no_game_generate(ctx, embed):

    embed.set_author(name="MatthisDev")
    embed.add_field(name="0 game : ", value="!generate to generate new games")
    await ctx.send(embed=embed)

async def game_generate(ctx, embed, dict_games):
    game_select = None

    for game in dict_games:
        game_select = game
        break

    game_choose_file = discord.File(game_select, filename="image.gif")
    embed.set_author(name="MatthisDev")
    embed.add_field(name="Winner :", value=dict_games[game_select], inline=True)
    embed.set_image(url="attachment://image.gif")

    await ctx.send(embed=embed, file=game_choose_file)
    dict_games.pop(game_select)
    os.remove(game_select)

    return dict_games

@bot.command(name="info")
async def checking_files(ctx):
    nmb_files = len(os.listdir(path_gifs))
    embed = discord.Embed(
        title="Paper Rock Scissors Simulator",
        color= discord.Color.orange()
    )
    embed.add_field(name="games generates : ", value=str(nmb_files), inline=False)
    embed.add_field(name="Commands :", value="!generate --- !simulate", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="generate")
async def game_generator_cmd(ctx):

    nmb_games_need = nmb_storage_gif - len(os.listdir('gifs_storage'))

    embed = discord.Embed(
        title="Paper Rock Scissors Simulator",
        color= discord.Color.orange()
        )
    if nmb_games_need == 0:
        embed.add_field(name="Status :", value="full", inline=True)
    else: 
        embed.add_field(name="Status :", value="start", inline=True)

    embed.add_field(name="Generate :", value=str(nmb_games_need), inline=True)

    await ctx.send(embed=embed)
    embed_ = await generate_game(nmb_games_need)
    await ctx.send(embed=embed_)

@to_thread
def generate_game(nmb_games_need):
    
    with open("score_save.json", "r") as file:
        JSON_data = json.load(file)
    with open("score_save.json", "w") as file:
        for _ in range(0, nmb_games_need):
            winner, name = game_function()

            if not JSON_data.get(name):
                JSON_data[name] = winner
            else : 
                print("already exist")
                new_name = name[:-4] + "045" + ".gif"
                os.rename(name, new_name)

        embed = discord.Embed(
            title="Paper Rock Scissors Simulator",
            color= discord.Color.orange()
        )
        embed.add_field(name="Status", value="end", inline=True)
        embed.add_field(name="Generate :", value=str(nmb_games_need), inline=True)
    
        json.dump(JSON_data, file)

    return embed

bot.run("MTAyMTQ1Njc5ODk3NDIyMjMzNg.GrvhEs.sgEedxPy-7uXNhTTqUppqs6zhjf1JHZQ1vfqMY")