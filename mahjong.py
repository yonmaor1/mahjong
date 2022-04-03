from player import *
import random

def makeDeck():
    # returns a complete deck (still missing flowers / seasons)
    deck = []
    # populate the deck: siuted values are 1-9, 4 tiles of each
    for i in range(1,10):
        deck += [(i, 'dot') for j in range(4)]
    for i in range(1,10):
        deck += [(i, 'stick') for j in range(4)]
    for i in range(1,10):
        deck += [(i, 'number') for j in range(4)]

    # directions
    deck += [('dung',) for j in range(4)]
    deck += [('nan',) for j in range(4)]
    deck += [('xi',) for j in range(4)]
    deck += [('bei',) for j in range(4)]

    # dragons
    deck += [('zhong',) for j in range(4)]
    deck += [('fa',) for j in range(4)]
    deck += [('box',) for j in range(4)]

    return deck

def initPlayers():
    # creates 4 player objects, returns them in a list
    player1Name = input('Enter Player 1s Name:')
    player1isAI = input('Make Player 1 an AI?')

    player2Name = input('Enter Player 1s Name:')
    player2isAI = input('Make Player 1 an AI?')

    player3Name = input('Enter Player 1s Name:')
    player3isAI = input('Make Player 1 an AI?')

    player4Name = input('Enter Player 1s Name:')
    player4isAI = input('Make Player 1 an AI?')

    player0 = Player(player1Name, 0, player1isAI)
    player1 = Player(player2Name, 1, player2isAI)
    player2 = Player(player3Name, 2, player3isAI)
    player3 = Player(player4Name, 3, player4isAI)

    players = [player0, player1, player2, player3]

    return players

def gameOver(players, tossedTile):
    # checks if game has ended (ie if any player can end the game)
    if (players[0].canHu(tossedTile) or
        players[1].canHu(tossedTile) or
        players[2].canHu(tossedTile) or
        players[3].canHu(tossedTile)):
        return True
    return False

def playRound(players):
    deck = makeDeck()
    deadTiles = []
    turn = 0
    giveHands(players, deck)
    players[0].isDealer = True
    # first turn (must draw new tile)
    players[0].drawTile(deck)
    tossedTile = players[0].tossTile()

    # rest of the turns (a tossed tile exists)
    while not gameOver(players, tossedTile):
        turn = (turn + 1) % 4

        # to make sure player doesn't Stanley (pong thne draw a tile)
        action = None

        # check if anyone can Pong / Kong
        # if so, skip to their turn 
        for player in [ players[turn], players[(turn+1)%4], players[(turn+2)%4] ]:
            if player.canPong(tossedTile):
                # Kong if and only if Pong
                if player.canKong(tossedTile):
                    # input must be bool
                    wantsToKong = input(f'{player.name} can Kong. Would you like to?')
                else:
                    # input must be bool
                    wantsToPong = input(f'{player.name} can Pong. Would you like to?')
                
                if wantsToKong: 
                    action = 'kong'
                    turn = player.num
                    break
                elif wantsToPong: 
                    action = 'pong'
                    turn = player.num
                    break
                else: 
                    action = None
        
        # if nobody Pongs/Kongs, check for Chi
        if (action is None) and (players[(turn+1)%4].canChi(tossedTile)):
            # input must be bool
            wantsToChi = input(f'{player.name} can Chi. Would you like to?')
            if wantsToChi:
                action = 'chi'

        if action is None:
            # if no action happened, tile is now dead
            deadTiles.append(tossedTile)
                
        tossedTile = playerTurn(players[turn], action, tossedTile, deck)


def playerTurn(player, action, tossedTile, deck):
    # performs one turn. Only gets called if no Hu can occur

    # dont let player draw a tile if they performed an action
    if action == 'pong':
        player.pong(tossedTile)
    elif action == 'kong':
        player.kong(tossedTile)
    elif action == 'chi':
        player.chi(tossedTile)
    else:
        player.drawTile(deck)
    
    # must toss tile
    tileToToss = player.tossTile()
    return tileToToss

def startGame():
    players = initPlayers()
    playRound(players)

