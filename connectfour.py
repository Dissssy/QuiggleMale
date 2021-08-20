import json
import random
from copy import deepcopy
import sqlite3

from discord_components import ActionRow, SelectOption
from discord_components.component import Select
from asyncio import sleep

class connectfour:
    playerhelper = ["🔴", "🔷"]
    inverseplayerhelper = {playerhelper[0] : -1, None : 0, playerhelper[1] : 1, "tie" : 0}
    winnerhelper = ["💋", "💦"]
    headerhelper = [["⬛", "1️⃣"],["⬛", "2️⃣"],["⬛", "3️⃣"],["⬛", "4️⃣"],["⬛", "5️⃣"],["⬛", "6️⃣"],["⬛", "7️⃣"],["⬛", "8️⃣"],["⬛", "9️⃣"],["1️⃣", "0️⃣"],["1️⃣", "1️⃣"],["1️⃣", "2️⃣"],["1️⃣", "3️⃣"],["1️⃣", "4️⃣"],["1️⃣", "5️⃣"],["1️⃣", "6️⃣"],["1️⃣", "7️⃣"],["1️⃣", "8️⃣"],["1️⃣", "9️⃣"],["2️⃣", "0️⃣"],["2️⃣", "1️⃣"],["2️⃣", "2️⃣"],["2️⃣", "3️⃣"],["2️⃣", "4️⃣"],["2️⃣", "5️⃣"]]
    def __init__(self, ctx, players, gameid, singleplayer, ai, dimensions, training = False, sendmessage = True, smartopponent = False):
        self.training = training
        self.sendmessage = sendmessage
        self.smartopponent = smartopponent
        width = dimensions[0]
        height = dimensions[1]
        self.ctx = ctx
        self.ai = ai
        self.players = players
        self.gameid = gameid
        self.singleplayer = singleplayer
        self.tie = False
        self.current_player = random.randint(0, 1)
        self.gamestate = [[None for i in range(width)] for j in range(height)]
        self.winningpieces = [[False for i in range(len(self.gamestate[0]))] for j in range(len(self.gamestate))]
        self.columnavailable = [True for i in range(len(self.gamestate[0]))]
        self.winningcount = 0
        self.storedstates = {}
        self.normalmap = (width == 7 and height == 6)
        self.failed = False
        self.message = None
        self.winner = None
        self.movestoend = 0
        self.db = sqlite3.connect("./botdata.db")
    
    def _stringtolistoffloats(self, string):
        tmp =  string.strip("][").split(", ")
        lyst = []
        for i in tmp:
            lyst.append(float(i))
        return lyst

    def _getmap(self, map, invert = False):
        hash = self._hashmap(map, invert)
        cursor = self.db.cursor()
        cursor.execute(f'SELECT INDICES FROM C4DATA WHERE GRID = "{hash}"')
        map = cursor.fetchall()
        cursor.close()
        if len(map) > 0:
            return self._stringtolistoffloats(str(map[0][0]))
        else:
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def updateBot(self):
        value = self.inverseplayerhelper[self.winner]
        if (self.training or not (self.singleplayer)):
            if self.training:
                trainingweight = 0.01
            else:
                trainingweight = 100
            cursor = self.db.cursor()
            for gamemap in self.storedstates:
                cursor.execute(f'SELECT INDICES FROM C4DATA WHERE GRID = "{gamemap}"')
                results = cursor.fetchall()
                indices = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                if len(results) == 0:
                    cursor.execute(f'INSERT INTO C4DATA VALUES ("{gamemap}", "{indices}")')
                else:
                    indices = self._stringtolistoffloats(str(results[0][0]))
                thisvalue = self.storedstates[gamemap]
                invert = False
                if thisvalue < 0:
                    invert = True
                    thisvalue = thisvalue * -1
                thisvalue = thisvalue - 1
                if invert:
                    if value == 0:
                        value = 0.5
                    indices[thisvalue] += (((value) / ((self.movestoend - 3) / 2)) * trainingweight) * -1
                else:
                    if value == 0:
                        value = -0.5
                    indices[thisvalue] += ((value) / ((self.movestoend - 3) / 2)) * trainingweight
                cursor.execute(f'UPDATE C4DATA SET INDICES = "{indices}" WHERE GRID = "{gamemap}"')
            cursor.close()
            self.db.commit()

    def isvalidplayer(self, playerid):
        for player in self.players:
            if playerid == player.id:
                if playerid == self.players[self.current_player].id:
                    return [True, ""]
                else:
                    return [False, "It's not your turn"]
        return [False, "You arent a player in this game"]
    
    def constructheader(self):
        topheader = ''
        bottomheader = ''
        for i in range(len(self.gamestate[0])):
            if len(self.gamestate[0]) < 10:
                bottomheader += self.headerhelper[i][1]
            else:
                topheader += self.headerhelper[i][0]
                bottomheader += self.headerhelper[i][1]
        return f"{topheader}\n{bottomheader}"

    def _hashmap(self, map = None, invert = False):
        if map is None:
            map = self.gamestate
        hash = ""
        for i in range(6):
            for j in range(7):
                if invert:
                    hash += str((self.inverseplayerhelper[map[i][j]] * -1) + 1)
                else:
                    hash += str(self.inverseplayerhelper[map[i][j]] + 1)
        return str(hash)
    
    def _creategridmessage(self):
        gridmessage = self.constructheader()
        for i in range(len(self.gamestate)):
            gridmessage += "\n"
            for j in range(len(self.gamestate[i])):
                if self.gamestate[i][j] is None:
                    gridmessage += ":black_large_square:"
                else:
                    if self.winningpieces[i][j]:
                        gridmessage += self.gamestate[i][j].replace(self.playerhelper[0], self.winnerhelper[0]).replace(self.playerhelper[1], self.winnerhelper[1])
                    else:
                        gridmessage += self.gamestate[i][j]
        return gridmessage
    
    def _checkcolumn(self):
        for i in range(len(self.gamestate[0])):
            if self.columnavailable[i]:
                if (self.gamestate[0][i] is not None):
                    self.columnavailable[i] = False

    def _construct_options(self):
        options = []
        for i in range(len(self.gamestate[0])):
            if self.columnavailable[i]:
                options.append(SelectOption(label = f"{i + 1}", value = f"{self.gameid}:{i}"))
        if len(options) == 0:
            self.winner = "tie"
            self.tie = True
            options.append(SelectOption(label = f"Tie!", value = f"{self.gameid}:tie"))
        return options

    def _checkgamewon(self):
        self._checkcolumn()
        if not self.tie:
            winner = None
            for i in range(len(self.gamestate)):
                for j in range(len(self.gamestate[i])):
                    if i < (len(self.gamestate) - 3) and j < len(self.gamestate[i]):
                        if (self.gamestate[i][j] == self.gamestate[i + 1][j] == self.gamestate[i + 2][j] == self.gamestate[i + 3][j]) and self.gamestate[i][j] is not None:
                            for g in range(4):
                                self.winningpieces[i + g][j] = True
                                winner = self.gamestate[i][j]
                    if i < (len(self.gamestate)) and j < (len(self.gamestate[i]) - 3):
                        if (self.gamestate[i][j] == self.gamestate[i][j + 1] == self.gamestate[i][j + 2] == self.gamestate[i][j + 3]) and self.gamestate[i][j] is not None:
                            for g in range(4):
                                self.winningpieces[i][j + g] = True
                                winner = self.gamestate[i][j]
                    if i < (len(self.gamestate) - 3) and j < (len(self.gamestate[i]) - 3):
                        if (self.gamestate[i][j] == self.gamestate[i + 1][j + 1] == self.gamestate[i + 2][j + 2] == self.gamestate[i + 3][j + 3]) and self.gamestate[i][j] is not None:
                            for g in range(4):
                                self.winningpieces[i + g][j + g] = True
                                winner = self.gamestate[i][j]
                    if i < (len(self.gamestate) - 3) and j > 2:
                        if (self.gamestate[i][j] == self.gamestate[i + 1][j - 1] == self.gamestate[i + 2][j - 2] == self.gamestate[i + 3][j - 3]) and self.gamestate[i][j] is not None:
                            for g in range(4):
                                self.winningpieces[i + g][j - g] = True
                                winner = self.gamestate[i][j]
            self.winner = winner

    async def _construct_message(self):
        self._checkgamewon()
        if self.sendmessage:
            gridmessage = self._creategridmessage()
            if not self.training:
                components = [ActionRow(Select(options = self._construct_options(), id = f"{self.gameid}", placeholder = f"Make your move {self.players[self.current_player].name}"))]
            else:
                components = None
            try:
                if self.tie:
                    components = [ActionRow(Select(options = [SelectOption(label = f"Tie!", value = f"{self.gameid}:tie", default = True)], id = f"{self.gameid}", disabled = True))]
                if self.winner is not None:
                    components = [ActionRow(Select(options = [SelectOption(label = f"Game Over", value = f"{self.gameid}:winner", default = True)], id = f"{self.gameid}", disabled = True))]
                if self.message == None:
                    self.message = await self.ctx.send(f"{gridmessage}\nPlayer {self.playerhelper[self.current_player]} ({self.players[self.current_player].mention})'s turn!", components = components)
                else:
                    playing = ""
                    if self.winner is None:
                        playing = f"Player {self.playerhelper[self.current_player]} ({self.players[self.current_player].mention})'s turn!"
                    elif not self.winner == "tie":
                        self._countwinningspaces()
                        playing = f"{self.getoverkillstring()}: {self.players[(self.current_player + 1) % 2].mention}"
                    if not self.training:
                        await self.message.edit(f"{gridmessage}\n{playing}", components = components)
                    elif self.winner is not None:
                        await self.message.edit(f"{gridmessage}\n{playing}", components = components)
            except Exception as e:
                await self.ctx.send(f"{e}\n\n if length is too long, your board is too big", delete_after = 5)
                self.failed = True
                self.winner = "tie"
    
    def getoverkillstring(self):
        string = "WINNER"
        count = self.winningcount
        if count > 4:
            string = "OVERKILL"
        if count > 6:
            string = "SLAYER"
        if count > 9:
            string = "DESTROYER"
        if count > 15:
            string = "GODLIKE"
        return string

    async def set(self, index):
        oldmap = deepcopy(self.gamestate)
        if self._droppiece(index):
            self.movestoend += 1
            await self._swapPlayers()
            self._checkgamewon()
            await self._construct_message()
            if self.normalmap:
                if self.current_player == 0:
                    self.storedstates[self._hashmap(oldmap, False)] = index + 1
                else:
                    self.storedstates[self._hashmap(oldmap, True)] = (index + 1) * -1
            if self.winner == None:
                return [False, [True, ""]]
            else:
                self.updateBot()
                return [True, [True, ""]]
        else:
            return [False, [False, "INVALID INDEX"]]
    
    async def _swapPlayers(self):
        self.current_player = (self.current_player + 1) % 2
        if not (self.singleplayer or self.ai) and self.winner is None:
            await self.message.reply(f"{self.players[self.current_player].mention}", delete_after = 1)

    def _droppiece(self, index):
        if self.columnavailable[index]:
            for i in range(len(self.gamestate)):
                if (i + 1) < len(self.gamestate):
                    if self.gamestate[i + 1][index] is not None:
                        self.gamestate[i][index] = self.playerhelper[self.current_player]
                        return True
                else:
                    self.gamestate[i][index] = self.playerhelper[self.current_player]
                    return True
        else:
            return False
    
    def _countwinningspaces(self):
        count = 0
        for i in range(len(self.winningpieces)):
            for j in range(len(self.winningpieces[0])):
                if self.winningpieces[i][j]:
                    count += 1
        self.winningcount = count
    
    async def takeoverworld(self, training = False):
        #index will be the piece you drop this turn, if index sent to set is invalid, then response[1][0] will be false
        #self.gamestate is the current state of the board, during play it looks like
        
        # [[None, None, None, None, None, None, None], 
        # [None, None, None, None, None, None, None], 
        # [None, None, None, None, None, None, None], 
        # [None, None, ':red_circle:', None, ':blue_circle:', None, None], 
        # [None, ':blue_circle:', ':blue_circle:', ':blue_circle:', ':red_circle:', None, None], 
        # [None, ':red_circle:', ':red_circle:', ':red_circle:', ':blue_circle:', None, None]]
        
        # sorry about that, if it makes you feel any better, you can always tell whether its your piece or the opponents piece by doing 
        
        # self.players[self.inverseplayerhelper[":whatevers at the index:"]].id == self.message.author.id
        
        # this god awful line returns True if its the ais piece, dont send it None thatll fuck it up
        # good luck have fun :)
        
        skipped = 0
        possiblemoves = []
        highestvalue = None
        restart = True
        funnymode = True
        if not training:
            map = self._getmap(self.gamestate)
            while restart:
                skipped = 0
                restart = False
                if funnymode and not self.training:
                    skip = random.choice([False, True])
                else:
                    skip = random.choice([False, False])
                for i in range(7):
                    if self.columnavailable[i]:
                        if map[i] is not None:
                            if highestvalue is None:
                                highestvalue = map[i]
                                possiblemoves.append(i)
                            else:
                                if map[i] == highestvalue:
                                    possiblemoves.append(i)
                                elif map[i] > highestvalue:
                                    possiblemoves = []
                                    possiblemoves.append(i)
                        else:
                            skipped += 1
                if skip and skipped < 7:
                    restart = True
                    for move in possiblemoves:
                        map[move] = None
        else:
            if self.smartopponent:
                map = self._getmap(self.gamestate, True)
                while restart:
                    skipped = 0
                    restart = False
                    if funnymode or self.training:
                        skip = random.choice([False, True])
                    else:
                        skip = random.choice([False, False])
                    for i in range(7):
                        if self.columnavailable[i]:
                            if map[i] is not None:
                                if highestvalue is None:
                                    highestvalue = map[i]
                                    possiblemoves.append(i)
                                else:
                                    if map[i] == highestvalue:
                                        possiblemoves.append(i)
                                    elif map[i] > highestvalue:
                                        possiblemoves = []
                                        possiblemoves.append(i)
                            else:
                                skipped += 1
                    if skip and skipped < 7:
                        restart = True
                        for move in possiblemoves:
                            map[move] = None
            else:
                for i in range(7):
                    if self.columnavailable[i]:
                        possiblemoves.append(i)
        if skipped == 7:
            for i in range(7):
                if self.columnavailable[i]:
                    possiblemoves.append(i)

        if len(possiblemoves) > 0:
            index = random.choice(possiblemoves)
            response = await self.set(index)
            if not response[1][0]:
                print("ahh help me im dwowning")
        else:
            self.winner = "tie"
        if self.winner is not None:
            return True
        else:
            return False