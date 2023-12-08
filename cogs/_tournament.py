import interactions
from addons.jsonimport import JsonImport
import random

JI = JsonImport("dev_config.json")

global listOfGames
global listOfTournament
listOfGames = ["Overwatch", "Minecraft",  "Valorant", "ApexLegends", "Warfork", "Fortnite"]
listOfTournament = []

def guild_id():
    return JI.get_value_from_key("GUILD_ID")

def generate_password(passwd_length):
    password = ""
    for i in range(passwd_length):
        password += chr(random.randint(33, 126))
    return password

def addTournament(
    tournament_name: str = None,
    max_player: int = None,
    private_match: bool = None,
    password: str = None,
    opponents: list = None
):
    global listOfTournament
    if password == None and private_match == True:
        password = generate_password(4)
    listOfTournament.append([tournament_name, max_player, private_match, password, opponents])
    if private_match == True:
        return password

def listTournament():
    return listOfTournament

def remTournament(ID):
    global listOfTournament
    success = False
    
    for i in listOfTournament:
        if i[0] == ID:
            success = True
            listOfTournament.remove(i)
            break
        elif success == True:
            break
        
    return success

class Tournament(interactions.Extension):
    
    ### /tournament ###
    @interactions.slash_command("tournament", description="Wie funktioniert es und welche Regeln gibt es?", scopes=[guild_id()])
    async def tournament(
        self,
        ctx: interactions.SlashContext
    ):
        await ctx.send("Hier wird noch ein Embed eingefügt werden.")
        
    ### /tournament create [(str)tournament_name] [(int)max_player] [(bool)private_match] [{optional}(str)password]###
    @tournament.subcommand(
        "erstellen", sub_cmd_description="Erstelle ein Turnier"
    )
    @interactions.slash_option(
        "tournament_name",
        "Gebe hier den Tournamentnamen ein.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        "max_player",
        "Gebe hier die maximale Anzahl an Spielern ein.",
        opt_type=interactions.OptionType.INTEGER,
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
        tournament_name: str = None,
        max_player: int = None,
        private_match: bool = None,
        password: str = None,
    ):
        passwd = addTournament(
            tournament_name,
            max_player,
            private_match,
            password,
            [ctx.author.id]
        )
        private_match_message = ""
        if private_match == True:
            private_match_message = "private "
        message = "Du hast das " + private_match_message + "Tournament: " + str(tournament_name) + " erstellt. \n"
        await ctx.send(message)
        if private_match == True and passwd != None:
            await ctx.bot.get_member(ctx.author.id, ctx.guild_id).send("Dein Passwort für das Turnier lautet: " + str(passwd))
    
    ### /tournament list ###
    @tournament.subcommand(
        "liste", sub_cmd_description="eine Liste aller Turniere"
    )
    async def liste(
        self,
        ctx: interactions.SlashContext,
    ):
        message = "Liste aller Turniere: \n"
        for i in listOfTournament:
            tournament = ""
            if i[2] == True:
                tournament += "[PRIVATE] "
            tournament += str(i[0]) + " | max Spieler: " + str(i[1]) + " | Angemeldete Spieler:  " + str(len(i[4]))
            message += tournament + "\n"
        await ctx.send(message)
    
    
    ### /tournament delete [(int)tournament_id] ###
    
    ### /tournament join [(int)tournament_id] ###
    
    ### /tournament leave [(int)tournament_id] ###
    
    ### /tournament start [(int)tournament_id] ###
    
    ### /tournament end [(int)tournament_id] ###
    
    ### /tournament info [(int)tournament_id] ###
    
    ### /pick [(int)tournamen_id] ###
    @interactions.slash_command("pick", description="A command with components", scopes=[guild_id()])
    @interactions.slash_option(
        "tournament_id",
        "Geben die Tournament ID ein",
        opt_type=interactions.OptionType.INTEGER,
        required=True,
    )
    async def components(
        self,
        ctx: interactions.SlashContext,
        tournament_id: int = None,
    ):
        
        ### füge eine verifizierung ein, ob der user in dem turnier ist ###
        ### füge die ausgewählten spieler in eine liste ein ###
        await ctx.send(
            "Here are some components",
            components=interactions.spread_to_rows(
                interactions.StringSelectMenu(
                    listOfGames,
                    placeholder="Bitte wähle mindestens zwei Spiel aus.",
                    min_values=2,
                    max_values=5,
                    custom_id="selected_games",
                ),
            ),
        )

    @interactions.component_callback("selected_games")
    async def select_me(self, ctx: interactions.ComponentContext):
        """A callback for the select me menu"""
        await ctx.send(f"You selected {' '.join(ctx.values)}")
        
    