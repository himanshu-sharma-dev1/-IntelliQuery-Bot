import discord
from discord import app_commands
from discord.ext import commands
import logging

from src.core.config import FAQ_FILE_PATH
from src.utils.faq_parser import write_faq

# Get the logger from the main bot file
logger = logging.getLogger('discord')

# --- Modal for Editing FAQs ---
class EditFaqModal(discord.ui.Modal):
    def __init__(self, bot: commands.Bot, question: str, answer: str):
        super().__init__(title=f"Edit FAQ: {question[:250]}")
        self.bot = bot
        self.question = question
        self.answer_input = discord.ui.TextInput(
            label="Answer",
            style=discord.TextStyle.paragraph,
            default=answer,
            max_length=1024,  # Embed description limit
        )
        self.add_item(self.answer_input)

    async def on_submit(self, interaction: discord.Interaction):
        faq_cog = self.bot.get_cog('FaqCog')
        if not faq_cog:
            return await interaction.response.send_message("FAQ system not ready. Please try again later.", ephemeral=True)

        new_answer = self.answer_input.value
        faq_cog.faq[self.question] = new_answer

        try:
            write_faq(faq_cog.faq, FAQ_FILE_PATH)
            logger.info(f"FAQ '{self.question}' edited by {interaction.user}.")
            await interaction.response.send_message(f"Successfully updated the FAQ: **{self.question}**", ephemeral=True)
        except Exception as e:
            logger.error(f"Error writing FAQ file after editing '{self.question}': {e}")
            # Reload to revert in-memory changes if save fails
            await self.bot.reload_extension('src.cogs.faq_cog')
            await interaction.response.send_message("An error occurred while saving the changes. The FAQ has been reverted.", ephemeral=True)


class AdminCog(commands.Cog):
    """A cog for admin-only commands to manage the FAQ."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Autocomplete function for FAQ questions
    async def faq_question_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        faq_cog = self.bot.get_cog('FaqCog')
        if not faq_cog:
            return []
        
        questions = faq_cog.faq.keys()
        
        # Provide some initial choices if the user hasn't typed anything
        if not current:
            return [
                app_commands.Choice(name=q[:100], value=q)
                for q in list(questions)[:25]
            ]

        # Filter choices based on user input
        return [
            app_commands.Choice(name=q[:100], value=q)
            for q in questions if current.lower() in q.lower()
        ][:25]

    @app_commands.command(name="edit", description="Edits the answer to an FAQ question.")
    @app_commands.describe(question="The question to edit the answer for.")
    @app_commands.autocomplete(question=faq_question_autocomplete)
    @app_commands.checks.has_role("Admin")
    async def edit_faq(self, interaction: discord.Interaction, question: str):
        """Edits an existing FAQ question's answer."""
        faq_cog = self.bot.get_cog('FaqCog')
        if not faq_cog or question not in faq_cog.faq:
            return await interaction.response.send_message("This question does not exist in the FAQ.", ephemeral=True)

        current_answer = faq_cog.faq[question]
        modal = EditFaqModal(self.bot, question, current_answer)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="delete", description="Deletes a question from the FAQ.")
    @app_commands.describe(question="The full question to delete.")
    @app_commands.autocomplete(question=faq_question_autocomplete)
    @app_commands.checks.has_role("Admin")
    async def delete_faq(self, interaction: discord.Interaction, question: str):
        """Deletes a question from the FAQ."""
        faq_cog = self.bot.get_cog('FaqCog')
        if not faq_cog:
            return await interaction.response.send_message("FAQ system not ready. Please try again later.", ephemeral=True)

        if question not in faq_cog.faq:
            return await interaction.response.send_message("This question does not exist in the FAQ.", ephemeral=True)

        # Remove the question from the in-memory dictionary
        del faq_cog.faq[question]

        try:
            # Write the updated dictionary back to the file
            write_faq(faq_cog.faq, FAQ_FILE_PATH)
            logger.info(f"FAQ '{question}' deleted by {interaction.user}.")
            await interaction.response.send_message(f"Successfully deleted the FAQ: **{question}**", ephemeral=True)
        except Exception as e:
            logger.error(f"Error writing FAQ file after deleting '{question}': {e}")
            await self.bot.reload_extension('src.cogs.faq_cog')
            await interaction.response.send_message("An error occurred while saving the changes. The FAQ has been reverted.", ephemeral=True)

    @app_commands.command(name="add", description="Adds a new question and answer to the FAQ.")
    @app_commands.describe(question="The new question to add.", answer="The answer to the new question.")
    @app_commands.checks.has_role("Admin")
    async def add_faq(self, interaction: discord.Interaction, question: str, answer: str):
        """Adds a new question and answer to the FAQ."""
        faq_cog = self.bot.get_cog('FaqCog')
        if not faq_cog:
            return await interaction.response.send_message("FAQ system not ready. Please try again later.", ephemeral=True)

        if question in faq_cog.faq:
            return await interaction.response.send_message(
                f"This question already exists. Use `/edit` to change it.",
                ephemeral=True
            )

        # Add the new question to the in-memory dictionary
        faq_cog.faq[question] = answer

        try:
            # Write the updated dictionary back to the file
            write_faq(faq_cog.faq, FAQ_FILE_PATH)
            logger.info(f"New FAQ '{question}' added by {interaction.user}.")
            await interaction.response.send_message(f"Successfully added the new FAQ: **{question}**", ephemeral=True)
        except Exception as e:
            logger.error(f"Error writing FAQ file after adding '{question}': {e}")
            # If saving fails, remove the question from the in-memory dict to revert the change
            del faq_cog.faq[question]
            await interaction.response.send_message("An error occurred while saving the new FAQ. Please try again.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
