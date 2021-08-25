import asyncio, discord, json, psutil, os, tictactoe, ultimateTTT, connectfour, rockpaperscissors, chessClass
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, ActionRow
import time
from os.path import getsize
from sys import argv

testmode = False
if "-testmode" in argv:
    testmode = True
training = False
updaterrunning = False

loop = asyncio.get_event_loop()
currentConfirming = {}
currentTTTgames = {}
currentUltimateTTTgames = {}
currentC4games = {}
currentRPSgames = {}
currentChessGames = {}

config = json.load(open("./config.json"))
owner = int(config["owner"])
if testmode:
    token = config["testtoken"]
else:
    token = config["token"]
gps = config["gps"]
prefix = config["prefix"]

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    global loop
    global testmode
    DiscordComponents(client)
    print(f"logged in as {client.user} \n ------")
    loop.create_task(gameoverchecker(client, "button_click"))
    loop.create_task(gameoverchecker(client, "select_option"))
    loop.create_task(presenceupdater())
    if testmode:
        loop.create_task(resourcelogger())

@client.event
async def on_command_error(ctx, error):
    errortimeout = 2.5
    if isinstance(error, commands.BadArgument):
        await ctx.reply(str(error.args[0]), delete_after = errortimeout)
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.reply(str(error.args[0]), delete_after = errortimeout)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply(str(error.args[0]), delete_after = errortimeout)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(str(error.args[0]), delete_after = errortimeout)
    else:
        print(error)

@client.command(name = "tictactoe", help = "Select a space to mark with your character and attempt to get 3 in a row before your opponent does", usage = "@user", aliases = ["ttt"], description = "A simple game of Tic Tac Toe")
async def ttt(ctx, user: discord.User):
    if not user == None:
        if not (ctx.author.bot or user.bot):
            global loop
            loop.create_task(confirmchallenge(ctx, user, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}", "ttt", ctx.author.id == user.id))
        else:
            await ctx.reply("you cant challenge a bot", delete_after = 5)
    else:
        await ctx.reply("ping someone to play against", delete_after = 5)

@client.command(name = "ultimatetictactoe", help = "https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe", usage = "@user", aliases = ["ultimatettt", "utictactoe", "uttt"], description = "A complex game of Tic Tac Toe, i highly recommend reading the wikipedia page before playing")
async def uttt(ctx, user: discord.User):
    if not user == None:
        if not (ctx.author.bot or user.bot):
            global loop
            loop.create_task(confirmchallenge(ctx, user, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}", "uttt", ctx.author.id == user.id))
        else:
            await ctx.reply("you cant challenge a bot", delete_after = 5)
    else:
        await ctx.reply("ping someone to play against", delete_after = 5)

@client.command(name = "connectfour", help = "Drop pieces from the top, they fall down to the bottom, attempt to get four in a row before your opponent does", usage = "@user *width *height\n* = optional", aliases = ["c4"], description = "A simple game of connect four")
async def c4(ctx, user: discord.User, width: int = 7, height: int = 6):
    if not user == None:
        if not (ctx.author.bot or (user.bot and not user.id == client.user.id)):
            if (width > 3) and (height > 3) and (width < 10) and (height < 10):
                if user.id == client.user.id:
                    width = 7
                    height = 6
                global loop
                loop.create_task(confirmchallenge(ctx, user, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}", "c4", ctx.author.id == user.id, specialdata = {"ai" : user.id == client.user.id, "dimensions" : [width, height]}))
            else:
                await ctx.reply(f"miniumum is 4, max is 9", delete_after = 15)
        else:
            await ctx.reply("you cant challenge a bot... besides me", delete_after = 5)
    else:
        await ctx.reply("ping someone to play against", delete_after = 5)

@client.command(name = "chess", help = "https://en.wikipedia.org/wiki/Chess\nNOTE: THIS VERSION OF CHESS DOES NOT HAVE CASTLING", usage = "@user", description = "Its chess")
async def chess(ctx, user: discord.User):
    if not user == None:
        if not (ctx.author.bot or user.bot):
            global loop
            loop.create_task(confirmchallenge(ctx, user, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}", "chess", ctx.author.id == user.id))
        else:
            await ctx.reply("you cant challenge a bot", delete_after = 5)
    else:
        await ctx.reply("ping someone to play against", delete_after = 5)

@client.command(name = "rockpaperscissors", help = "Scissors beats Paper beats Rock beats Scissors, try to guess which one will make you win against your opponent", usage = "@user *rounds\n* = optional", aliases = ["rps"], description = "A simple game of Rock Paper Scissors")
async def rps(ctx, user: discord.User, rounds: int = 1):
    if not user == None:
        if not (ctx.author.bot or user.bot):
            global loop
            loop.create_task(confirmchallenge(ctx, user, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}", "rps", ctx.author.id == user.id, rounds = rounds))
        else:
            await ctx.reply("you cant challenge a bot", delete_after = 5)
    else:
        await ctx.reply("ping someone to play against", delete_after = 5)
        

@client.command(hidden = True)
async def r(ctx, *, args: str = ""):
    if ctx.author.id == owner:
        args = args.split(" ")
        try:
            await ctx.message.delete()
        except:
            pass
        global training
        if (activity(True) and not "y" in args) or (training and not "t" in args):
            string = ""
            delete_after = None
            if activity(True) and not "y" in args:
                string += f"Theres still activity{activity()}are you sure you want to restart?"
                components = [ActionRow(Button(label = "Yes", style = ButtonStyle.green, id = "restart:yes"), Button(label = "No", style = ButtonStyle.red, id = "restart:no"))]
            if training and not "t" in args:
                string = string.replace("are you sure you want to restart?", "") + "im training right now, either abort training or wait until later"
                components = []
                delete_after = 5
            await ctx.send(string, components = components, delete_after = delete_after)
            if len(components) > 0 and not training:
                while True:
                    interaction = await client.wait_for("button_click", check = lambda i: i.component.id.startswith("restart"))
                    if interaction.user.id == owner:
                        if interaction.component.id.endswith("yes"):
                            restart = True
                        else:
                            restart = False
                        await interaction.respond(type = 6)
                        await interaction.message.delete()
                        if restart:
                            await client.close()
                    else:
                        await interaction.respond(content = "you are not the owner")
        else:
            await client.close()

@client.command(hidden = True)
async def resources(ctx):
    if ctx.author.id == owner:
        try:
            await ctx.message.delete()
        except:
            pass
        process = psutil.Process(os.getpid())
        await ctx.send(f"cpu : {process.cpu_percent()}\nram : {process.memory_info().rss}", delete_after = 10)

@client.command(hidden = True)
async def list(ctx):
    if ctx.author.id == owner:
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(activity(), delete_after = 10)

@client.command(hidden = True)
async def trainc4(ctx, amount = 1, smartopponent: bool = False):
    if ctx.author.id == owner:
        global training
        if not training:
            global loop
            training = True
            loop.create_task(dotrainingc4(ctx, amount, smartopponent))
        else:
            await ctx.reply("im already training bud")

@client.command(hidden = True)
async def abortc4(ctx):
    if ctx.author.id == owner:
        global training
        training = False

async def dotrainingc4(ctx, amount, smartopponent):
    global training
    global gps
    if amount > 0:
        try:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = f"Connect Four {amount} times"))
        except Exception as e:
            print(str(e))
        await ctx.message.reply(f"{amount} games should take approximately {secondstotime(amount / gps)}")
        startingtime = time.time()
        lean = 0
        locallean = 0
        totalmoves = 0
        localmoves = 0
        ties = 0
        for i in range(0, amount):
            winner, moves = await connectFourTraining(ctx, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}:training:{i}", [client.user, client.user], True, True, [7, 6], i == (amount - 1), smartopponent)
            lean += winner
            locallean += winner
            totalmoves += moves
            localmoves += moves
            completed = i + 1
            if winner == 0:
                ties += 1
            if (i + 1) % 50 == 0:
                await asyncio.sleep(0.1)
                print(i + 1, end = ":\t")
                print(f"{(locallean / completed) * 100:.2f}%\t{(lean / completed) * 100:.2f}%", end = "\t|\t")
                print(f"{localmoves / 50:.2f}\t{totalmoves / completed:.2f}", end = "\t|\t")
                print(f"{ties}", end = "\t|\t")
                print(sizeof_fmt(getsize("./botdata.db")))
                locallean = 0
                localmoves = 0
            if not training:
                break
    else:
        try:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = f"Connect Four indefinitely"))
        except Exception as e:
            print(str(e))
        startingtime = time.time()
        lean = 0
        locallean = 0
        totalmoves = 0
        localmoves = 0
        i = 0
        ties = 0
        while True:
            winner, moves = await connectFourTraining(ctx, f"{ctx.guild.id}{ctx.channel.id}{ctx.message.id}:training:{i}", [client.user, client.user], True, True, [7, 6], i == (amount - 1), smartopponent)
            lean += winner
            locallean += winner
            totalmoves += moves
            localmoves += moves
            completed = i + 1
            if winner == 0:
                ties += 1
            if (i + 1) % 50 == 0:
                await asyncio.sleep(0.1)
                print(i + 1, end = ":\t")
                print(f"{(locallean / completed) * 100:.2f}%\t{(lean / completed) * 100:.2f}%", end = "\t|\t")
                print(f"{localmoves / 50:.2f}\t{totalmoves / completed:.2f}", end = "\t|\t")
                print(f"{ties}", end = "\t|\t")
                print(sizeof_fmt(getsize("./botdata.db")))
                locallean = 0
                localmoves = 0
            i += 1
            if not training:
                break
    
    elapsed = time.time() - startingtime
    await ctx.message.reply(f"Finished {completed} games in {secondstotime(elapsed)} ({completed / elapsed:.2f} games per second)\nwon {(lean / completed) * 100:.2f}% of the time {ties} were ties\navg moves = {totalmoves / completed:.2f}")
    gps = completed / elapsed
    config["gps"] = gps
    with open("./config.json", "w") as f:
        json.dump(config, f)
    training = False

async def confirmchallenge(ctx, user, gameid, gametype, singleplayer, rounds = 0, ai = False, specialdata = {"ai" : False}):
    global currentConfirming
    if not gametype == "forfeit":
        players = [ctx.author, user]
    if singleplayer or specialdata["ai"]:
        if gametype == "ttt":
            loop.create_task(tictactoeGame(ctx, gameid, players, singleplayer))
        elif gametype == "uttt":
            loop.create_task(ultimatetictactoeGame(ctx, gameid, players, singleplayer))
        elif gametype == "c4":
            loop.create_task(connectFourGame(ctx, gameid, players, singleplayer, specialdata["ai"], specialdata["dimensions"]))
        elif gametype == "chess":
            loop.create_task(chessGame(ctx, gameid, players, singleplayer))
        else:
            await ctx.reply("you cant play that game solo, sorry", delete_after = 5)
        try:
            await ctx.message.delete()
        except Exception as e:
            print(str(e))
    else:
        if not gametype == "forfeit":
            try:
                await ctx.message.delete()
            except Exception as e:
                print(str(e))   
        roundstring = "a game"
        if rounds > 1:
            roundstring = f"{rounds} rounds"
        if gametype == "forfeit":
            await ctx.channel.send(f"{user.mention}, are you sure you want to forfeit?", components = [ActionRow(Button(id = f"{gameid}:accept", label = "Yes", style = ButtonStyle.green), Button(id = f"{gameid}:decline", label = "No", style = ButtonStyle.red))])
        else:
            await ctx.send(f"{user.mention}, you have been challenged to {roundstring} of {makereadable(gametype)} by {ctx.author.mention}", components = [ActionRow(Button(id = f"{gameid}:accept", label = "accept", style = ButtonStyle.green), Button(id = f"{gameid}:decline", label = "decline", style = ButtonStyle.red))])
        currentConfirming[gameid] = True
        while True:
            interaction = await client.wait_for("button_click", check = lambda i: i.component.id.startswith(gameid))
            if interaction.user.id == user.id:
                response = interaction.component.id.split(":")[-1]
                await interaction.respond(type = 6)
                if response == "accept":
                    if gametype == "forfeit":
                        global currentChessGames
                        await currentChessGames[gameid].forfeit(user)
                        currentChessGames.pop(gameid)
                    elif gametype == "ttt":
                        loop.create_task(tictactoeGame(ctx, gameid, players, singleplayer))
                    elif gametype == "uttt":
                        loop.create_task(ultimatetictactoeGame(ctx, gameid, players, singleplayer))
                    elif gametype == "c4":
                        loop.create_task(connectFourGame(ctx, gameid, players, singleplayer, False, specialdata["dimensions"]))
                    elif gametype == "rps":
                        loop.create_task(rockpaperscissorsGame(ctx, gameid, players, rounds))
                    elif gametype == "chess":
                        loop.create_task(chessGame(ctx, gameid, players, singleplayer))
                await interaction.message.delete()
                currentConfirming.pop(gameid)
                return
            else:
                await interaction.respond(content = f"You arent {user}")

async def tictactoeGame(ctx, gameid, players, singleplayer):
    global currentTTTgames
    currentTTTgames[gameid] = tictactoe.tictactoe(ctx, players, gameid, singleplayer = singleplayer)
    await currentTTTgames[gameid]._construct_message()
    while True:
        interaction = await client.wait_for("button_click", check = lambda i: i.component.id.startswith(gameid))
        player = currentTTTgames[gameid].isvalidplayer(interaction.user.id)
        if player[0]:
            response = await currentTTTgames[gameid].set(interaction.component.id.split(":")[-1])
            if response[0]:
                try:
                    await interaction.respond(type = 6)
                except Exception as e:
                    print(str(e))
                currentTTTgames.pop(gameid)
                return
            elif response[1][0]:
                try:
                    await interaction.respond(type = 6)
                except Exception as e:
                    print(str(e))
            else:
                try:
                    await interaction.respond(content = response[1])
                except Exception as e:
                    print(str(e))
        else:
            try:
                await interaction.respond(content = player[1])
            except Exception as e:
                print(str(e))

async def ultimatetictactoeGame(ctx, gameid, players, singleplayer):
    global currentUltimateTTTgames
    currentUltimateTTTgames[gameid] = ultimateTTT.ultimateTTT(ctx, players, gameid, True, singleplayer = singleplayer)
    await currentUltimateTTTgames[gameid]._construct_message()
    while True:
        interaction = await client.wait_for("button_click", check = lambda i: i.component.id.startswith(gameid))
        player = currentUltimateTTTgames[gameid].isvalidplayer(interaction.user.id)
        if player[0]:
            try:
                await interaction.respond(type = 6)
            except Exception as e:
                print(str(e))
            response = await currentUltimateTTTgames[gameid].set(interaction.component.id.split(":")[-1])
            if response[0]:
                currentUltimateTTTgames.pop(gameid)
                return
        else:
            try:
                await interaction.respond(content = player[1])
            except Exception as e:
                print(str(e))

async def connectFourGame(ctx, gameid, players, singleplayer, ai, dimensions):
    global currentC4games
    currentC4games[gameid] = connectfour.connectfour(ctx, players, gameid, singleplayer, ai, dimensions)
    win = False
    if ai and (currentC4games[gameid].current_player == 1):
        await currentC4games[gameid].takeoverworld()
    await currentC4games[gameid]._construct_message()
    if currentC4games[gameid].failed:
        currentC4games.pop(gameid)
        return
    while True:
        interaction = await client.wait_for("select_option", check = lambda i: i.component[0].value.startswith(gameid))
        player = currentC4games[gameid].isvalidplayer(interaction.user.id)
        if player[0]:
            try:
                await interaction.respond(type = 6)
            except Exception as e:
                print(str(e))
            response = await currentC4games[gameid].set(int(interaction.component[0].value.split(":")[-1]))
            if currentC4games[gameid].failed:
                currentC4games.pop(gameid)
                return
            if response[0]:
                currentC4games.pop(gameid)
                return
            if ai:
                win = await currentC4games[gameid].takeoverworld()
            if win:
                currentC4games.pop(gameid)
                return
        else:
            try:
                await interaction.respond(content = player[1])
            except Exception as e:
                print(str(e))

async def rockpaperscissorsGame(ctx, gameid, players, rounds):
    global currentRPSgames
    currentRPSgames[gameid] = rockpaperscissors.rockpaperscissors(ctx, players, gameid, rounds)
    await currentRPSgames[gameid]._construct_message()
    while True:
        interaction = await client.wait_for("button_click", check = lambda i: i.component.id.startswith(gameid))
        player = currentRPSgames[gameid].isvalidplayer(interaction.user.id)
        if player[0]:
            response = await currentRPSgames[gameid].set(interaction.component.id.split(":")[-1], interaction.user)
            if response[0]:
                try:
                    await interaction.respond(type = 6)
                except Exception as e:
                    print(str(e))
                currentRPSgames.pop(gameid)
                return
            else:
                if response[1] is not None:
                    try:
                        await interaction.respond(content = response[1])
                    except Exception as e:
                        print(str(e))
                else:
                    try:
                        await interaction.respond(type = 6)
                    except Exception as e:
                        print(str(e))
        else:
            try:
                await interaction.respond(content = player[1])
            except Exception as e:
                print(str(e))

async def chessGame(ctx, gameid, players, singleplayer):
    global currentChessGames
    currentChessGames[gameid] = chessClass.chess(ctx, players, gameid, singleplayer)
    await currentChessGames[gameid].constructmessage()
    while True:
        interaction = await client.wait_for("select_option", check = lambda i: i.component[0].value.startswith(gameid))
        if interaction.component[0].value.endswith("forfeit"):
            player = currentChessGames[gameid].isvalidplayer(interaction.user.id, checkTurn = False)
            if player[0]:
                global loop
                loop.create_task(confirmchallenge(interaction, interaction.user, gameid, "forfeit", False))
                try:
                    await interaction.respond(type = 6)
                except Exception as e:
                    print(str(e))
            else:
                try:
                    await interaction.respond(content = player[1])
                except Exception as e:
                    print(str(e))
        else:
            player = currentChessGames[gameid].isvalidplayer(interaction.user.id)
            if player[0]:
                response = await currentChessGames[gameid].set(interaction.component[0].value.split(":")[-1])
                if response[0]:
                    try:
                        await interaction.respond(type = 6)
                    except Exception as e:
                        print(str(e))
                    currentChessGames.pop(gameid)
                    return
                else:
                    if not response[1]:
                        try:
                            await interaction.respond(content = response[1][1])
                        except Exception as e:
                            print(str(e))
                    else:
                        try:
                            await interaction.respond(type = 6)
                        except Exception as e:
                            print(str(e))
            else:
                try:
                    await interaction.respond(content = player[1])
                except Exception as e:
                    print(str(e))
    # except Exception as e:
    #     await ctx.send(str(e))
    #     currentChessGames.pop(gameid)

async def gameoverchecker(client, type):
    while True:
        if type == "button_click":
            interaction = await client.wait_for(type, check = lambda i: (not i.component.id.split(":")[0] in currentTTTgames) and 
                                                                        (not i.component.id.split(":")[0] in currentUltimateTTTgames) and
                                                                        (not i.component.id.split(":")[0] in currentRPSgames) and 
                                                                        (not i.component.id.split(":")[0] in currentConfirming) and 
                                                                        (not i.component.id.startswith("restart")))
        elif type == "select_option":
            interaction = await client.wait_for(type, check = lambda i: (not i.component[0].value.split(":")[0] in currentC4games) and
                                                                        (not i.component[0].value.split(":")[0] in currentChessGames))
        
        await interaction.respond(content = "this was lost to the sands of time (probably a restart, my bad, sorry)")
        await interaction.message.delete()

async def connectFourTraining(ctx, gameid, players, singleplayer, ai, dimensions, sendmessage, smartopponent):
    global currentC4games
    currentC4games[gameid] = connectfour.connectfour(ctx, players, gameid, singleplayer, ai, dimensions, True, sendmessage, smartopponent)
    win = False
    await currentC4games[gameid]._construct_message()
    while True:
        player = not bool(currentC4games[gameid].current_player)
        win = await currentC4games[gameid].takeoverworld(player)
        if win:
            winner = currentC4games[gameid].inverseplayerhelper[currentC4games[gameid].winner]
            moves = currentC4games[gameid].movestoend
            currentC4games.pop(gameid)
            return winner, moves

async def presenceupdater():
    global updaterrunning
    if not updaterrunning:
        starttime = time.time()
        updaterrunning = True
        sleep = 5
        while updaterrunning:
            elapsed = time.time() - starttime
            global training
            if not training:
                try:
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = f"for {secondstotime(elapsed)}"))
                except Exception as e:
                    print(str(e))
            await asyncio.sleep(sleep)

async def resourcelogger():
    process = psutil.Process(os.getpid())
    # while True:
    #     print(process.memory_info().rss)
    #     await asyncio.sleep(10)

def makereadable(gamecode):
    if gamecode == "ttt":
        return "Tic Tac Toe"
    if gamecode == "uttt":
        return "Ultimate Tic Tac Toe"
    if gamecode == "c4":
        return "Connect Four"
    if gamecode == "rps":
        return "Rock Paper Scissors"
    if gamecode == "chess":
        return "Chess"

def secondstotime(seconds):
    unit = "second"
    if seconds >= 60:
        unit = "minute"
        seconds = seconds / 60
        sleep = 60
        if seconds >= 60:
            unit = "hour"
            seconds = seconds / 60
            if seconds >= 24:
                unit = "day"
                seconds = seconds / 24
                if seconds >= 30:
                    unit = "month"
                    seconds = seconds / 30
                    if seconds >= 365:
                        unit = "year"
                        seconds = seconds / 365
    s = "s"
    if seconds > 0.99 and seconds <1.99:
        s = ""
    return f"{seconds:.0f} {unit}{s}"

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def activity(check = False):
    if check:
        if len(currentConfirming) > 0:
            return True 
        if len(currentTTTgames) > 0:
            return True
        if len(currentUltimateTTTgames) > 0:
            return True
        if len(currentC4games) > 0:
            return True 
        if len(currentRPSgames) > 0:
            return True
        if len(currentChessGames) > 0:
            return True
        else:
            return False
    else:
        return f"```Active confirmations:\n{currentConfirming}\nTic Tac Toe:\n{currentTTTgames}\nUltimate Tic Tac Toe:\n{currentUltimateTTTgames}\nConnect Four:\n{currentC4games}\nRock Paper Scissors:\n{currentRPSgames}\nChess:\n{currentChessGames}```"

client.run(token)