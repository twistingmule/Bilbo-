import discord
from discord.ext import commands
import os
import openai

# Set OpenRouter API key and base URL
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def ask(ctx, *, question):
    await ctx.trigger_typing()
    try:
        response = openai.ChatCompletion.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",  # changeable depending on what's available to you
            messages=[
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content.strip()
        await ctx.send(answer[:2000])  # Truncate if too long for Discord
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

bot.run(os.getenv("DISCORD_TOKEN"))
