import interactions
from addons.jsonimport import JsonImport
import random

JI = JsonImport("dev_config.json")

global listOfGames
global listOfDuels
listOfGames = ["Overwatch", "Minecraft",  "Valorant", "ApexLegends", "Warfork", "Fortnite", "Sector's Edge"]
listOfDuels = []

def guild_id():
    return JI.get_value_from_key("GUILD_ID")

def generate_password(passwd_length):
    password = ""
    for i in range(passwd_length):
        password += chr(random.randint(33, 126))
    return password

def addDuels(
    duel_name: str = "",
    private_match: bool = False,
    password: str = "",
    challenger: str = "",
    opponents: str = ""
):
    global listOfDuels
    if password == None and private_match == True:
        password = generate_password(4)
    listOfDuels.append([duel_name, private_match, password, challenger, opponents])
    if private_match == True:
        return password

def listDuels():
    return listOfDuels

def remDuel(name):
    global listOfDuels
    success = False
    
    for i in listOfDuels:
        if i[0] == name:
            success = True
            listOfDuels.remove(i)
            break
        elif success == True:
            break
        
    return success

class Duels(interactions.Extension):
    
    ### /duels ###
    @interactions.slash_command("duels", description="Wie funktioniert es und welche Regeln gibt es?", scopes=[guild_id()])
    async def duels(
        self,
        ctx: interactions.SlashContext
    ):
        await ctx.send("Hier wird noch ein Embed eingefügt werden.")
        
    ### /duels erstellen [(str)duels_name] [(bool)private_match] [{optional}(str)password]###
    @duels.subcommand(
        "erstellen", sub_cmd_description="Erstelle ein Turnier"
    )
    @interactions.slash_option(
        "duels_name",
        "Gebe hier den Tournamentnamen ein.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        "private_match",
        "Soll das Spiel privat sein?",
        opt_type=interactions.OptionType.BOOLEAN,
        required=False,
    )
    @interactions.slash_option(
        "password",
        "Hier kannst du ein Passwort für das Turnier festlegen.",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def erstellen(
        self,
        ctx: interactions.SlashContext,
        duels_name: str = None,
        private_match: bool = None,
        password: str = None,
    ):
        passwd = addDuels(
            duels_name,
            private_match,
            password,
            ctx.author,
            opponents=""
        )
        private_match_message = ""
        if private_match == True:
            private_match_message = "privates "
        message = "Du hast ein " + private_match_message + "Duel '" + str(duels_name) + "' erstellt. \n"
        await ctx.send(message)
        if private_match == True and passwd != None:
            await ctx.bot.get_member(ctx.author.id, ctx.guild_id).send("Dein Passwort für das Turnier lautet: " + str(passwd))
            
    ### /duels beitretten [(str)duels_name] [{optional}(str)password]###
    @duels.subcommand(
        "beitretten", sub_cmd_description="Tritt einem Duel bei"
    )
    @interactions.slash_option(
        "duels_name",
        "Gebe hier den Tournamentnamen ein.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        "password",
        "Hier kannst du ein Passwort für das Turnier festlegen.",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def beitretten(
        self,
        ctx: interactions.SlashContext,
        duels_name: str = None,
        password: str = None,
    ):
        global listOfDuels
        success = False
        if len(listOfDuels) != 0:
            for i in listOfDuels:
                if i[0] == duels_name:
                    success = True
                    if i[1] == True and i[3] != ctx.author:
                        if i[2] == password:
                            listOfDuels[i][4] = str(ctx.author)
                            await ctx.send("Du bist dem Duel '" + str(duels_name) + "' beigetreten.")
                        else:
                            await ctx.send("Das Passwort für das Duel '" + str(duels_name) + "' ist falsch.")
                    elif i[3] != ctx.author:
                        listOfDuels[i][4] = str(ctx.author)
                        await ctx.send("Du bist dem Duel '" + str(duels_name) + "' beigetreten.")
                    elif i[3] == ctx.author:
                        await ctx.send("Du kannst nicht deinem eigenen Duel '" + str(duels_name) + "' beitreten.")
                        break
                    break
            if success == False:
                await ctx.send("Das Duel '" + str(duels_name) + "' existiert nicht.")
        else:
            await ctx.send("Es gibt noch keine Duels.")
            
    ### /duels verlassen [(str)duels_name] ###
    
    ### /duels liste ###
    @duels.subcommand(
        "liste", sub_cmd_description="eine Liste aller Duels"
    )
    async def liste(
        self,
        ctx: interactions.SlashContext,
    ):
        message = "Liste aller Duels: \n"
        for i in listOfDuels:
            duels = ""
            if i[1] == True:
                duels += "[PRIVATE] "
            duels += str(i[0]) + " | Angemeldete Spieler:  " + str(i[3]) + " vs. "
            if i[4] == "":
                duels += "(offen)"
            message += duels + "\n"
        await ctx.send(message)
        
    ### /duels invite [(str)duels_name] [(str)opponent] ###
    