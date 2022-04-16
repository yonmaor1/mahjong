from player import *
from pygame.locals import *
import pygame, sys, random

def getDeck():
    # returns a complete deck (still missing flowers / seasons)
    deck = []
    # populate the deck: siuted values are 1-9, 4 tiles of each
    for i in range(1,10):
        deck += [(i, 'circle') for j in range(4)]
    for i in range(1,10):
        deck += [(i, 'stick') for j in range(4)]
    for i in range(1,10):
        deck += [(i, 'number') for j in range(4)]

    # directions
    deck += [('dung', None) for j in range(4)]
    deck += [('nan', None) for j in range(4)]
    deck += [('xi', None) for j in range(4)]
    deck += [('bei', None) for j in range(4)]

    # dragons
    deck += [('zhong', None) for j in range(4)]
    deck += [('fa', None) for j in range(4)]
    deck += [('box', None) for j in range(4)]

    # add seasons / flowers later

    return deck

def initPlayers():
    # creates 4 player objects, returns them in a list
    player1Name = input('Enter Player 1s Name:')
    player1isAI = input('Make Player 1 an AI?')

    player2Name = input('Enter Player 2s Name:')
    player2isAI = input('Make Player 2 an AI?')

    player3Name = input('Enter Player 3s Name:')
    player3isAI = input('Make Player 3 an AI?')

    player4Name = input('Enter Player 4s Name:')
    player4isAI = input('Make Player 4 an AI?')

    player1 = Player(player1Name, 0, player1isAI)
    player2 = Player(player2Name, 1, player2isAI)
    player3 = Player(player3Name, 2, player3isAI)
    player4 = Player(player4Name, 3, player4isAI)

    players = [player1, player2, player3, player4]

    return players

def gameOver(players, tossedTile):
    # checks if game has ended (ie if any player can end the game)
    if (players[0].canHu(tossedTile) or
        players[1].canHu(tossedTile) or
        players[2].canHu(tossedTile) or
        players[3].canHu(tossedTile)):
        return True
    return False

def checkForAction(players, tossedTile, turn):
    # called in playRound > while not gameOver()
    # check if players want to Kong / Pong
    for player in [ players[turn], players[(turn+1)%4], players[(turn+2)%4] ]:
        action = None
        if player.canPong(tossedTile):
            # Kong if and only if Pong
            if player.canKong(tossedTile):
                if player.isAI:
                    action = 'kong'
                    turn = player.num
                    break
                else:
                    # input must be bool
                    wantsToKong = input(f'{player.name} can Kong. Would you like to?')
            else:
                if player.isAI:
                    action = 'pong'
                    turn = player.num
                    break
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
    return action, turn

def firstTurn(players):
    # initializes game attributes
    deck = getDeck()
    deadTiles = []
    turn = 0
    giveHands(players, deck)
    # if dealer wins they stay dealer
    dealer = players[0]

    # first turn (must draw new tile)
    players[0].drawTile(deck)
    tossedTile = players[0].tossTile()

    return deck, tossedTile, deadTiles, turn, dealer

def playRound(players, deck, tossedTile, deadTiles, turn, dealer):

    # rest of the turns (a tossed tile exists)
    if not gameOver(players, tossedTile):

        # to make sure player doesn't Stanley (pong / chi then draw a tile)
        action = None

        # check if anyone can Pong / Kong
        # if so, skip to their turn 
        action, turn = checkForAction(players, tossedTile, turn)
        
        # if nobody Pongs/Kongs, check for Chi (only following player can Chi)
        nextPlayer = players[(turn + 1) % 4]
        if (action is None) and (nextPlayer.canChi(tossedTile)):
            if nextPlayer.isAI:
                action = 'chi'
            else:
                # input must be bool
                wantsToChi = input(f'{nextPlayer.name} can Chi. Would you like to?')
                if wantsToChi:
                    action = 'chi'

        if action is None:
            # if no action happened, tile is now dead
            deadTiles.append(tossedTile)
                
        turn = (turn + 1) % 4
        tossedTile = playerTurn(players[turn], action, tossedTile, deck)

    if gameOver(players, tossedTile):
        # somebody can Hu
        for player in players:
            if player.won:
                winner = player
                # whoever tossed out winning card is loser, unless winner drew card
                # not using loser rn, might impliment betting / drinking  
                losers = [ players[turn] ]
                if losers[0] is winner:
                    losers = [  players[(turn + 1) % 4], 
                                players[(turn + 2) % 4], 
                                players[(turn + 3) % 4] ]
                keepPlaying = input(f'{winner.name} won! Keep playing?')

        if not keepPlaying:
            # want to quit game
            return

        if winner is dealer:
            # if dealer won they stay dealer
            playRound(players)

        else:
            # if dealer lost, player 1 becomes dealer
            for player in players:
                player.num = (player.num + 1) % 4
            playRound(players)
    return deck, tossedTile, deadTiles, turn, dealer


def playerTurn(player, action, tossedTile, deck):
    # performs one turn. Only gets called if no Hu can occur

    # dont let player draw a tile if they performed an action
    if action == 'pong':
        player.pong(tossedTile)
    elif action == 'kong':
        # Kong draws tile from the back 
        player.kong(tossedTile)
        player.drawTile(deck)
    elif action == 'chi':
        player.chi(tossedTile)
    
    else:
        player.drawTile(deck)
    
    # must toss tile
    if player.isAI:
        tileToToss = player.tossTileAI()
    else:
        tileToToss = player.tossTile()
    
    return tileToToss

