import discord
from discord.ext import commands
class GenericModule(commands.Cog):
    
    WARNING = '\033[93m'
    END = '\033[0m'
    
    def __init__(self, client, name):
        self.__COGNAME = name
        self.client = client
    
    def module_message(self, message, level):
        print(f"{WARNING}{message}{END}")