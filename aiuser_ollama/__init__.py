from .aiuser_ollama import AiUserOllama

async def setup(bot):
    await bot.add_cog(AiUserOllama(bot))
