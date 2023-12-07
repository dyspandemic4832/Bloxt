import interactions
from addons.jsonimport import JsonImport

JI = JsonImport("dev_config.json")

class PingCog(interactions.Extension):
    @interactions.slash_command(
        "ping", description="Simple Ping Commands", scopes=[JI.get_value_from_key("GUILD_ID")]
    )
    async def test_cmd(self, ctx: interactions.SlashContext):
        await ctx.send("Pong!")
        
    