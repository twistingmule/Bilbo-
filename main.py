import os
import threading
import discord
from discord.ext import commands
import openai
from flask import Flask

# --- OpenRouter Client Setup ---
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.base_url = "https://openrouter.ai/api/v1"

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def ask(ctx, *, question=None):
    if not question:
        await ctx.send("❗ You need to ask a question, like:\n`!ask What is the meaning of life?`")
        return

    async with ctx.channel.typing():
        try:
            response = openai.chat.completions.create(
                model="meta-llama/llama-4-scout:free",
                messages=[{"role": "user", "content": question}]
            )
            answer = response.choices[0].message.content.strip()
            await ctx.send(answer[:2000])
        except Exception as e:
            await ctx.send(f"⚠️ Error: {str(e)}")

# --- Flask Setup for Render Health Check ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord Bot is running!"

def run_bot():
    bot.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
