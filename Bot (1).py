import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
from discord.ui import View, Button

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
mentions = discord.AllowedMentions(everyone=False, users=True, roles=True, replied_user=True)

default_prefix = "!"
bot = commands.Bot(command_prefix=default_prefix, 
                   intents=intents, 
                   help_command=None, 
                   allowed_mentions=mentions)

prefixes = {}

def get_prefix(bot, message):
    return prefixes.get(message.guild.id, default_prefix)

bot.command_prefix = get_prefix

@bot.event
async def on_guild_join(guild):
    prefixes[guild.id] = default_prefix

@bot.command()
async def test_embed(ctx):
    embed = discord.Embed(
        title="Test",
        description="This is a test embed.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    
@bot.command
async def reviver(ctx: commands.Context):
    await ctx.send("reviving users complete 100%")

@bot.event
async def on_guild_remove(guild):
    prefixes.pop(guild.id, None)

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix: str):
    prefixes[ctx.guild.id] = prefix
    await ctx.send(f"Prefix changed to: {prefix}")

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason: str = None):
    if reason is None:
        await ctx.send("Please provide a reason for the warning.")
        return
    
    embed = discord.Embed(
        title="User Warned",
        description=f"{member.mention} has been warned by {ctx.author.mention}\nReason: {reason}",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(title=f"Avatar of {member.display_name}")
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def cmd(ctx):
    embed_initial = discord.Embed(
        title="List of Commands",
        description=f"Hello {ctx.author.mention}! Here are the list of commands:\n\n"
                    "Click the corresponding button to view commands for that category:\n",
        color=discord.Color.blue()
    )

    view = View()
    buttons = [
        Button(label="Actual Useful Stuff", custom_id="category_1"),
        Button(label="Games", custom_id="category_2"),
        Button(label="Utility (Staff and Higher)", custom_id="category_3"),
        Button(label="Extra", custom_id="category_4")
    ]

    async def button_callback(interaction):
        if interaction.user != ctx.author:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return

        category_id = interaction.data["custom_id"]

        if category_id == "category_1":
            embed_initial.description = "Here are the commands for Actual Useful Stuff category:\n\n" \
                                        "!cmd - opens commands list (this)\n\n" \
                                        "!lmessage - here is where you get messages from the developer\n\n" \
                                        "!poll [topic here] - creates a poll\n\n" \
                                        "!search [input] - basically google search\n\n" \
                                        "!yt [input] - too lazy to open youtube? use this command to search\n\n" \
                                        "!newticket [topic] - creates a new ticket\n\n" \
                                        "!avatar [username] - gets the avatar of the mentioned user\n\n" \
                                        "!ping - is it just your internet lagging or is bot lagging? check it using this command!\n\n" \
                                        "!echo - says hello to you\n\n" \
                                        "!messagecho [message] - bot says the message for you in embedded form\n\n" \
                                        "!membercount - tells you the server member count."

        elif category_id == "category_2":
            embed_initial.description = "Here are the commands for Games category:\n\n" \
                                        "!dice - rolls a single dice\n\n" \
                                        "!roll - gives you 3 random numbers from 1-7"

        elif category_id == "category_3":
            embed_initial.description = "Here are the commands for Utility (Staff and Higher) category:\n\n" \
                                        "!purge [user] - used to mass delete messages\n\n" \
                                        "!warn [user] - warns a user\n\n" \
                                        "!mute [user] - mutes a person (wip)\n\n" \
                                        "!unmute [user] - unmutes a person (wip)\n\n" \
                                        "!kick [user] - kicks a person\n\n" \
                                        "!skick [user] - kicks a person but silently\n\n" \
                                        "!ban [user] - bans a person\n\n" \
                                        "!close - closes a ticket\n\n" \
                                        "!setprefix - sets the prefix to the desired choice"

        elif category_id == "category_4":
            embed_initial.description = "Here are the commands for Extra category:\n\n" \
                                        "!info - the information of the bot\n\n" \
                                        "!credits - list everyone who helped me with the bot\n\n" \
                                        "!contribute - list everything you can do to help me!"

        await interaction.response.edit_message(embed=embed_initial, view=view)

    for button in buttons:
        button.callback = button_callback
        view.add_item(button)

    await ctx.send(embed=embed_initial, view=view)
                           
@bot.command()
async def echo(ctx: commands.Context):
    embed = discord.Embed(
        title="Echo Command",
        description=f"Hello {ctx.author}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def membercount(ctx: commands.Context):
    embed = discord.Embed(title="Member Count", description=f"Member In This Server **{ctx.guild.member_count}**", color=0x00ffff
    )
    await ctx.send (embed=embed)
    
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! 🏓\n ***(round{bot.latency*1000})*** ms**")

@bot.command()
async def dice(ctx: commands.Context):
    embed = discord.Embed(title="🎲 Dice Game 🎲", description=f"You got a {random.randint(1, 6)}. Good job!")
    await embed.set_footer(text=f"Command requested by {ctx.author}")
    await ctx.send (embed=embed)

@bot.command()
async def ban(ctx: commands.Context):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.reply("You don't have enough permissions!")
    if not ctx.message.mentions:
        return await ctx.reply("no users found")
    for user in ctx.message.mentions:
        await user.ban()
        await ctx.reply(f"{user} has been banned!")

@bot.command()
async def kick(ctx: commands.Context):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.reply("You don't have enough permissions!")
    if not ctx.message.mentions:
        return await ctx.reply("no users found")
    for user in ctx.message.mentions:
        await user.kick()
        embed = discord.Embed(title=f"{user} has been kicked!", description=f"Kicked by: {ctx.author}", color=0xa900ff)
        await ctx.send(embed=embed)

@bot.command()
async def skick(ctx: commands.Context):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.reply("You don't have enough permissions!")
    if not ctx.message.mentions:
        return await ctx.reply("no users found")
    for user in ctx.message.mentions:
        await user.kick()

@bot.command()
async def purge(ctx: commands.Context, limit: str):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.reply("You don't have enough permissions!")
    if not limit.isdigit():
        return await ctx.reply("not a digit :(")
    msgs = await ctx.channel.purge(limit=int(limit))
    embed = discord.Embed(title="**Purge**", description=f"**{len(msgs)} messages have been deleted!**", color=0x191919)
    embed.set_footer(text=f"{ctx.author} - {ctx.author.id}")
    if ctx.author.avatar:
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_footer(icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)
    
@bot.command()
async def credits(ctx: commands.Context):
    await ctx.send (
        f"hello {ctx.author}, welcome to the hall of fame!\n"+
        "--------------------------------------------------\n"+
        "here are the people who helped me with the bot!\n"+
        "--------------------------------------------------\n"+
        "gdjkhp - helped me port the code from bds to python and helped me discover a way to host this bot 24/7 for free! (thanks gdjkhp!)\n"+
        "--------------------------------------------------\n"+
        "gato - without his wonderfull server, i wouldnt have started this project, so thank him too!\n"+
        "--------------------------------------------------\n"+
        "list of affiliates:\n"+
        "dannie the dominator in all of africa and who also has 5 bottles of beer in his desk a.k.a <@1149740991117545664>\n"+
        "SpaceFloppa"
)
    
@bot.command()
async def info(ctx: commands.Context):
    await ctx.send (
        f"requested by {ctx.author}.\n"+
        "--------------------------------------------------\n"+
        f"ping: **{round(bot.latency*1000)} ms**\n"+
        "python version: 3.9.19\n"
    )
@bot.command()
async def lmessage(ctx: commands.context):
    await ctx.send ("hello, theres no new message yet.")

@bot.command()
async def contribute(ctx):
    embed = discord.Embed(
        title=f'Hello, {ctx.author.name}!',
        description=("You can contribute by:\n"
                     "--------------------------------------------------\n"
                     "Donating:\n"
                     "Not added yet, next update\n"
                     "--------------------------------------------------\n"
                     "Coding:\n"
                     "Help with some code, make sure to DM me first so I can send the source code\n"
                     "--------------------------------------------------\n"
                     "Affiliating:\n"
                     "You can share affiliate code, DM me proof.\n"
                     "Copy this link: [My affiliate link](https://bot-hosting.net/?aff=864351364771610645)\n"
                     "--------------------------------------------------\n"
                     "Those are all the ways to contribute, DM me proof to get added to the list on !credits\n"
                     ),
        color=0xccff66
    )
    
    embed.set_footer(text=f"Requested by {ctx.author}")
    
    await ctx.send(embed=embed)
                          
bot.run(os.getenv("TOKEN")) # bot token here