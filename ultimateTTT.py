import random
from discord_components import Button, ButtonStyle, ActionRow

class ultimateTTT:
    def __init__(self, ctx, players, gameid, maingame = False, current_player = None, index = None, parent = None, singleplayer = False):
        self.ctx = ctx
        if current_player == None:
            self.current_player = random.randint(0, 1)
        else:
            self.current_player = current_player
        if not index == None:
            self.index = index
        self.players = players
        self.gameid = gameid
        self.parent = parent
        self.tie = False
        self.singleplayer = singleplayer
        self.winner = None
        self.selection = None
        self.maingame = maingame
        if self.maingame:
            self.gamestate = [[ultimateTTT(self.ctx, self.players, self.gameid, current_player = self.current_player, index = [x, y], parent = self) for y in range(3)] for x in range(3)]
        else:
            self.gamestate = [[ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey], [ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey], [ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey]]
        self.message = None
        self.boardmessage = None
        self.buttonhelper = [ButtonStyle.red, ButtonStyle.blue]
        self.charhelper = {ButtonStyle.grey : "_", ButtonStyle.red : "X", ButtonStyle.blue : "O", None : "_", "tie" : "*"}
        self.chartobutton = {"*" : ButtonStyle.grey, "tie" : ButtonStyle.grey, "_" : ButtonStyle.grey, "X" : ButtonStyle.red, "O" : ButtonStyle.blue}
        if maingame:
            self._constructglobalboard()
    
    def isvalidplayer(self, playerid):
        for player in self.players:
            if playerid == player.id:
                if playerid == self.players[self.current_player].id:
                    return [True, ""]
                else:
                    return [False, "It's not your turn"]
        return [False, "You arent a player in this game"]

    def setmessage(self, message):
        self.message = message
    
    def setplayer(self, player):
        self.current_player = player

    def makebutton(self, x, y):
        if self.maingame:
            state = self.charhelper[self.gamestate[x][y].winner]
            state = self.chartobutton[state]
            return Button(
                            label = self.charhelper[state],
                            style = state,
                            id = f'{self.gameid}:{x}{y}',
                            disabled = self.gamestate[x][y].tie or not (self.winner == None) or not (state == ButtonStyle.grey)
                        )
        else:
            state = self.gamestate[x][y]
            xx, yy = self.index
            surround = ''
            if x == xx and y == yy:
                surround = '|'
            return Button(
                            label = f"{surround}{self.charhelper[state]}{surround}",
                            style = state,
                            id = f'{self.gameid}:{x}{y}',
                            disabled = not (self.winner == None) or not (state == ButtonStyle.grey)
                        )
    
    def _constructglobalboard(self):
        globalboard = [['' for i in range(9)] for j in range(9)]
        boardstring = ""
        for h in range(3):
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        winner = self.gamestate[h][i].winner
                        if winner == None or self.winner is not None:
                            globalboard[j + (h * 3)][k + (i * 3)] = self.gamestate[h][i].gamestate[j][k]
                        elif winner == "tie":
                            globalboard[j + (h * 3)][k + (i * 3)] = "tie"
                        else:
                            globalboard[j + (h * 3)][k + (i * 3)] = winner
        rowcount = 0
        splitcount = 0
        for row in globalboard:
            rowcount += 1
            pointcount = 0
            splitpointcount = 0
            for point in row:
                pointcount += 1
                boardstring += self.charhelper[point] + " "
                if pointcount == 3 and splitpointcount < 2:
                    splitpointcount += 1
                    boardstring += "| "
                    pointcount = 0
            boardstring += "\n"
            if rowcount == 3 and splitcount < 2:
                splitcount += 1
                boardstring += "------|-------|------\n"
                rowcount = 0
        success = []
        self.globalboardstring = boardstring
        for row in self.gamestate:
            for game in row:
                game.globalboardstring = self.globalboardstring
                success.append(game.index)
        return success

    async def _construct_message(self):
        self._checkgamewon()
        newcomponents = [
            ActionRow(
                self.makebutton(0, 0),
                self.makebutton(0, 1),
                self.makebutton(0, 2)
            ),
            ActionRow(
                self.makebutton(1, 0),
                self.makebutton(1, 1),
                self.makebutton(1, 2),
                Button(label = "Wiki", style = 5, url = "https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe")
            ),
            ActionRow(
                self.makebutton(2, 0),
                self.makebutton(2, 1),
                self.makebutton(2, 2)
            )
        ]
        if self.maingame:
            self._constructglobalboard()
        else:
            self.parent._constructglobalboard()
        if self.message == None:
            self.message = await self.ctx.send(
                f"```{self.globalboardstring}```Player {self.current_player + 1} ({self.players[self.current_player].mention})'s turn! select a local board!", 
                components = newcomponents
            )
            for row in self.gamestate:
                for game in row:
                    game.setmessage(self.message)
        else:
            if self.winner == None:
                setting = ''
                if self.maingame:
                    setting = ' select a local board!'
                await self.message.edit(
                    f"```{self.globalboardstring}```Player {self.current_player + 1} ({self.players[self.current_player].mention})'s turn!{setting}",
                    components = newcomponents
                )
            else:
                if self.maingame:
                    if not self.tie:
                        await self._swapPlayers()
                        await self.message.edit(
                            f"```{self.globalboardstring}```WINNER: Player {self.current_player + 1} ({self.players[self.current_player].mention})",
                            components = newcomponents
                        )
                    else:
                        await self.message.edit(
                            f"```{self.globalboardstring}```TIE!",
                            components = newcomponents
                        )

    def rotategrid(self, grid):
        newgrid = [[None for i in range(3)] for j in range(3)]
        for i in range(3):
            for j in range(3):
                newgrid[2 - j][i] = grid[i][j]
        return newgrid

    def _checkgamewon(self):
        grid = [[None for i in range(3)] for j in range(3)]
        if self.maingame:
            for i in range(3):
                for j in range(3):
                    grid[i][j] = self.gamestate[i][j].winner
                    if grid[i][j] == None:
                        grid[i][j] = ButtonStyle.grey
            gridr = self.rotategrid(grid)
            for i in range(3):
                if grid[i][0] == grid[i][1] == grid[i][2] and not grid[i][0] == ButtonStyle.grey:
                    self.winner = grid[i][0]
                    return
                if gridr[i][0] == gridr[i][1] == gridr[i][2] and not gridr[i][0] == ButtonStyle.grey:
                    self.winner = gridr[i][0]
                    return
            if grid[0][0] == grid[1][1] == grid[2][2] and not grid[0][0] == ButtonStyle.grey:
                self.winner = grid[0][0]
                return
            if gridr[0][0] == gridr[1][1] == gridr[2][2] and not gridr[0][0] == ButtonStyle.grey:
                self.winner = gridr[0][0]
                return
            openspaces = 0
            for i in range(3):
                for j in range(3):
                    if grid[i][j] == ButtonStyle.grey: openspaces += 1
            if openspaces == 0:
                self.winner = "tie"
                self.tie = True
        else:
            grid = self.gamestate
            gridr = self.rotategrid(grid)
            for i in range(3):
                if grid[i][0] == grid[i][1] == grid[i][2] and not grid[i][0] == ButtonStyle.grey:
                    self.winner = grid[i][0]
                    return
                if gridr[i][0] == gridr[i][1] == gridr[i][2] and not gridr[i][0] == ButtonStyle.grey:
                    self.winner = gridr[i][0]
                    return
            if grid[0][0] == grid[1][1] == grid[2][2] and not grid[0][0] == ButtonStyle.grey:
                self.winner = grid[0][0]
                return
            if gridr[0][0] == gridr[1][1] == gridr[2][2] and not gridr[0][0] == ButtonStyle.grey:
                self.winner = gridr[0][0]
                return
            openspaces = 0
            for i in range(3):
                for j in range(3):
                    if grid[i][j] == ButtonStyle.grey: openspaces += 1
            if openspaces == 0:
                self.winner = "tie"
                self.tie = True

    async def set(self, index):
        if self.maingame:
            self._checkgamewon()
            if self.winner == None:
                if self.selection == None:
                    self.selection = [int(index[0]), int(index[1])]
                    await self.gamestate[self.selection[0]][self.selection[1]]._construct_message()
                    if self.winner == None:
                        return [False, [True, ""]]
                    else:
                        return [True, [True, ""]]
                else:
                    await self.gamestate[self.selection[0]][self.selection[1]].set(index)
                    await self._swapPlayers()
                    self.selection = [int(index[0]), int(index[1])]
                    if self.gamestate[self.selection[0]][self.selection[1]].winner == None:
                        self._checkgamewon()
                        if self.winner is not None:
                            self._checkgamewon()
                            await self._construct_message()
                        else:
                            await self.gamestate[self.selection[0]][self.selection[1]]._construct_message()
                    else:
                        self.selection = None
                        await self._construct_message()
                    self._checkgamewon()
                    if self.winner == None:
                        return [False, [True, ""]]
                    else:
                        return [True, [True, ""]]
            else:
                await self._construct_message()
        else:
            if self.gamestate[int(index[0])][int(index[1])] == ButtonStyle.grey:
                self.gamestate[int(index[0])][int(index[1])] = self.buttonhelper[self.current_player]
                await self._construct_message()
                if self.winner == None:
                    return [False, [True, ""]]
                else:
                    return [True, [True, ""]]
            else:
                return [False, [False, "that button is supposed to be disabled"]]

    async def _swapPlayers(self):
        self.current_player = (self.current_player + 1) % 2
        if not self.singleplayer and self.winner is None:
            await self.message.reply(f"{self.players[self.current_player].mention}", delete_after = 1)
        for row in self.gamestate:
            for game in row:
                game.setplayer(self.current_player)