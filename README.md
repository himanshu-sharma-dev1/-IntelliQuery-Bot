# IntelliQuery Bot

This is a professional, deployment-ready Discord bot that provides intelligent answers to user questions. It uses a local FAQ file for instant, accurate responses and leverages Google's Gemini 1.5 Flash model for questions it doesn't know, ensuring no query goes unanswered. The entire application is containerized with Docker, making it easy to deploy and run 24/7.

## Features & Skills Demonstrated

*   **Containerization:** Fully containerized with Docker and Docker Compose for easy, one-command deployment.
*   **AI Integration:** Connected to Google's Gemini 1.5 Flash model for intelligent, fallback responses.
*   **Modern Discord API:** Utilizes modern Slash Commands (`/ask`, `/list`) and rich Embeds for a clean user experience.
*   **Scalable Architecture:** Built with a modular Cogs system to allow for easy feature expansion.
*   **Secure Configuration:** Manages sensitive API keys and tokens using a `.env` file, which is kept private via `.gitignore`.
*   **Dynamic Content Management:** Includes an owner-only command (`!faq add`) to update the FAQ without needing to edit code or restart the bot.

## Tech Stack

*   **Language:** Python 3.12
*   **Libraries:**
    *   `discord.py`: For Discord API interaction.
    *   `google-generativeai`: For connecting to the Gemini AI model.
    *   `python-dotenv`: For managing environment variables.
*   **Deployment:** Docker & Docker Compose

## How to Run

**1. Prerequisites:**
*   Git
*   Python 3.8+
*   Docker Desktop

**2. Clone the Repository:**
```bash
git clone https://github.com/himanshu-sharma-dev1/-IntelliQuery-Bot.git
cd -IntelliQuery-Bot
```

**3. Configure Your Secrets:**
*   Rename the `.env.example` file to `.env`.
*   Open the `.env` file and paste in your actual `DISCORD_BOT_TOKEN` and `GEMINI_API_KEY`.

**4. Build and Run the Bot:**
Make sure Docker Desktop is running, then run the following command:
```bash
docker-compose up --build -d
```

**5. Invite the Bot & Sync Commands:**
*   Use the OAuth2 URL Generator in the Discord Developer Portal to create an invite link. You will need the `bot` and `applications.commands` scopes.
*   Once the bot is in your server, run `!faq sync` one time to register the slash commands.

The bot is now fully operational!
