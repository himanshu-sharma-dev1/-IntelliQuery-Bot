import discord
from discord import app_commands
from discord.ext import commands
from thefuzz import process
import google.generativeai as genai

from src.utils.faq_parser import parse_faq
from src.core.config import FAQ_FILE_PATH, GEMINI_API_KEY

class FaqCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.faq = parse_faq(FAQ_FILE_PATH)
        genai.configure(api_key=GEMINI_API_KEY)

    @app_commands.command(name="list", description="Lists all available FAQ questions.")
    async def list_questions(self, interaction: discord.Interaction):
        """Lists all available FAQ questions."""
        if self.faq:
            question_list = "\n".join(sorted(self.faq.keys()))
            embed = discord.Embed(
                title="Available FAQ Questions",
                description=f"```\n{question_list}\n```",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("I don't have any questions in my FAQ at the moment.", ephemeral=True)

    @app_commands.command(name="ask", description="Answers a question from the FAQ or uses AI as a fallback.")
    @app_commands.describe(question="The question you want to ask.")
    async def ask_question(self, interaction: discord.Interaction, question: str):
        """Answers a question from the FAQ or uses Gemini as a fallback."""
        # Defer the response to show a "thinking" state, as Gemini can be slow
        await interaction.response.defer()

        # First, check for an exact match
        if question in self.faq:
            embed = discord.Embed(
                title=question,
                description=self.faq[question],
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed)
            return

        # If no exact match, use fuzzy matching
        match = process.extractOne(question, self.faq.keys(), score_cutoff=90)

        if match:
            matched_question, score = match
            self.bot.logger.info(f"Fuzzy match for '{question}': '{matched_question}' with score {score}")
            embed = discord.Embed(
                title=f"Did you mean: '{matched_question}'?",
                description=self.faq[matched_question],
                color=discord.Color.orange()
            )
            await interaction.followup.send(embed=embed)
        else:
            # Fallback to Gemini API
            self.bot.logger.info(f"No suitable FAQ found for '{question}'. Asking Gemini...")
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"You are a helpful FAQ bot. Provide a helpful answer to the following question: '{question}'"
                response = await model.generate_content_async([prompt])

                if response.parts:
                    embed = discord.Embed(
                        title="Answer from my AI Assistant",
                        description=response.text,
                        color=discord.Color.purple()
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    self.bot.logger.warning(f"Gemini response was blocked. Feedback: {response.prompt_feedback}")
                    embed = discord.Embed(
                        title="Error",
                        description="My AI capabilities are restricted for that question.",
                        color=discord.Color.red()
                    )
                    await interaction.followup.send(embed=embed)

            except Exception as e:
                self.bot.logger.error(f"Error generating response from Gemini: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="I couldn't connect to the AI service.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FaqCog(bot))
