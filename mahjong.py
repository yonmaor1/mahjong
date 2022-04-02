from player import *
import random

def makeDeck():
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
    player1Name = input('Enter Player 1s Name:')
    player1isAI = input('Make Player 1 an AI?')

    player2Name = input('Enter Player 1s Name:')
    player2isAI = input('Make Player 1 an AI?')

    player3Name = input('Enter Player 1s Name:')
    player3isAI = input('Make Player 1 an AI?')

    player4Name = input('Enter Player 1s Name:')
    player4isAI = input('Make Player 1 an AI?')

    player1 = Player(player1Name, player1isAI)
    player2 = Player(player2Name, player2isAI)
    player3 = Player(player3Name, player3isAI)
    player4 = Player(player4Name, player4isAI)

    return player1, player2, player3, player4    

def playRound(player1, player2, player3, player4):
    deck = makeDeck()
    giveHands(player1, player2, player3, player4, deck)
    player1.isDealer = True
    ### STOPPED HERE
    playerTurn(player1, deck)

def playerTurn(player, tossedTile, deck):
    player.drawTile(deck)
    player.tossTile()

def startGame():
    player1, player2, player3, player4 = initPlayers()
    playRound(player1, player2, player3, player4)





