from typing import Literal
from enum import Enum
import discord
import os
import app

from discord.ext import commands
from app.discord.embed import dataset_embed_slash, default_embed, help_embed, help_embed_slash
from app.discord.pagination import Pagination


def start_bot(name):
    # It is necessary to initialise the Flask app to be able to interact with it.
    # This will allow us to use repositories, services, and so forth.
    ap = app.create_app()

    token = os.getenv("DISCORD_TOKEN")
    bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        # TODO: Change this with a useful message
        await bot.change_presence(activity=discord.Activity
                                  (type=discord.ActivityType.listening, name="Rhapsody of Fire"))
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally.")
        print('------')

    @bot.command()
    async def intro(ctx):
        """Shows an introduction to uvlhub and commands to get started."""
        await ctx.send(embed=help_embed(ctx))

    @bot.tree.command(name="intro", description="Shows an introduction to uvlhub and commands to get started.")
    async def slash_intro(interaction: discord.Interaction):
        await interaction.response.send_message(embed=help_embed_slash(interaction))

    @bot.tree.command(name="latest_datasets",
                      description="Sends a list of the 5 latest datasets.")
    async def slash_latest_datasets_page(interaction: discord.Interaction):
        from app.modules.dataset.repositories import DataSetRepository
        from app.modules.profile.models import UserProfile

        async def get_page(page: int):
            emb = embeds[page-1]
            n = len(datasets)
            emb.set_footer(text=f"UVLHUB.IO • Page {page} from {n}", icon_url="https://www.uvlhub.io/static/img/icons/icon-250x250.png")
            return emb, n
        
        with ap.app_context():
            repo = DataSetRepository()
            datasets = DataSetRepository.latest_synchronized(repo)
            embeds = []
            for dataset in datasets:
                user_profile = UserProfile.query.filter_by(user_id=dataset.user_id).first()
                embeds.append(dataset_embed_slash(interaction, dataset, user_profile))
            if len(embeds) == 0:
                await interaction.response.send_message(embed=default_embed(
                    "We have not found any datasets. This most likely means that there are none in the database.", "No datasets found"))
            await Pagination(interaction, get_page).navigate()
    
    # Make a new publication_type enum that includes Any,
    # as this is not meant to be included in the original enum,
    # but is necessary for the bot.
    from app.modules.dataset.models import PublicationType

    types = ['ANY'] + [t.name for t in PublicationType]
    PublicationType = Enum('PublicationType', types)

    @bot.tree.command(name="search_datasets",
                      description="Search for datasets by title, description, authors, tags, UVL files...")
    async def slash_search_datasets(interaction: discord.Interaction, query: str, sorting: Literal["newest", "oldest"], publication_type: PublicationType):
        from app.modules.explore.repositories import ExploreRepository
        from app.modules.profile.models import UserProfile

        async def get_page(page: int):
            emb = embeds[page-1]
            n = len(datasets)
            emb.set_footer(text=f"UVLHUB.IO • Page {page} from {n}", icon_url="https://www.uvlhub.io/static/img/icons/icon-250x250.png")
            return emb, n
        
        with ap.app_context():
            repo = ExploreRepository()
            datasets = ExploreRepository.filter(repo, query, sorting, publication_type.name.lower())
            embeds = []
            for dataset in datasets:
                user_profile = UserProfile.query.filter_by(user_id=dataset.user_id).first()
                embeds.append(dataset_embed_slash(interaction, dataset, user_profile))
            if len(embeds) == 0:
                await interaction.response.send_message(embed=default_embed(
                    "We have not found any datasets that meet your search criteria. How about trying some others?", "No datasets found"))
            else:
                await Pagination(interaction, get_page).navigate()

    bot.run(token)
