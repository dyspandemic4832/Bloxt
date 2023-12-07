import interactions
import interactions.api.events
import asyncio
from addons.jsonimport import JsonImport

JI = JsonImport("dev_config.json")

global balance
global pending_balance
global transaction_number

balance = 3
transaction_number:int = 1
pending_balance = []

def guild_id():
    return JI.get_value_from_key("GUILD_ID")

def addToPending(transaction_number, number, user):
    global pending_balance
    pending_balance.append((transaction_number, number, user))
    
def addToBalance(number):
    global balance
    balance += number
    
def retrieve_transaction_number():
    global transaction_number
    current_transaction_number = transaction_number
    transaction_number += 1
    return current_transaction_number
    
def verify_pending(transaction_number):
    global pending_balance
    success = False
    
    for i in pending_balance:
        if i[0] == transaction_number:
            success = True
            addToBalance(i[1])
            pending_balance.remove(i)
            break
        elif success == True:
            break
    
    return success
    
def retreiveBalance():
    global balance
    return balance

def retreivePendingBalance():
    global pending_balance
    sum_pending_balance = 0
    for i in pending_balance:
        sum_pending_balance += i[1]
    return sum_pending_balance

### COG Avertax ###
class Avertax(interactions.Extension):
    
    #### /avertax ####
    @interactions.slash_command(
        "avertax", description="Avertax's Commands", scopes=[guild_id()]
    )
    async def avertax(self, ctx: interactions.SlashContext):
        
        await ctx.send("Avertax's Discord Server:\nhttps://discord.gg/kDFe42CQsm\nFeatures for that Community Server:\n1. Org Kassenmanagement\n")
    
    #### /einzahlen ####
    @interactions.slash_command("einzahlen", description="A command with options", scopes=[guild_id()])
    @interactions.slash_option(
        "auec",
        "alphaUnitedEarthCredits",
        opt_type=interactions.OptionType.INTEGER,
        required=True,
    )
    @interactions.slash_option(
        "verwendungszwecken",
        "Hier kannst du einen Verwendungszweck angeben",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def einzahlen(
        self,
        ctx: interactions.SlashContext,
        auec: int,
        verwendungszwecken: str = None,
    ):
        transaction_num = retrieve_transaction_number()
        
        """A command with lots of options"""
        embed = interactions.Embed(
            "Transaktion ausstehend!",
            description="Warte auf die Bestätigung des Kassenwarts!",
            color=interactions.BrandColors.YELLOW,
        )
        embed.add_field(
            "Transaktionsnummer:",
            str(transaction_num),
            inline=False,
        )
        embed.add_field(
            "Einzahlungsbetrag:",
            str(auec),
            inline=False,
        )
        if verwendungszwecken != None:
            embed.add_field(
                "Verwendungszweck:",
                verwendungszwecken,
                inline=False,
            )
        addToPending(transaction_num, auec, ctx.author)
        await ctx.send(embed=embed)
    
    #### /kontostand ####
    @interactions.slash_command("kontostand", description="Gibt das Vermächtniss der Orgakasse aus", scopes=[guild_id()])
    async def kontostand(
        self,
        ctx: interactions.SlashContext,
    ):
        Orgakasse = retreiveBalance()
        Ausstehend = retreivePendingBalance()
        
        embed = interactions.Embed(
            "Orgakassenstand",
            description="Übersicht über den Orgakassenstand",
            color=interactions.BrandColors.BLURPLE,
        )
        embed.add_field(
            "Orgakassenstand:",
            str(Orgakasse),
            inline=False,
        )
        embed.add_field(
            "Ausstehend:",
            str(Ausstehend),
            inline=False,
        )
        await ctx.send(embed=embed)

    #### /verify ####
    @interactions.slash_command("verify", description="Verifiziere eine Transaktion", scopes=[guild_id()])
    @interactions.slash_option(
        "transaktionsnummer",
        "gebe die Transaktionsnummer an",
        opt_type=interactions.OptionType.INTEGER,
        required=True,
    )
    async def verify(
        self,
        ctx: interactions.SlashContext,
        transaktionsnummer: int,
    ):
        embed = interactions.Embed(
            "",
            description="Die Transaktion: '" + str(transaktionsnummer),
        )
        
        if verify_pending(transaktionsnummer) is True:
            embed.title = "Transaktion erfolgreich!"
            embed.description += "' wurde erfolgreich verifiziert!"
            embed.color=interactions.BrandColors.BLURPLE
            
            embed.add_field(
            "neuer Orgakassenstand:",
            str(retreiveBalance()),
            inline=False,
            )
        else:
            embed.title = "Transaktion fehlgeschlagen!"
            embed.description += "' wurde nicht gefunden!"
            embed.color=interactions.BrandColors.RED
        
        print(ctx.author)
        
        await ctx.send(embed=embed)
        
    #### /ausstehend ####
    @interactions.slash_command("ausstehend", description="Listet ausstehende Transaktionen an", scopes=[guild_id()])
    async def ausstehend(
        self,
        ctx: interactions.SlashContext,
    ):
        embed = interactions.Embed(
            "Ausstehende Transaktionen",
            description="Liste aller ausstehenden Transaktionen",
            color=interactions.BrandColors.GREEN,
        )
        
        embed.add_field(
                "aktueller Orgakassenstand:",
                str(retreiveBalance()),
                inline=False,
            )
        if pending_balance != []:
            for i in pending_balance:
                embed.add_field(
                    "Transaktionsnummer:",
                    str(i[0]),
                    inline=True,
                )
                embed.add_field(
                    "Betrag:",
                    str(i[1]),
                    inline=True,
                )
                embed.add_field(
                    "User:",
                    str(i[2]),
                    inline=True,
                )
        else:
            embed.add_field(
                "Keine ausstehenden Transaktionen",
                "Es gibt keine ausstehenden Transaktionen",
                inline=False,
            )
        
        await ctx.send(embed=embed)