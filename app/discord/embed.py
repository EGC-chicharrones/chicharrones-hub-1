import discord
from discord.ext import commands
import datetime

def help_embed(ctx):
    embed = discord.Embed(title="Introduction", colour=discord.Colour(0x78dd1), description=f"Hello, {ctx.author.display_name}! Let's get started on using the bot:", timestamp=datetime.datetime.now())

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="UVLHUB.IO", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="What is uvlhub.io?", value="uvlhub is a repository of feature models in UVL format integrated with Zenodo and flamapy following Open Science principles.\n\nIt is a project developed by DiversoLab and made possible thanks to the efforts of researchers from the University of Seville, University of Malaga and University of Ulm.")
    embed.add_field(name="What is it for?", value="With uvlhub, you can search, download and upload datasets and feature models.")
    embed.add_field(name="What is this bot for?", value="This Discord bot aims to bring the core functionality of uvlhub right to your Discord server. Look up datasets, download UVL files, and much more!\n\nNote: some features may require you to log in with your uvlhub account.")

    return embed


def help_embed_slash(interaction: discord.Interaction):
    embed = discord.Embed(title="Introduction", colour=discord.Colour(0x78dd1), description=f"Hello, {interaction.user.mention}! Let's get started on using the bot:", timestamp=datetime.datetime.now())

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="UVLHUB.IO", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="What is uvlhub.io?", value="uvlhub is a repository of feature models in UVL format integrated with Zenodo and flamapy following Open Science principles.\n\nIt is a project developed by DiversoLab and made possible thanks to the efforts of researchers from the University of Seville, University of Malaga and University of Ulm.")
    embed.add_field(name="What is it for?", value="With uvlhub, you can search, download and upload datasets and feature models.")
    embed.add_field(name="What is this bot for?", value="This Discord bot aims to bring the core functionality of uvlhub right to your Discord server. Look up datasets, download UVL files, and much more!\n\nNote: some features may require you to log in with your uvlhub account.")

    return embed


def default_embed(ctx, desc, title="UVLHUB.IO", name=None, field_desc=None, thumbnail=False):
    embed = discord.Embed(title=title, colour=discord.Colour(0x78dd1), description=desc, timestamp=datetime.datetime.now())

    if thumbnail: # TODO: Replace with uvlhub logo
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="UVLHUB.IO", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    if name and field_desc:
        embed.add_field(name=name, desc=field_desc)
    
    return embed