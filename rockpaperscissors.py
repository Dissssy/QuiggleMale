from discord_components.component import ActionRow, Button, ButtonStyle
from math import floor


class rockpaperscissors:
    def __init__(self, ctx, players, gameid, rounds):
        self.ctx = ctx
        self.players = players
        self.wins = [0, 0]
        self.gameid = gameid
        self.rounds = rounds
        self.message = None
        self.totalwinner = None
        self.currentround = 1
        self.selections = [None, None]
        self.selectionkey = {"rock" : 1, "paper" : 2, "scissors" : 3}
        
    def _convert_player_to_index(self, player):
        if self.players[0].id == player.id:
            return 0
        else: 
            return 1

    def isvalidplayer(self, playerid):
        for player in self.players:
            if playerid == player.id:
                return [True, ""]
        return [False, "You arent a player in this game"]

    async def _construct_message(self):
        gotwinner = self.totalwinner is not None
        components = [ActionRow(
            Button(label = "👊", id = f"{self.gameid}:rock", style = ButtonStyle.red, disabled = gotwinner),
            Button(label = "✋", id = f"{self.gameid}:paper", style = ButtonStyle.green, disabled = gotwinner),
            Button(label = "✌", id = f"{self.gameid}:scissors", style = ButtonStyle.blue, disabled = gotwinner)
        )]
        ping = ["", ""]
        if self.selections[0] is None:
            ping[0] = f"{self.players[0].mention}"
        else:
            ping[0] = f"{self.players[0].name}"
        
        if self.selections[1] is None:
            ping[1] = f"{self.players[1].mention}"
        else:
            ping[1] = f"{self.players[1].name}"
        
        if self.message == None:
            self.message = await self.ctx.send(f"{ping[0]} : {self.wins[0]}\n{ping[1]} : {self.wins[1]}\nround {self.currentround}/{self.rounds}", components = components)
        else:
            if self.totalwinner is None:
                if self.selections[0] is None and self.selections[1] is None:
                    await self.message.delete()
                    self.message = await self.ctx.send(f"{ping[0]} : {self.wins[0]}\n{ping[1]} : {self.wins[1]}\nround {self.currentround}/{self.rounds}", components = components)
                else:
                    await self.message.edit(f"{ping[0]} : {self.wins[0]}\n{ping[1]} : {self.wins[1]}\nround {self.currentround}/{self.rounds}", components = components)
            else:
                if self.totalwinner == "tie":
                    self.totalwinner = None
                    self.rounds += 1
                else:
                    await self.message.delete()
                    self.message = await self.ctx.send(f"winner: {self.totalwinner.mention}\n{self.wins[self._convert_player_to_index(self.totalwinner)]} to {self.wins[(self._convert_player_to_index(self.totalwinner) + 1) % 2]}", components = components)
    
    async def set(self, selection, player):
        if self.selections[self._convert_player_to_index(player)] is None:
            self.selections[self._convert_player_to_index(player)] = selection
            if None in self.selections:
                await self._construct_message()
                return [False, None]
            else:
                self._checkroundwon()
                self._checkgamewon()
                await self._construct_message()
                if self.totalwinner == None:
                    return [False, None]
                else:
                    return [True, None]
        else:
            return [False, f"You've already made a selection this round, you picked {self.selections[self._convert_player_to_index(player)]}"]
    
    def _checkroundwon(self):
        one, two = self.selections
        one = self.selectionkey[one]
        two = self.selectionkey[two]
        if one == two:
            pass
        elif(one > two or (one == 1 and two == 3)) and not (one == 3 and two == 1):
            self.wins[0] += 1
        else:
            self.wins[1] += 1
        self.selections = [None, None]
        self.currentround += 1
    
    def _checkgamewon(self):
        if self.wins[0] > floor(self.rounds/2) or self.wins[1] > floor(self.rounds/2):
            if self.wins[0] > self.wins[1]:
                self.totalwinner = self.players[0]
            else:
                self.totalwinner = self.players[1]