from discord.ext import commands
import discord, subprocess, os, json
import chat_exporter

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')


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
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite me to your server!", url="https://discord.com/api/oauth2/authorize?client_id=782818919336902676&permissions=8&scope=bot",color=ctx.author.color))

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
        await ctx.send(embed=discord.Embed(title="Knowledge Bot's source code", url="https://github.com/SheepCommander/KnowledgeBase/tree/main/bots/Knowledge-Bot%20Anthony2be",color=ctx.author.color))








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
            for x in os.listdir(f'KnowledgeBase/{folder}'):
                things += x + "\n"
            embed=discord.Embed(color=ctx.author.color)
            embed.add_field(name=f"{folder}:", value=things, inline=False)
            await ctx.send(embed=embed)

        elif thing == 'you':
            ctx.send('no u')

        else:
            f = open(f'KnowledgeBase/{folder}/' + thing + '/raw-paste.txt', 'r',encoding = 'utf=8')
            raw = f.read()
            f.close()
            await ctx.send(raw)


    @commands.command(brief='Updates the repo', description = 'Updates the repo that the bot uses')
    async def update(self, ctx):
        subprocess.call([r'repo-updater.bat'])
        await ctx.send('Updated!')

    @commands.command()
    async def acronyms(self, ctx):
        f = open(f'KnowledgeBase/acronyms-list/raw-paste.txt', 'r',encoding = 'utf=8')
        raw = f.read()
        f.close()
        await ctx.send(raw)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

    



   
bot.add_cog(Knowledge())
bot.add_cog(Moderation())
bot.add_cog(Misc())



bot.run(TOKEN)
