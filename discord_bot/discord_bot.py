from discord.ext import commands
import discord
import os
import random
from db_calls.sith import sith_plan
from db_calls.update_roster import update_roster
from db_calls.how_many import get_number
from db_calls.planet_check import planet_check
from db_calls.ops_check import ops_check
from db_calls.jedi import jedi_plan
from db_calls.planets import planets_check
from db_calls.rare import rare_plan
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
async def send_message(ctx, message):
    print("ping")
    if str(ctx.channel) == "bot_test" or str(ctx.channel) == "swgoh-bot-channel":
        x = message
        if len(x) <= 2000:
            await ctx.send(x)
        else:
            chunks = [x[i:i+2000] for i in range(0, len(x), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)

@bot.command()
async def list(ctx, what_list):
    if what_list == "planets":
        x = 'Mustafar, Corellia, Coruscant, Geonosis, Felucia, Bracca, Dathomir, Tatooine, Kashyyyk, Zeffo, Haven-class Medical Station, Kessel, Lothal, Malachor, Vandor, Ring of Kafrene, Death Star, Hoth, Scarif'
    await send_message(ctx, x)

@bot.command()
async def how_many(ctx,relic_level, unit_name):
    x = get_number(relic_level, unit_name)
    await send_message(ctx, x)

@bot.command()
async def planet(ctx,planet_name, all=True):
    x = planet_check(planet_name, all)
    await send_message(ctx, x)

@bot.command()
async def planets(ctx,planet1, planet2, all=True):
    x = planets_check(planet1, planet2, all)
    await send_message(ctx, x)

@bot.command()
async def ops(ctx,planet_name):
    x = ops_check(planet_name)
    await send_message(ctx, x)

@bot.command()
async def sith(ctx):
    x = sith_plan()
    await send_message(ctx, x)

@bot.command()
async def jedi(ctx):
    x = jedi_plan()
    await send_message(ctx, x)


@bot.command()
async def rare(ctx):
    x = rare_plan()
    await send_message(ctx, x)

@bot.command()
async def update(ctx):
    await send_message(ctx, "This takes like 30 seconds")
    update_roster()
    await send_message(ctx, "guild updated")

@bot.command()
async def Ezls(ctx, crate):
    if crate.lower() == "crate":
        phrases = ["Knock, knock!","SteveO, is that you?!","Ax Brad, he’ll know what to do.",
                   "DILLY, DILLY!!","Is that babe @vpukam8621 still hanging around….oh, hey!",
                   "Yes, I’m!","Wanna here a guud joke?!", "https://tenor.com/3qw8.gif", 
                   "https://tenor.com/RJkK.gif",
                   "https://tenor.com/view/who-is-you-talking-looking-who-are-you-talking-about-look-up-gif-15744968"]
        
        x = random.choice(phrases)
        await send_message(ctx, x)

bot.run(BOT_TOKEN)