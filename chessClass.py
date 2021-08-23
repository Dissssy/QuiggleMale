
import random
from discord_components import ActionRow, Select, SelectOption, Button, ButtonStyle
from copy import deepcopy

class chess:
    boardEmotes = ["<:r:878210060705218601>", "<:bl:878210060843630602>"]
    intToLetter = ["A", "B", "C", "D", "E", "F", "G", "H"]
    intToType = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
    intToEmote = [None , "<:1:878210060814262293>", "<:2:878210061007204352>", "<:3:878210060977840128>", "<:4:878210061019791406>", "<:5:878210060558401547>", "<:6:878210060818464779>", "<:7:878210060826869760>", "<:8:878210060856229938>"]
    intToColor = ["White", "Black"]
    pieceEmoteStrings = [[["<:wPr:878232501603172423>", "<:wRr:878232501905154108>", "<:wNr:878232501728968785>", "<:wBr:878232501926121503>", "<:wQr:878232501976449085>", "<:wKr:878232501921927188>"], ["<:bPr:878232501582200833>", "<:bRr:878232501540257813>", "<:bNr:878232501909352478>", "<:bBr:878232501640917032>", "<:bQr:878232501531869246>", "<:bKr:878232504543359016>"]], [["<:wPb:878236200450801714>", "<:wRb:878236200417230858>", "<:wNb:878236200274628658>", "<:wBb:878236735060975626>", "<:wQb:878236200362709043>", "<:wKb:878236200480170044>"], ["<:bPb:878236200165580910>", "<:bRb:878236200136216576>", "<:bNb:878236200173989958>", "<:bBb:878236200304005121>", "<:bQb:878236200249458708>", "<:bKb:878236200228503552>"]]]
    promotions = [3, 2, 1, 4]
    rookDirections = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    bishopDirections = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    knightDirections = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2]]
    queenDirections = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    def __init__(self, ctx, players, gameid, singleplayer):
        self.ctx = ctx
        if random.choice([True, False]):
            self.players = [players[1], players[0]]
        else:
            self.players = [players[0], players[1]]
        self.currentplayer = 0
        self.gameid = gameid
        self.singleplayer = singleplayer
        self.message = None
        self.promote = None
        self.winner = None
        self.check = None
        self.checkpieces = None
        self.cantUncheck = False
        self.kings = [[0, 4], [7, 4]]
        self.gamestate = [[self.piece(1, 0), self.piece(2, 0), self.piece(3, 0), self.piece(4, 0), self.piece(5, 0), self.piece(3, 0), self.piece(2, 0), self.piece(1, 0)], [self.piece(0, 0) for i in range(8)], [None for i in range(8)], [None for i in range(8)], [None for i in range(8)], [None for i in range(8)], [self.piece(0, 1) for i in range(8)], [self.piece(1, 1), self.piece(2, 1), self.piece(3, 1), self.piece(4, 1), self.piece(5, 1), self.piece(3, 1), self.piece(2, 1), self.piece(1, 1)]]
        self.checkAllMoves(self.gamestate)
    
    def checkAllMoves(self, gamestate, checking = False):
        dolast = [None, None]
        for i in range(8):
            for j in range(8):
                if gamestate[i][j] is not None:
                    if not gamestate[i][j]['type'] == 5:
                        gamestate[i][j]['moves'], gamestate[i][j]['movecount'], gamestate[i][j]['captures'] = self.checkMoves([i, j], gamestate, checking)
                    else:
                        dolast[(gamestate[i][j]['color'] + self.currentplayer) % 2] = [i, j]
        for piece in dolast:
            gamestate[piece[0]][piece[1]]['moves'], gamestate[piece[0]][piece[1]]['movecount'], gamestate[piece[0]][piece[1]]['captures'] = self.checkMoves([piece[0], piece[1]], gamestate, checking)

    def checkMoves(self, piece, gamestate, checking = False):
        captures = {}
        moves = []
        if gamestate[piece[0]][piece[1]]['type'] == 0:
            direction = ((gamestate[piece[0]][piece[1]]['color'] * 2) - 1) * -1
            if piece[0] + direction >= 0 and piece[0] + direction <= 7:
                if gamestate[piece[0] + direction][piece[1]] is None:
                    moves.append([piece[0] + direction, piece[1]])
                    if gamestate[piece[0]][piece[1]]['firstmove'] and gamestate[piece[0] + direction + direction][piece[1]] is None:
                        moves.append([piece[0] + direction + direction, piece[1]])
                for i in range(2):
                    if (piece[1] + ((i * 2) - 1) >= 0 and piece[1] + ((i * 2) - 1) <= 7):
                        captures[str([piece[0] + direction, piece[1] + ((i * 2) - 1)])] = True
                        if gamestate[piece[0] + direction][piece[1] + ((i * 2) - 1)] is not None:
                            if not gamestate[piece[0] + direction][piece[1] + ((i * 2) - 1)]['color'] == gamestate[piece[0]][piece[1]]['color']:
                                moves.append([piece[0] + direction, piece[1] + ((i * 2) - 1)])
        elif gamestate[piece[0]][piece[1]]['type'] == 1:
            for direction in self.rookDirections:
                for i in range(8):
                    if piece[0] + (direction[0] * (i + 1)) >= 0 and piece[0] + (direction[0] * (i + 1)) <= 7 and piece[1] + (direction[1] * (i + 1)) >= 0 and piece[1] + (direction[1] * (i + 1)) <= 7:
                        captures[str([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])] = True
                        if gamestate[piece[0] + (direction[0] * (i + 1))][piece[1] + (direction[1] * (i + 1))] is not None:
                            if not gamestate[piece[0] + (direction[0] * (i + 1))][piece[1] + (direction[1] * (i + 1))]['color'] == gamestate[piece[0]][piece[1]]['color']:
                                moves.append([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])
                            break
                        else:
                            moves.append([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])
        elif gamestate[piece[0]][piece[1]]['type'] == 2:
            for direction in self.knightDirections:
                if piece[0] + direction[0] >= 0 and piece[0] + direction[0] <= 7 and piece[1] + direction[1] >= 0 and piece[1] + direction[1] <= 7:
                    captures[str([piece[0] + direction[0], piece[1] + direction[1]])] = True
                    if gamestate[piece[0] + direction[0]][piece[1] + direction[1]] is not None:
                        if not gamestate[piece[0] + direction[0]][piece[1] + direction[1]]['color'] == gamestate[piece[0]][piece[1]]['color']:
                            moves.append([piece[0] + direction[0], piece[1] + direction[1]])
                    else:
                        moves.append([piece[0] + direction[0], piece[1] + direction[1]])
        elif gamestate[piece[0]][piece[1]]['type'] == 3:
            for direction in self.bishopDirections:
                for i in range(8):
                    if piece[0] + (direction[0] * (i + 1)) >= 0 and piece[0] + (direction[0] * (i + 1)) <= 7 and piece[1] + (direction[1] * (i + 1)) >= 0 and piece[1] + (direction[1] * (i + 1)) <= 7:
                        captures[str([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])] = True
                        if gamestate[piece[0] + (direction[0] * (i + 1))][piece[1] + (direction[1] * (i + 1))] is not None:
                            if not gamestate[piece[0] + (direction[0] * (i + 1))][piece[1] + (direction[1] * (i + 1))]['color'] == gamestate[piece[0]][piece[1]]['color']:
                                moves.append([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])
                            break
                        else:
                            moves.append([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])
        elif gamestate[piece[0]][piece[1]]['type'] == 4:
            for direction in self.queenDirections:
                dirmoves = []
                for i in range(8):
                    if piece[0] + (direction[0] * (i + 1)) >= 0 and piece[0] + (direction[0] * (i + 1)) <= 7 and piece[1] + (direction[1] * (i + 1)) >= 0 and piece[1] + (direction[1] * (i + 1)) <= 7:
                        captures[str([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])] = True
                        if gamestate[piece[0] + (direction[0] * (i + 1))][piece[1] + (direction[1] * (i + 1))] is not None:
                            if not gamestate[piece[0] + (direction[0] * (i + 1))][piece[1] + (direction[1] * (i + 1))]['color'] == gamestate[piece[0]][piece[1]]['color']:
                                dirmoves.append([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])
                            break
                        else:
                            dirmoves.append([piece[0] + (direction[0] * (i + 1)), piece[1] + (direction[1] * (i + 1))])
                moves.append(dirmoves)
        elif gamestate[piece[0]][piece[1]]['type'] == 5:
            for direction in self.queenDirections:
                if piece[0] + direction[0] >= 0 and piece[0] + direction[0] <= 7 and piece[1] + direction[1] >= 0 and piece[1] + direction[1] <= 7:
                    possible = True
                    for i in range(8):
                        for j in range(8):
                            if gamestate[i][j] is not None:
                                if not gamestate[i][j]['color'] == gamestate[piece[0]][piece[1]]['color']:
                                    if str([piece[0] + direction[0], piece[1] + direction[1]]) in gamestate[i][j]['captures']:
                                        possible = False
                            if not possible:
                                break
                        if not possible:
                            break
                    if possible:
                        captures[str([piece[0] + direction[0], piece[1] + direction[1]])] = True
                        if gamestate[piece[0] + direction[0]][piece[1] + direction[1]] is not None:
                            if not gamestate[piece[0] + direction[0]][piece[1] + direction[1]]['color'] == gamestate[piece[0]][piece[1]]['color']:
                                moves.append([piece[0] + direction[0], piece[1] + direction[1]])
                        else:
                            moves.append([piece[0] + direction[0], piece[1] + direction[1]])

        if not checking and self.check is not None:
            if gamestate[piece[0]][piece[1]]['color'] == gamestate[self.check[0]][self.check[1]]['color']:
                if gamestate[piece[0]][piece[1]]['type'] == 4:
                    uncheck = False
                    for i in range(8):
                        for move in moves[i]:
                            if self.checkUncheck(piece, move):
                                moves = [[] for i in range(8)]
                                captures = {}
                                uncheck = True
                                break
                        if uncheck:
                            break
                else:
                    for move in moves:
                        if self.checkUncheck(piece, move):
                            moves = []
                            captures = {}
                            break
        
        if gamestate[piece[0]][piece[1]]['type'] == 4:
            moveCount = 0
            for i in range(8):
                moveCount += len(moves[i])
        else:
            moveCount = len(moves)
        if gamestate[piece[0]][piece[1]]['type'] == 0 and piece[0] == (gamestate[piece[0]][piece[1]]['color'] * -7) + 7:
            self.promote = piece
        return moves, moveCount, captures

    def checkCheck(self, gamestate):
        piecesCheck = 0
        check = None
        cantUncheck = False
        for i in range(8):
            for j in range(8):
                if gamestate[i][j] is not None:
                    if gamestate[i][j]['type'] == 5:
                        for k in range(8):
                            for l in range(8):
                                if gamestate[k][l] is not None:
                                    if not gamestate[i][j]['color'] == gamestate[k][l]['color']:
                                        if str([i, j]) in gamestate[k][l]['captures']:
                                            piecesCheck += 1
                                            check = [k, l]
                                        if piecesCheck > 1:
                                            cantUncheck = True
                                            return check, cantUncheck
        return check, cantUncheck

    def checkUncheck(self, piece, move):
        newgamestate = deepcopy(self.gamestate)
        newgamestate[move[0]][move[1]] = newgamestate[piece[0]][piece[1]]
        newgamestate[piece[0]][piece[1]] = None
        self.checkAllMoves(newgamestate, checking = True)
        check, _ = self.checkCheck(newgamestate)
        if check is not None:
            if self.gamestate[check[0]][check[1]]["color"] == self.gamestate[piece[0]][piece[1]]["color"]:
                return True
        return False

    def piece(self, type, color):
        piece = {}
        piece['type'] = type
        piece['color'] = color
        piece['name'] = self.intToType[type]
        piece['moves'] = []
        piece['captures'] = {}
        piece['movecount'] = 0
        piece['firstmove'] = True
        return piece

    def updatePiece(self, piece):
        self.gamestate[piece[0]][piece[1]]['name'] = self.intToType[type]

    def constructboardstring(self):
        string = "<:a:878071110481117205><:b:878071110544003114><:c:878071110862766120><:d:878071110455939104><:e:878071110749532171><:f:878071110510465106><:g:878071110996987935><:h:878071110892146728>\n"
        for i in range(8):
            for j in range(8):
                color = int(i % 2 == j % 2)
                if self.gamestate[i][j] is None:
                    string += self.boardEmotes[color]
                else:
                    string += self.pieceEmoteStrings[color][self.gamestate[i][j]['color']][self.gamestate[i][j]['type']]
            string += "\n"
        return string

    def canMoveTo(self, space):
        piecesCapture = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : []}
        for i in range(8):
            for j in range(8):
                if self.gamestate[i][j] is not None:
                    if self.gamestate[i][j]['color'] == self.currentplayer:
                        if self.gamestate[i][j]['type'] == 4:
                            for moves in self.gamestate[i][j]['moves']:
                                if space in moves:
                                    piecesCapture[self.gamestate[i][j]['type']].append([[i, j], space])
                        else:
                            if space in self.gamestate[i][j]['moves']:
                                piecesCapture[self.gamestate[i][j]['type']].append([[i, j], space])
        return piecesCapture

    def uncheckHelper(self, king):
        piece = self.gamestate[self.check[0]][self.check[1]]
        moves = [[], [], [], [], [], []]
        if piece['type'] == 0 or piece['type'] == 2:
            possiblePieces = self.canMoveTo([self.check[0], self.check[1]])
            for i in range(6):
                moves[i] += possiblePieces[i]
        else:
            direction = [0, 0]
            for i in range(2):
                if self.check[i] < king[i]:
                    direction[i] = 1
                elif self.check[i] == king[i]:
                    direction[i] = 0
                else:
                    direction[i] = -1
            position = self.check
            for i in range(8):
                possiblePieces = self.canMoveTo([position[0], position[1]])
                for i in range(6):
                    moves[i] += possiblePieces[i]
                for i in range(2):
                    position[i] += direction[i]
                if position == king:
                    break
        return moves

    def constructoptions(self, piece = None, promote = False, moveQueen = None, check = None, checkType = None):
        options = []
        end = False
        if not check:
            if piece is None:
                for i in range(8):
                    for j in range(8):
                        if self.gamestate[i][j] is not None:
                            if self.gamestate[i][j]['movecount'] > 0 and self.gamestate[i][j]['color'] == self.currentplayer:
                                options.append(SelectOption(label = f"{self.intToLetter[j]}{i + 1} : {self.gamestate[i][j]['name']}", value = f"{self.gameid}:select|{i}{j}"))
            else:
                if not promote:
                    if not self.gamestate[piece[0]][piece[1]]['type'] == 4:
                        for move in self.gamestate[piece[0]][piece[1]]['moves']:
                            poop = ""
                            if self.gamestate[move[0]][move[1]] is not None:
                                poop = f" and capture {self.intToType[self.gamestate[move[0]][move[1]]['type']]}"
                            options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToLetter[move[1]]}{move[0] + 1}{poop}", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|{move[0]}{move[1]}"))
                    else:
                        if moveQueen is None:
                            for i in range(8):
                                moves = self.gamestate[piece[0]][piece[1]]['moves'][i]
                                if len(moves) > 0:
                                    move = moves[-1]
                                    options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} towards {self.intToLetter[move[1]]}{move[0] + 1}", value = f"{self.gameid}:queen|{piece[0]}{piece[1]}|{i}"))
                        else:
                            for move in self.gamestate[piece[0]][piece[1]]['moves'][moveQueen]:
                                poop = ""
                                if self.gamestate[move[0]][move[1]] is not None:
                                    poop = f" and capture {self.intToType[self.gamestate[move[0]][move[1]]['type']]}"
                                options.append(SelectOption(label = f"{self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToLetter[move[1]]}{move[0] + 1}{poop}", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|{move[0]}{move[1]}"))
                    options.append(SelectOption(label = f"Back", value = f"{self.gameid}:move|{piece[0]}{piece[1]}|back"))
                else:
                    for promotion in self.promotions:
                        options.append(SelectOption(label = f"promote {self.intToLetter[piece[1]]}{piece[0] + 1} to {self.intToType[promotion]}", value = f"{self.gameid}:promote|{piece[0]}{piece[1]}|{promotion}"))
            if len(options) == 0:
                options.append(SelectOption(label = f"Game over", value = f"{self.gameid}:gameover"))
                end = True
        else:
            if not self.cantUncheck:
                if checkType is None:
                    self.checkpieces = self.uncheckHelper(piece)
                    for i in range(6):
                        if len(self.checkpieces[i]) > 0:
                            options.append(SelectOption(label = f"Escape check with a {self.intToType[i]}", value = f"{self.gameid}:checktype|{i}"))
                else:
                    for piecemove in self.checkpieces[checkType]:
                        apiece, move = piecemove
                        poop = ""
                        if self.gamestate[move[0]][move[1]] is not None:
                            poop = f" and capture {self.intToType[self.gamestate[move[0]][move[1]]['type']]}"
                        options.append(SelectOption(label = f"{self.intToLetter[apiece[1]]}{apiece[0] + 1} to {self.intToLetter[move[1]]}{move[0] + 1}{poop}", value = f"{self.gameid}:move|{apiece[0]}{apiece[1]}|{move[0]}{move[1]}"))
        if self.check and len(options) == 0:
            self.winner = self.players[(self.currentplayer + 1) % 2]
            options.append(SelectOption(label = f"Game over", value = f"{self.gameid}:gameover"))
            end = True
        return options, end

    async def constructmessage(self, piece = None, promote = False, moveQueen = None, check = None, checkType = None):
        options, end = self.constructoptions(piece, promote = promote, moveQueen = moveQueen, check = check, checkType = checkType)
        if not end:
            options.append(SelectOption(label = f"Forfeit", value = f"{self.gameid}:forfeit"))
            components = [ActionRow(Select(options = options, id = f"{self.gameid}", placeholder = f"Make your move {self.players[self.currentplayer].name}"))]
        else:
            components = [ActionRow(Select(options = options, id = f"{self.gameid}", placeholder = f"Game over", disabled = True))]
        fart = "Selecting"
        if piece is not None:
            if not promote:
                fart = f"Moving {self.intToLetter[piece[1]]}{piece[0] + 1} : {self.intToType[self.gamestate[piece[0]][piece[1]]['type']]}"
            else:
                fart = f"Promoting {self.intToLetter[piece[1]]}{piece[0] + 1}"
        piss = ""
        if check is not None:
            piss = ", you're in check!"
        if self.message == None:
            self.message = await self.ctx.send(f"{self.constructboardstring()}{self.intToColor[self.currentplayer]}s turn\n-- {fart}{piss}", components = components)
        else:
            if self.winner is None:
                await self.message.edit(f"{self.constructboardstring()}{self.intToColor[self.currentplayer]}s turn\n-- {fart}{piss}", components = components)
            else:
                await self.message.edit(f"{self.constructboardstring()}WINNER: {self.intToColor[(self.currentplayer + 1) % 2]} ({self.winner.mention})", components = components)

    async def set(self, value):
        values = value.split("|")
        if values[0] == "select":
            await self.constructmessage([int(values[1][0]), int(values[1][1])])
        elif values[0] == "move":
            if values[2] == "back":
                await self.constructmessage()
            else:
                self.check = None
                self.checkpieces = None
                self.gamestate[int(values[2][0])][int(values[2][1])] = self.gamestate[int(values[1][0])][int(values[1][1])]
                self.gamestate[int(values[1][0])][int(values[1][1])] = None
                self.gamestate[int(values[2][0])][int(values[2][1])]['firstmove'] = False
                if self.gamestate[int(values[2][0])][int(values[2][1])]['type'] == 5:
                    self.kings[self.gamestate[int(values[2][0])][int(values[2][1])]['color']] = [values[2][0]][values[2][1]]
                self.checkAllMoves(self.gamestate)
                self.check, self.cantUncheck = self.checkCheck(self.gamestate)
                if self.promote == None:
                    if self.check == None:
                        await self.swapPlayers()
                        await self.constructmessage()
                    else:
                        await self.swapPlayers()
                        await self.constructmessage(self.kings[self.currentplayer], check = True)
                else:
                    await self.constructmessage(self.promote, promote = True)
        elif values[0] == "promote":
            self.gamestate[int(values[1][0])][int(values[1][1])]['type'] = int(values[2][0])
            self.updatePiece([int(values[1][0])][int(values[1][1])])
            self.promote = None
            self.checkAllMoves(self.gamestate)
            await self.swapPlayers()
            await self.constructmessage()
        elif values[0] == "queen":
            await self.constructmessage([int(values[1][0]), int(values[1][1])], moveQueen = int(values[2]))
        elif values[0] == "checktype":
            await self.constructmessage(self.check, check = True, checkType = int(values[1]))
        if self.winner == None:
            return [False, [True, ""]]
        else:
            return [True, [True, ""]]
    
    def isvalidplayer(self, playerid, checkTurn = True):
        for player in self.players:
            if playerid == player.id:
                if checkTurn:
                    if playerid == self.players[self.currentplayer].id:
                        return [True, ""]
                    else:
                        return [False, "It's not your turn"]
                else:
                    return [True, ""]
        return [False, "You arent a player in this game"]
    
    async def swapPlayers(self):
        self.currentplayer = (self.currentplayer + 1) % 2
        if not self.singleplayer and self.winner is None:
            await self.message.reply(f"{self.players[self.currentplayer].mention}", deleteafter = 1)