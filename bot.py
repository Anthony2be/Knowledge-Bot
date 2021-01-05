from discord.ext import commands
import discord, json, chat_exporter, requests
from github import Github


g = Github(open('GitHub_token.txt','r').read())

TOKEN = open('Discord_token.txt', 'r').read()
key = open('Hypixel_key.txt','r').read()
repo = g.get_user('SheepCommander').get_repo( "KnowledgeBase" )

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'k!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 2)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 2)




@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('With Knowledge'))
    print(f'{bot.user.name} has connected to Discord!')
    chat_exporter.init_exporter(bot)






class Misc(commands.Cog):
    @commands.command(brief = 'exports the channel you say it in (might take some time)')
    async def save(self, ctx):
        await chat_exporter.export(ctx)
        
    @commands.command()
    async def foo(self, ctx, arg):
        await ctx.send(arg)



    @commands.command()
    @commands.has_permissions(administrator = True)
    async def prefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent = 2)
        await ctx.send('Changed the prefix to `' + prefix + '`')

        @commands.command(brief='Sees if the bot is working', description='''Sees if the bot is working and also says the bot's latency''')
        async def ping(self, ctx):
            await ctx.send('Pong! \nBot Latency is ' + str(bot.latency))
    @commands.command()
    async def source(self, ctx):
        await ctx.send(embed=discord.Embed(title="Knowledge Bot's source code", url="https://github.com/Anthony2be/Knowledge-Bot",color=ctx.author.color))








class Moderation(commands.Cog):
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def setdelay(ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, userName: discord.User, * , reason = None):
        embed=discord.Embed(title = f"Kicked {userName}", description = f"Reason: {reason}",color=ctx.author.color)
        await ctx.guild.kick(userName)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, userName: discord.User, * , reason = None):
            embed=discord.Embed(title = f"Banned {userName}", description = f"Reason: {reason}",color=ctx.author.color)
            await ctx.guild.ban(userName)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userName: discord.User, * , reason = None):
        embed=discord.Embed(title = f"Unbanned {userName}", description = f"Reason: {reason}",color=ctx.author.color)
        await ctx.guild.unban(userName)
        await ctx.send(embed=embed)







class Knowledge(commands.Cog):
    @commands.command()
    async def github(self, ctx, folder, * , thing):
        if thing == 'list':
            things = ""
            for file in repo.get_contents(f"1.16.4/{folder}/"):
                things += file.name + "\n"
            embed=discord.Embed(color=ctx.author.color)
            embed.add_field(name=f"{folder}:", value=things, inline=False)
            await ctx.send(embed=embed)

        elif thing == 'you':
            await ctx.send('no u')

        else:
            file_content = repo.get_contents(f'1.16.4/{folder}/' + thing + '/raw-discord-paste.txt')
            await ctx.send(file_content.decoded_content.decode())


    @commands.command()
    async def acronyms(self, ctx):
        file_content = repo.get_contents(f'1.16.4/acronyms-list/raw-discord-paste.txt')
        await ctx.send(file_content.decoded_content.decode())





@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

        
    



   
bot.add_cog(Knowledge())
bot.add_cog(Moderation())
bot.add_cog(Misc())



bot.run(TOKEN)