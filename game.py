from mahjong import *
from globals import *

pygame.init()

# screen
screen = pygame.display.set_mode((WIDTH + SIDEBAR, HEIGHT))
screen.fill(GREEN)

running = True


def runGame():
    activeName = getActiveName(screen)
    screen.fill(GREEN)

    players = initPlayers(activeName)
    # BUG: active player will change after a round ends
    activePlayer = players[0]
    deck, deadTiles, turn, dealer = initGame(players)
    drawnTile = activePlayer.drawTile(deck)
    
    displayHand(activePlayer.hand, screen)
    displayOtherHands(players, activePlayer, turn, deadTiles, deck, None, screen)
    displayDrawn(drawnTile, activePlayer.hand, players, activePlayer, turn, deadTiles, deck, None, screen)
    displayDeck(deck, screen)
    displaySidebar(screen)
    displayButtons(activePlayer, None, 0, screen)
    pygame.display.update()

    tossedTile = activePlayer.getTossedTile(drawnTile)
    
    if tossedTile != drawnTile:
        activePlayer.tossTile(tossedTile)
        activePlayer.hand.append(drawnTile)

    displayAll(players, activePlayer, turn, deadTiles, deck, tossedTile, screen)

    while not gameOver(players, tossedTile):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        (deck, tossedTile, action, deadTiles, turn, dealer) = endTurn(  players,
                                                                        deck, 
                                                                        tossedTile, 
                                                                        deadTiles, 
                                                                        turn, 
                                                                        dealer, 
                                                                        screen)

        drawnTile, deck = startTurn(players[turn], action, tossedTile, deck)

        pygame.draw.rect(screen, GREEN, BOARD)
        displayHand(activePlayer.hand, screen)
        if turn == activePlayer.num and not (drawnTile is None):
            displayDrawn(drawnTile, activePlayer.hand, players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
        displayOtherHands(players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
        displayRevealed(activePlayer.revealed, players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
        displayOtherRevealed(players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
        displayDead(deadTiles, players, activePlayer, turn, deck, tossedTile, screen)
        displayDeck(deck, screen)
        if action != None and action != False:
            displaySidebar(screen, f'{players[turn].name} will {action}')
        else:
            displaySidebar(screen)
        displayButtons(activePlayer, tossedTile, turn, screen)
        pygame.display.update()
        
        tossedTile = middleTurn(players[turn], players, turn, drawnTile, deadTiles, deck, screen)

        displayAll(players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
        FPS.tick(30)

    # exited while loop
    endGame(players, turn, dealer, screen)
    runGame()

    
runGame()