import interactions
from addons.jsonimport import JsonImport

JI = JsonImport("dev_config.json")

class Avertax(interactions.Extension):
    
    @interactions.slash_command(
        "communityserver", description="Communityserver's Commands", scopes=[JI.get_value_from_key("GUILD_ID")]
    )
    
    async def avertax(self, ctx: interactions.SlashContext):
        
        await ctx.send("Communityserver's Discord Server:\nhttps://discord.gg/sVCyxhndSt\nCommands for that Community Server:\n")
    
    @interactions.user_context_menu(name="ping")
    async def ping(ctx: interactions.ContextMenuContext):
        member: interactions.Member = ctx.target
        await ctx.send(member.mention)