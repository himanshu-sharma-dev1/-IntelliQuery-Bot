import discord
from discord.ext import commands
import logging
import os
import asyncio

from src.core.config import DISCORD_BOT_TOKEN, COMMAND_PREFIX, LOG_LEVEL, LOG_FILE

# --- Logging Setup ---
logger = logging.getLogger('discord')
logger.setLevel(LOG_LEVEL)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# --- Bot Initialization ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(COMMAND_PREFIX), intents=intents, help_command=None, owner_id=672703712166281217)
bot.logger = logger

@bot.event
async def on_ready():
    """Event that fires when the bot is ready."""
    logger.info(f'Logged in as {bot.user}')
    logger.info('Bot is ready and online.')

@bot.group()
@commands.guild_only()
@commands.is_owner()
async def faq(ctx: commands.Context):
    """A group of commands for managing the FAQ."""
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid faq command passed...')

@faq.command(name='sync')
async def faq_sync(ctx: commands.Context):
    """Syncs slash commands with Discord."""
    synced = await ctx.bot.tree.sync()
    logger.info(f"Synced {len(synced)} commands globally.")
    await ctx.send(f"Synced {len(synced)} commands.")

async def load_cogs():
    """Loads all cogs from the cogs directory."""
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'src.cogs.{filename[:-3]}')
                logger.info(f'Loaded cog: {filename}')
            except Exception as e:
                logger.error(f'Failed to load cog {filename}: {e}')

async def main():
    """Main function to run the bot."""
    if not DISCORD_BOT_TOKEN:
        logger.error("FATAL: DISCORD_BOT_TOKEN environment variable not set.")
        return

    async with bot:
        await load_cogs()
        await bot.start(DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shut down by user.")