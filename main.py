import discord
from discord.ext import commands
import os
import openai

# Setup OpenRouter credentials
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Discord bot setup with required intents
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
async def ask(ctx, *, question=None):
    if not question:
        await ctx.send("❗ You need to ask a question, like:\n`!ask What is the meaning of life?`")
        return

    async with ctx.channel.typing():  # ✅ Correct typing usage
        try:
            response = openai.ChatCompletion.create(
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",  # Or another OpenRouter model
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            await ctx.send(answer[:2000])  # Truncate long responses for Discord
        except Exception as e:
            await ctx.send(f"⚠️ Error: {str(e)}")

bot.run(os.getenv("DISCORD_TOKEN"))
