import random
from discord_components import Button, ButtonStyle, ActionRow


class tictactoe:
    buttonhelper = [ButtonStyle.red, ButtonStyle.blue]
    charhelper = {ButtonStyle.grey: "_", ButtonStyle.red: "X", ButtonStyle.blue: "O"}

    def __init__(self, ctx, players, gameid, singleplayer=False):
        self.ctx = ctx
        self.singleplayer = singleplayer
        self.current_player = random.randint(0, 1)
        self.players = players
        self.gameid = gameid
        self.tie = False
        self.winner = None
        self.gamestate = [
            [ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey],
            [ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey],
            [ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey],
        ]
        self.message = None

    def isvalidplayer(self, playerid):
        for player in self.players:
            if playerid == player.id:
                if playerid == self.players[self.current_player].id:
                    return [True, ""]
                else:
                    return [False, "It's not your turn"]
        return [False, "You arent a player in this game"]

    def makebutton(self, x, y):
        return Button(
            label=self.charhelper[self.gamestate[x][y]],
            style=self.gamestate[x][y],
            id=f"{self.gameid}:{x}{y}",
            disabled=not (self.winner == None)
            or not (self.gamestate[x][y] == ButtonStyle.grey),
        )

    async def _construct_message(self):
        self._checkgamewon()
        newcomponents = [
            ActionRow(
                self.makebutton(0, 0), self.makebutton(0, 1), self.makebutton(0, 2)
            ),
            ActionRow(
                self.makebutton(1, 0),
                self.makebutton(1, 1),
                self.makebutton(1, 2),
            ),
            ActionRow(
                self.makebutton(2, 0), self.makebutton(2, 1), self.makebutton(2, 2)
            ),
        ]
        if self.message == None:
            self.message = await self.ctx.send(
                f"Player {self.current_player + 1} ({self.players[self.current_player].mention})'s turn!",
                components=newcomponents,
            )
        else:
            if self.winner == None:
                await self.message.delete()
                self.message = await self.ctx.send(
                    f"Player {self.current_player + 1} ({self.players[self.current_player].mention})'s turn!",
                    components=newcomponents,
                )
            else:
                if not self.tie:
                    await self._swapPlayers()
                    await self.message.delete()
                    self.message = await self.ctx.send(
                        f"WINNER: Player {self.current_player + 1} ({self.players[self.current_player].mention})",
                        components=newcomponents,
                    )
                else:
                    await self.message.delete()
                    self.message = await self.ctx.send(
                        f"TIE!", components=newcomponents
                    )

    def rotategrid(self, grid):
        newgrid = [[None, None, None], [None, None, None], [None, None, None]]
        for i in range(3):
            for j in range(3):
                newgrid[2 - j][i] = grid[i][j]
        return newgrid

    def _checkgamewon(self):
        grid = self.gamestate
        gridr = self.rotategrid(grid)
        for i in range(0, 3):
            if (
                grid[i][0] == grid[i][1] == grid[i][2]
                and not grid[i][0] == ButtonStyle.grey
            ):
                self.winner = grid[i][0]
                return
            if (
                gridr[i][0] == gridr[i][1] == gridr[i][2]
                and not gridr[i][0] == ButtonStyle.grey
            ):
                self.winner = gridr[i][0]
                return
        if (
            grid[0][0] == grid[1][1] == grid[2][2]
            and not grid[0][0] == ButtonStyle.grey
        ):
            self.winner = grid[0][0]
            return
        if (
            gridr[0][0] == gridr[1][1] == gridr[2][2]
            and not gridr[0][0] == ButtonStyle.grey
        ):
            self.winner = gridr[0][0]
            return
        openspaces = 0
        for i in range(3):
            for j in range(3):
                if grid[i][j] == ButtonStyle.grey:
                    openspaces += 1
        if openspaces == 0:
            self.winner = "tie"
            self.tie = True

    async def set(self, index):
        if self.gamestate[int(index[0])][int(index[1])] == ButtonStyle.grey:
            self.gamestate[int(index[0])][int(index[1])] = self.buttonhelper[
                self.current_player
            ]
            await self._swapPlayers()
            self._checkgamewon()
            await self._construct_message()
            if self.winner == None:
                return [False, [True, ""]]
            else:
                return [True, [True, ""]]

        else:
            return [False, "that button is supposed to be disabled"]

    async def _swapPlayers(self):
        self.current_player = (self.current_player + 1) % 2
        if not self.singleplayer and self.winner is None:
            await self.message.reply(
                f"{self.players[self.current_player].mention}", delete_after=1
            )
