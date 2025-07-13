import discord
from redbot.core import commands, Config
import aiohttp
import asyncio

class AiUserOllama(commands.Cog):
    """Talk with a local AI model using Ollama"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def ai(self, ctx, *, prompt: str):
        """Ask your local Ollama AI something"""
        await ctx.trigger_typing()

        ollama_url = "http://localhost:11434/api/generate"
        model_name = "llama3"  # Change to whatever model is installed on your Ollama instance

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            async with self.session.post(ollama_url, json=payload) as resp:
                if resp.status != 200:
                    await ctx.send(f"❌ Error: Ollama server returned status {resp.status}")
                    return

                data = await resp.json()
                response = data.get("response", "⚠️ No response from Ollama.")
                await ctx.send(response[:2000])  # Discord message limit
        except Exception as e:
            await ctx.send(f"❌ Exception occurred: {e}")

    def cog_unload(self):
        asyncio.create_task(self.session.close())
