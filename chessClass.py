import random
from discord_components import ActionRow, Select, SelectOption, Button, ButtonStyle

class chess:
    # boardEmotes = [":red_square:", ":black_large_square:"]
    boardEmotes = ["<:r_:878210060705218601>", "<:bl:878210060843630602>"]
    intToLetter = ["A", "B", "C", "D", "E", "F", "G", "H"]
    intToType = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
    # intToEmote = [None , ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
    intToEmote = [None , "<:1_:878210060814262293>", "<:2_:878210061007204352>", "<:3_:878210060977840128>", "<:4_:878210061019791406>", "<:5_:878210060558401547>", "<:6_:878210060818464779>", "<:7_:878210060826869760>", "<:8_:878210060856229938>"]
    intToColor = ["White", "Black"]
    promotions = [3, 2, 1, 4]
    def __init__(self, ctx, players, gameid, singleplayer):
        self.ctx = ctx
        shuffle = random.choice([True, False])
        if shuffle:
            self.players = [players[1], players[0]]
        else:
            self.players = [players[0], players[1]]
        self.current_player = 0
        self.gameid = gameid
        self.singleplayer = singleplayer
        self.message = None
        self.promote = None
        self.winner = None
        self.check = None
        self.gamestate = [[self.piece(self, 1, 0), self.piece(self, 2, 0), self.piece(self, 3, 0), self.piece(self, 4, 0), self.piece(self, 5, 0), self.piece(self, 3, 0), self.piece(self, 2, 0), self.piece(self, 1, 0)], [self.piece(self, 0, 0) for i in range(8)], [None for i in range(8)], [None for i in range(8)], [None for i in range(8)], [None for i in range(8)], [self.piece(self, 0, 1) for i in range(8)], [self.piece(self, 1, 1), self.piece(self, 2, 1), self.piece(self, 3, 1), self.piece(self, 4, 1), self.piece(self, 5, 1), self.piece(self, 3, 1), self.piece(self, 2, 1), self.piece(self, 1, 1)]]
        # self.gamestate = [[None for i in range(8)] for i in range(8)]
        dolast = [None, None]
        for i in range(8):
            for j in range(8):
                # if i == 4 and j == 4:
                #     self.gamestate[i][j] = self.piece(self, 4, 0)
                if self.gamestate[i][j] is not None:
                    if not self.gamestate[i][j].type == 5:
                        self.gamestate[i][j].setPosition(i, j)
                        self.gamestate[i][j].setPossibleMoves()
                    else:
                        dolast[(self.gamestate[i][j].color + self.current_player) % 2] = [i, j]
        for piece in dolast:
            self.gamestate[piece[0]][piece[1]].setPosition(piece[0], piece[1])
            self.gamestate[piece[0]][piece[1]].setPossibleMoves()
    
    class piece:
        emoteStrings = [["<:wPb:878236200450801714>", "<:wRb:878236200417230858>", "<:wNb:878236200274628658>", "<:wBb:878236735060975626>", "<:wQb:878236200362709043>", "<:wKb:878236200480170044>"], ["<:bPb:878236200165580910>", "<:bRb:878236200136216576>", "<:bNb:878236200173989958>", "<:bBb:878236200304005121>", "<:bQb:878236200249458708>", "<:bKb:878236200228503552>"]]
        rookDirections = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        bishopDirections = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        knightDirections = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2]]
        queenDirections = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        def __init__(self, parent, type, color):
            self.parent = parent
            self.type = type
            self.color = color
            self.string = self.emoteStrings[color][type]
            self.position = [0, 0]
            self.possibleMoves = []
            self.captures = {}
            self.firstmove = True
            self.moveCount = 0

        def promote(self):
            self.string = self.emoteStrings[self.color][self.type]

        def setPosition(self, x, y):
            self.position = [x, y]
        
        def setPossibleMoves(self):
            captures = {}
            moves = []
            if self.type == 0:
                direction = ((self.color * 2) - 1) * -1
                if self.position[0] + direction >= 0 and self.position[0] + direction <= 7:
                    if self.parent.gamestate[self.position[0] + direction][self.position[1]] is None:
                        moves.append([self.position[0] + direction, self.position[1]])
                        if self.firstmove and self.parent.gamestate[self.position[0] + direction + direction][self.position[1]] is None:
                            moves.append([self.position[0] + direction + direction, self.position[1]])
                    for i in range(2):
                        if (self.position[1] + ((i * 2) - 1) >= 0 and self.position[1] + ((i * 2) - 1) <= 7):
                            captures[str([self.position[0] + direction, self.position[1] + ((i * 2) - 1)])] = True
                            if self.parent.gamestate[self.position[0] + direction][self.position[1] + ((i * 2) - 1)] is not None:
                                if not self.parent.gamestate[self.position[0] + direction][self.position[1] + ((i * 2) - 1)].color == self.color:
                                    moves.append([self.position[0] + direction, self.position[1] + ((i * 2) - 1)])
            elif self.type == 1:
                for direction in self.rookDirections:
                    for i in range(8):
                        if self.position[0] + (direction[0] * (i + 1)) >= 0 and self.position[0] + (direction[0] * (i + 1)) <= 7 and self.position[1] + (direction[1] * (i + 1)) >= 0 and self.position[1] + (direction[1] * (i + 1)) <= 7:
                            captures[str([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])] = True
                            if self.parent.gamestate[self.position[0] + (direction[0] * (i + 1))][self.position[1] + (direction[1] * (i + 1))] is not None:
                                if not self.parent.gamestate[self.position[0] + (direction[0] * (i + 1))][self.position[1] + (direction[1] * (i + 1))].color == self.color:
                                    moves.append([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])
                                break
                            else:
                                moves.append([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])
            elif self.type == 2:
                for direction in self.knightDirections:
                    if self.position[0] + direction[0] >= 0 and self.position[0] + direction[0] <= 7 and self.position[1] + direction[1] >= 0 and self.position[1] + direction[1] <= 7:
                        captures[str([self.position[0] + direction[0], self.position[1] + direction[1]])] = True
                        if self.parent.gamestate[self.position[0] + direction[0]][self.position[1] + direction[1]] is not None:
                            if not self.parent.gamestate[self.position[0] + direction[0]][self.position[1] + direction[1]].color == self.color:
                                moves.append([self.position[0] + direction[0], self.position[1] + direction[1]])
                        else:
                            moves.append([self.position[0] + direction[0], self.position[1] + direction[1]])
            elif self.type == 3:
                for direction in self.bishopDirections:
                    for i in range(8):
                        if self.position[0] + (direction[0] * (i + 1)) >= 0 and self.position[0] + (direction[0] * (i + 1)) <= 7 and self.position[1] + (direction[1] * (i + 1)) >= 0 and self.position[1] + (direction[1] * (i + 1)) <= 7:
                            captures[str([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])] = True
                            if self.parent.gamestate[self.position[0] + (direction[0] * (i + 1))][self.position[1] + (direction[1] * (i + 1))] is not None:
                                if not self.parent.gamestate[self.position[0] + (direction[0] * (i + 1))][self.position[1] + (direction[1] * (i + 1))].color == self.color:
                                    moves.append([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])
                                break
                            else:
                                moves.append([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])
            elif self.type == 4:
                for direction in self.queenDirections:
                    dirmoves = []
                    for i in range(8):
                        if self.position[0] + (direction[0] * (i + 1)) >= 0 and self.position[0] + (direction[0] * (i + 1)) <= 7 and self.position[1] + (direction[1] * (i + 1)) >= 0 and self.position[1] + (direction[1] * (i + 1)) <= 7:
                            captures[str([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])] = True
                            if self.parent.gamestate[self.position[0] + (direction[0] * (i + 1))][self.position[1] + (direction[1] * (i + 1))] is not None:
                                if not self.parent.gamestate[self.position[0] + (direction[0] * (i + 1))][self.position[1] + (direction[1] * (i + 1))].color == self.color:
                                    dirmoves.append([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])
                                break
                            else:
                                dirmoves.append([self.position[0] + (direction[0] * (i + 1)), self.position[1] + (direction[1] * (i + 1))])
                    moves.append(dirmoves)
            elif self.type == 5:
                for direction in self.queenDirections:
                    if self.position[0] + direction[0] >= 0 and self.position[0] + direction[0] <= 7 and self.position[1] + direction[1] >= 0 and self.position[1] + direction[1] <= 7:
                        possible = True
                        for i in range(8):
                            for j in range(8):
                                if self.parent.gamestate[i][j] is not None:
                                    if not self.parent.gamestate[i][j].color == self.color:
                                        if self.parent.gamestate[i][j].canCapture(str([self.position[0] + direction[0], self.position[1] + direction[1]])):
                                            possible = False
                                if not possible:
                                    break
                            if not possible:
                                break
                        if possible:
                            captures[str([self.position[0] + direction[0], self.position[1] + direction[1]])] = True
                            if self.parent.gamestate[self.position[0] + direction[0]][self.position[1] + direction[1]] is not None:
                                if not self.parent.gamestate[self.position[0] + direction[0]][self.position[1] + direction[1]].color == self.color:
                                    moves.append([self.position[0] + direction[0], self.position[1] + direction[1]])
                            else:
                                moves.append([self.position[0] + direction[0], self.position[1] + direction[1]])
            self.captures = captures
            self.possibleMoves = moves
            if self.type == 4:
                moveCount = 0
                for i in range(8):
                    moveCount += len(self.possibleMoves[i])
            else:
                moveCount = len(moves)
            self.moveCount = moveCount
            if self.type == 0 and self.position[0] == (self.color * -7) + 7:
                return True
            return False
        
        def move(self):
            self.firstmove = False

        def canCapture(self, key):
            if key in self.captures:
                return True
            else:
                return False
    
    def _checkMoves(self):
        dolast = [None, None]
        for i in range(8):
            for j in range(8):
                if self.gamestate[i][j] is not None:
                    if not self.gamestate[i][j].type == 5:
                        result = self.gamestate[i][j].setPossibleMoves()
                        if result:
                            self.promote = [i, j]
                    else:
                        dolast[(self.gamestate[i][j].color + self.current_player) % 2] = [i, j]
        for piece in dolast:
            self.gamestate[piece[0]][piece[1]].setPossibleMoves()

    def _checkCheck(self):
        for i in range(8):
            for j in range(8):
                if self.gamestate[i][j] is not None:
                    if self.gamestate[i][j].type == 5:
                        for k in range(8):
                            for l in range(8):
                                if self.gamestate[k][l] is not None:
                                    if not self.gamestate[i][j].color == self.gamestate[k][l].color:
                                        if self.gamestate[k][l].canCapture(str([i, j])):
                                            self.check = [i, j]
                                        if self.check:
                                            return
    
    def _construct_options(self, piece = None, promote = False, moveQueen = None, check = None):
        options = []
        end = False
        if not check:
            if piece is None:
                for i in range(8):
                    for j in range(8):
                        if self.gamestate[i][j] is not None:
                            if self.gamestate[i][j].moveCount > 0 and self.gamestate[i][j].color == self.current_player:
                                options.append(SelectOption(label = f"{self.intToLetter[j]}{i + 1} : {self.intToType[self.gamestate[i][j].type]}", value = f"{self.gameid}:select|{i}{j}"))
            else:
                if not promote:
                    if not self.gamestate[piece[0]][piece[1]].type == 4:
                        for move in self.gamestate[piece[0]][piece[1]].possibleMoves:
                            poop = ""
                            if self.gamestate[move[0]][move[1]] is not None:
                                poop = f" and capture {self.intToType[self.gamestate[move[0]][move[1]].type]}"
                            options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToLetter[move[1]]}{move[0] + 1}{poop}", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|{move[0]}{move[1]}"))
                    else:
                        if moveQueen is None:
                            for i in range(8):
                                moves = self.gamestate[piece[0]][piece[1]].possibleMoves[i]
                                if len(moves) > 0:
                                    move = moves[-1]
                                    options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} towards {self.intToLetter[move[1]]}{move[0] + 1}", value = f"{self.gameid}:queen|{piece[0]}{piece[1]}|{i}"))
                        else:
                            for move in self.gamestate[piece[0]][piece[1]].possibleMoves[moveQueen]:
                                poop = ""
                                if self.gamestate[move[0]][move[1]] is not None:
                                    poop = f" and capture {self.intToType[self.gamestate[move[0]][move[1]].type]}"
                                options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToLetter[move[1]]}{move[0] + 1}{poop}", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|{move[0]}{move[1]}"))
                    options.append(SelectOption(label = f"Back", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|back"))
                else:
                    for promotion in self.promotions:
                        options.append(SelectOption(label = f"promote {self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToType[promotion]}", value = f"{self.gameid}:promote|{piece[0]}{piece[1]}|{promotion}"))
            if len(options) == 0:
                options.append(SelectOption(label = f"Game over", value = f"{self.gameid}:gameover"))
                end = True
        else:
            for move in self.gamestate[piece[0]][piece[1]].possibleMoves:
                poop = ""
                if self.gamestate[move[0]][move[1]] is not None:
                    poop = f" and capture {self.intToType[self.gamestate[move[0]][move[1]].type]}"
                options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToLetter[move[1]]}{move[0] + 1}{poop}", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|{move[0]}{move[1]}"))
        if self.check and len(options) == 0:
            self.winner = self.players[(self.current_player + 1) % 2]
            options.append(SelectOption(label = f"Game over", value = f"{self.gameid}:gameover"))
            end = True
        return options, end

    def _construct_boardstring(self):
        string = "<:a_:878071110481117205><:b_:878071110544003114><:c_:878071110862766120><:d_:878071110455939104><:e_:878071110749532171><:f_:878071110510465106><:g_:878071110996987935><:h_:878071110892146728>\n"
        for i in range(8):
            # string += f"{self.intToEmote[i + 1]}"
            for j in range(8):
                if self.gamestate[i][j] is None:
                    string += self.boardEmotes[int(i % 2 == j % 2)]
                else:
                    if i % 2 == j % 2:
                        string += self.gamestate[i][j].string
                    else:
                        string += self.gamestate[i][j].string.replace("<:wPb:878236200450801714>", "<:wPr:878232501603172423>").replace("<:wRb:878236200417230858>", "<:wRr:878232501905154108>").replace("<:wNb:878236200274628658>", "<:wNr:878232501728968785>").replace("<:wBb:878236735060975626>", "<:wBr:878232501926121503>").replace("<:wQb:878236200362709043>", "<:wQr:878232501976449085>").replace("<:wKb:878236200480170044>", "<:wKr:878232501921927188>").replace("<:bPb:878236200165580910>", "<:bPr:878232501582200833>").replace("<:bRb:878236200136216576>", "<:bRr:878232501540257813>").replace("<:bNb:878236200173989958>", "<:bNr:878232501909352478>").replace("<:bBb:878236200304005121>", "<:bBr:878232501640917032>").replace("<:bQb:878236200249458708>", "<:bQr:878232501531869246>").replace("<:bKb:878236200228503552>", "<:bKr:878232504543359016>")
            string += "\n"
        return string

    async def _construct_message(self, piece = None, promote = False, moveQueen = None, check = None):
        options, end = self._construct_options(piece, promote = promote, moveQueen = moveQueen, check = check)
        if not end:
            options.append(SelectOption(label = f"Forfeit", value = f"{self.gameid}:forfeit"))
            components = [ActionRow(Select(options = options, id = f"{self.gameid}", placeholder = f"Make your move {self.players[self.current_player].name}"))]
        else:
            components = [ActionRow(Select(options = options, id = f"{self.gameid}", placeholder = f"Game over", disabled = True))]
        fart = "Selecting"
        if piece is not None:
            if not promote:
                fart = f"Moving {self.intToLetter[piece[1]]}{piece[0] + 1} : {self.intToType[self.gamestate[piece[0]][piece[1]].type]}"
            else:
                fart = f"Promoting {self.intToLetter[piece[1]]}{piece[0] + 1}"
        piss = ""
        if check is not None:
            piss = ", you're in check!"
        if self.message == None:
            self.message = await self.ctx.send(f"{self._construct_boardstring()}{self.intToColor[self.current_player]}s turn\n-- {fart}{piss}", components = components)
        else:
            if self.winner is None:
                await self.message.edit(f"{self._construct_boardstring()}{self.intToColor[self.current_player]}s turn\n-- {fart}{piss}", components = components)
            else:
                await self.message.edit(f"{self._construct_boardstring()}WINNER: {self.intToColor[(self.current_player + 1) % 2]} ({self.winner.mention})", components = components)

    def isvalidplayer(self, playerid, checkTurn = True):
        for player in self.players:
            if playerid == player.id:
                if checkTurn:
                    if playerid == self.players[self.current_player].id:
                        return [True, ""]
                    else:
                        return [False, "It's not your turn"]
                else:
                    return [True, ""]
        return [False, "You arent a player in this game"]

    async def set(self, value):
        values = value.split("|")
        if values[0] == "select":
            await self._construct_message([int(values[1][0]), int(values[1][1])])
        elif values[0] == "move":
            if values[2] == "back":
                await self._construct_message()
            else:
                self.check = None
                self.gamestate[int(values[2][0])][int(values[2][1])] = self.gamestate[int(values[1][0])][int(values[1][1])]
                self.gamestate[int(values[1][0])][int(values[1][1])] = None
                self.gamestate[int(values[2][0])][int(values[2][1])].setPosition(int(values[2][0]), int(values[2][1]))
                self.gamestate[int(values[2][0])][int(values[2][1])].firstmove = False
                self._checkMoves()
                self._checkCheck()
                if self.promote == None:
                    if self.check == None:
                        await self._swapPlayers()
                        await self._construct_message()
                    else:
                        await self._swapPlayers()
                        await self._construct_message(self.check, check = True)
                else:
                    await self._construct_message(self.promote, promote = True)
        elif values[0] == "promote":
            self.gamestate[int(values[1][0])][int(values[1][1])].type = int(values[2][0])
            self.gamestate[int(values[1][0])][int(values[1][1])].promote()
            self.promote = None
            self._checkMoves()
            await self._swapPlayers()
            await self._construct_message()
        elif values[0] == "queen":
            await self._construct_message([int(values[1][0]), int(values[1][1])], moveQueen = int(values[2]))
        if self.winner == None:
            return [False, [True, ""]]
        else:
            return [True, [True, ""]]
    
    async def _swapPlayers(self):
        self.current_player = (self.current_player + 1) % 2
        if not self.singleplayer and self.winner is None:
            await self.message.reply(f"{self.players[self.current_player].mention}", delete_after = 1)