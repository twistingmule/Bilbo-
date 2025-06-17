import os
import threading
import discord
from discord.ext import commands
from OpenAI import OpenAI
from Flask import Flask

# --- OpenRouter Client Setup (using SDK ≥ 1.0.0) ---
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

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
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
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
