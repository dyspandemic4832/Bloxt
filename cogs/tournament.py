import interactions
from addons.jsonimport import JsonImport

JI = JsonImport("dev_config.json")

global listOfGames
global listOfTournament
listOfGames = ["Overwatch", "Minecraft",  "Valorant", "ApexLegends", "Warfork", "Fortnite"]
listOfTournament = []

def guild_id():
    return JI.get_value_from_key("GUILD_ID")

def addTournament(Tournamentname, Opponents):
    ID = len(listOfTournament) + 1
    listOfTournament.append((ID ,Tournamentname, Opponents))
    return ID

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
        await ctx.send("Hello, world!")
        
    ### /tournament create [(str)tournament_name] [(str)gegner] ###
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
        "gegner",
        "Geben den Name des Gegners ein",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def erstellen(
        self,
        ctx: interactions.SlashContext,
        tournament_name: str = None,
        gegner: str = None,
    ):
        tournamentID = addTournament(tournament_name, Opponents=(ctx.author, gegner))
        await ctx.send("You have created the Tournament: " + str(tournament_name) + "\nID: " + str(tournamentID))
    
    ### /tournament list ###
    
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
        
    