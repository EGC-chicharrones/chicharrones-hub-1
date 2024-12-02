import discord
import os
import app

from discord.ext import commands
from app.discord.embed import dataset_embed_slash, help_embed, help_embed_slash
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
        from app.modules.dataset.models import DataSet
        from app.modules.dataset.repositories import DataSetRepository

        async def get_page(page: int):
            emb = embeds[page-1]
            n = len(datasets)
            emb.set_footer(text=f"UVLHUB.IO · Page {page} from {n}", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            return emb, n
        
        with ap.app_context():
            repo = DataSetRepository()
            datasets = DataSetRepository.latest_synchronized(repo)
            embeds = []
            for dataset in datasets:
                embeds.append(dataset_embed_slash(interaction, dataset))
            # await interaction.response.send_message(embed=embeds[0])
            await Pagination(interaction, get_page).navigate()

    bot.run(token)
