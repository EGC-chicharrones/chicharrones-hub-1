import discord
import os
import app

from discord.ext import commands
from app.discord.embed import help_embed, help_embed_slash


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
                      description="Sends a list of the 5 latest datasets. Not a final implementation.")
    async def slash_latest_datasets(interaction: discord.Interaction):
        # TODO: Pass data to an embed builder and add paging.
        from app.modules.dataset.repositories import DataSetRepository
        with ap.app_context():
            repo = DataSetRepository()
            datasets = DataSetRepository.latest_synchronized(repo)
            message = "\n".join(f"Dataset with ID {dataset.id}: {dataset.name()}" for dataset in datasets)
            await interaction.response.send_message(message)

    bot.run(token)
