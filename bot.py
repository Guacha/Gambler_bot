import DB_Control
from StockMarket.market import StockMarket
import discord
from discord.ext import commands
from discord_slash import SlashCommand

class GamBlot(commands.Bot):
    def __init__(self, prefix):
        self.db = DB_Control.initialise_database()
        super().__init__(command_prefix=prefix, intents=discord.Intents.all())
        self.slash = SlashCommand(self, sync_commands=True)


# Gremios en los que se va a probar el bot
test_guilds = [375866694465355776]

# Inicialización del bot
client = GamBlot("/")

# Eventos
@client.event
async def on_ready():
    print("Bot listo")    

# Comandos
@client.slash.slash(name="ping",
                    guild_ids=test_guilds,
                    description="Comando para medir la latencia con el bot en cualquier momento dado")
async def ping(ctx):
    await ctx.respond()
    await ctx.send(f"Pong! (Latencia: {client.latency*1000} ms)")

client.run("")


    