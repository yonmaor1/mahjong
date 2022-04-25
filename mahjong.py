from player import *
from globals import *
from displays import *

def getDeck():
    # returns a complete deck (still missing flowers / seasons)
    deck = []
    # populate the deck: siuted values are 1-9, 4 tiles of each
    for i in range(1,10):
        deck += [Tile(i, 'circle', 'deck', None) for j in range(4)]
    for i in range(1,10):
        deck += [Tile(i, 'stick', 'deck', None) for j in range(4)]
    for i in range(1,10):
        deck += [Tile(i, 'number', 'deck', None) for j in range(4)]

    # directions
    deck += [Tile('dung', None, 'deck', None) for j in range(4)]
    deck += [Tile('nan', None, 'deck', None) for j in range(4)]
    deck += [Tile('xi', None, 'deck', None) for j in range(4)]
    deck += [Tile('bei', None, 'deck', None) for j in range(4)]

    # dragons
    deck += [Tile('zhong', None, 'deck', None) for j in range(4)]
    deck += [Tile('fa', None, 'deck', None) for j in range(4)]
    deck += [Tile('box', None, 'deck', None) for j in range(4)]

    # seasons / flowers
    # deck += [Tile(None, 'flower', 'deck', None) for j in range(4)]
    # deck += [Tile(None, 'season', 'deck', None) for j in range(4)]

    random.shuffle(deck)

    for i in range(0, len(deck[:-1]), 2):
        topTile = deck[i]
        bottomTile = deck[i+1]
        topTile.index = bottomTile.index = (i // 2) % stacksPerSide
        topTile.side = bottomTile.side = (i // 2) // stacksPerSide

    print(len(deck))
    return deck

def initPlayers(player1Name):
    # creates 4 player objects, returns them in a list
    player1 = Player(player1Name, 0, False)
    player2 = Player('Mimi', 1, True)
    player3 = Player('Sean', 2, True)
    player4 = Player('Wesley', 3, True)

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

def checkForAction(players, tossedTile, deadTiles, turn, deck, screen):
    # called in endTurn > while not gameOver()
    # check if players want to Kong / Pong
    displayTossed(tossedTile, players, players[0], turn, deadTiles, deck, screen)
    pygame.display.update()
    for player in [ players[(turn+0)%4], players[(turn+1)%4], players[(turn+2)%4] ]:
        action = None
        if player.canPong(tossedTile):
            # Kong if and only if Pong
            if player.canKong(tossedTile):
                if player.isAI:
                    action = 'kong'
                    turn = player.num
                    break
                else:
                    rects, booleans = displayButtons(player, tossedTile, turn, screen)
                    action = getAction(rects, booleans)
            else:
                if player.isAI:
                    action = 'pong'
                    turn = player.num
                    break
                else:
                    rects, booleans = displayButtons(player, tossedTile, turn, screen)
                    action = getAction(rects, booleans)
            
            if action == 'kong': 
                turn = player.num
                break
            elif action == 'pong': 
                turn = player.num
                break
            elif action == 'hu':
                turn = player.num
                break
            else:
                action = None
    return action, turn

def initGame(players):
    # initializes game attributes
    deck = getDeck()
    deadTiles = []
    turn = 0
    giveHands(players, deck)
    # if dealer wins they stay dealer
    dealer = players[0]

    return deck, deadTiles, turn, dealer

def firstTurn(players, deck, deadTiles, turn):
    
    # first turn (must draw new tile)
    players[0].drawTile(deck)
    tossedTile = players[0].tossTile()

    return deck, tossedTile, deadTiles, turn

def endTurn(players, deck, tossedTile, deadTiles, turn, dealer, screen):

    turn = (turn + 1) % 4

    # to make sure player doesn't Stanley (pong / chi then draw a tile)
    action = None

    # check if anyone can Pong / Kong
    # if so, skip to their turn
    action, turn = checkForAction(players, tossedTile, deadTiles, turn, deck, screen)
    
    # if nobody Pongs/Kongs, check for Chi (only following player can Chi)
    nextPlayer = players[turn]
    if (action is None) and (nextPlayer.canChi(tossedTile)):
        if nextPlayer.isAI:
            action = 'chi'
        else:
            rects, booleans = displayButtons(nextPlayer, tossedTile, turn, screen)
            action = getAction(rects, booleans)

    if action == None or action == False:
        # if no action happened, tile is now dead
        deadTiles.append(tossedTile)

    displayButtons(players[turn], None, turn, screen)
    pygame.display.update()

    return deck, tossedTile, action, deadTiles, turn, dealer

def startTurn(player, action, tossedTile, deck):
    # performs one turn. Only gets called if no Hu can occur

    # dont let player Stanley (draw a tile if they performed an action)
    if action == 'pong':
        player.pong(tossedTile)
        drawnTile = None
    elif action == 'kong':
        # Kong draws tile from the back 
        player.kong(tossedTile)
        drawnTile = player.drawTile(deck)
    elif action == 'chi':
        player.chi(tossedTile)
        drawnTile = None
    else:
        drawnTile = player.drawTile(deck)

    return drawnTile, deck
    
    
def middleTurn(player, players, turn, drawnTile, deadTiles, deck, screen):
    # must toss tile
    if player.isAI:
        tileToToss = player.tossTileAI()
    else:
        tileToToss = player.getTossedTile(drawnTile)
        if tileToToss != drawnTile:
            player.tossTile(tileToToss)

    displayTossed(None, players, players[0], turn, deadTiles, deck, screen)
    pygame.display.update()
    time.sleep(0.5)
    
    if tileToToss != drawnTile and tileToToss != None:
        # only now add the drawn tile to the hand (if it wasn't thrown out)
        player.hand.append(drawnTile)
    
    return tileToToss


def endGame(players, turn, dealer, screen):
    # somebody can Hu
    for player in players:
        if player.won:
            winner = player
            print(f'{winner.name} won!!')
            for tile in winner.hand:
                tile.location = 'hu'
                tile.update()
                tile.draw(screen)
            pygame.display.update()
            # whoever tossed out winning card is loser, unless winner drew card
            # not using loser rn, might impliment betting / drinking  
            losers = [ players[turn] ]
            if losers[0] is winner:
                losers = [  players[(turn + 1) % 4], 
                            players[(turn + 2) % 4], 
                            players[(turn + 3) % 4] ]
    
    '''keepPlaying = input(f'{winner.name} won! Keep playing?')

    if not keepPlaying:
        # want to quit game
        return

    # BUG: reset must happen in game.py
    if winner is dealer:
        # if dealer won they stay dealer
        endTurn(players)

    else:
        # if dealer lost, player 1 becomes dealer
        for player in players:
            player.num = (player.num + 1) % 4
        endTurn(players)
    '''
