import discord
from discord.ext import commands
import logging

from src.core.config import FAQ_FILE_PATH
from src.utils.faq_parser import parse_faq

# Get the logger from the main bot file
logger = logging.getLogger('discord')

class AdminCog(commands.Cog):
    """A cog for admin-only commands to manage the FAQ."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add")
    @commands.has_role("Admin")  # Restricts this command to users with the "Admin" role
    async def add_faq(self, ctx, *, content: str):
        """Adds a new question and answer to the FAQ. Usage: !faq add <question> | <answer>"""
        try:
            question, answer = [item.strip() for item in content.split('|', 1)]
        except ValueError:
            await ctx.send("Invalid format. Please use: `!faq add <question> | <answer>`")
            return

        # Append the new Q&A to the FAQ.md file
        with open(FAQ_FILE_PATH, 'a', encoding='utf-8') as f:
            # Ensure there are newlines before the new entry
            f.write(f"\n\n## {question}\n{answer}")
        
        logger.info(f"New FAQ added by {ctx.author}: '{question}'")
        
        # Reload the FaqCog to update its internal FAQ dictionary
        try:
            await self.bot.reload_extension('src.cogs.faq_cog')
            logger.info("FaqCog reloaded successfully.")
            await ctx.send(f"Successfully added the new FAQ: **{question}**")
        except Exception as e:
            logger.error(f"Failed to reload FaqCog: {e}")
            await ctx.send("FAQ added, but a restart may be needed for it to become active.")

    @add_faq.error
    async def add_faq_error(self, ctx, error):
        """Error handler for the add_faq command."""
        if isinstance(error, commands.MissingRole):
            await ctx.send("Sorry, you don't have the required 'Admin' role to use this command.")
        else:
            await ctx.send("An unexpected error occurred. Please check the logs.")
            logger.error(f"Error in add_faq command: {error}")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
