from mahjong import *
from globals import *

pygame.init()

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    displayOtherHands(players, activePlayer, screen)
    displayDrawn(drawnTile, activePlayer.hand, screen)
    displayDeck(deck, screen)
    pygame.display.update()
    
    #deck, tossedTile, deadTiles, turn = firstTurn(players, deck, deadTiles, turn)
    tossedTile = activePlayer.getTossedTile(drawnTile)
    

    if tossedTile != drawnTile:
        activePlayer.tossTile(tossedTile)
        activePlayer.hand.append(drawnTile)

    displayHand(activePlayer.hand, screen)
    displayOtherHands(players, activePlayer, screen)
    displayRevealed(activePlayer.revealed, screen)
    displayOtherRevealed(players, activePlayer, screen)
    displayDead(deadTiles, screen)
    displayDeck(deck, screen)
    pygame.display.update()

    while not gameOver(players, tossedTile):
        # print(player.hand for player in players)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        (deck, tossedTile, action, deadTiles, turn, dealer) = endTurn(  players,
                                                                        deck, 
                                                                        tossedTile, 
                                                                        deadTiles, 
                                                                        turn, 
                                                                        dealer)

        drawnTile, deck = startTurn(players[turn], action, tossedTile, deck)

        print(drawnTile is None)

        screen.fill(GREEN)
        displayHand(activePlayer.hand, screen)
        displayOtherHands(players, activePlayer, screen)
        displayRevealed(activePlayer.revealed, screen)
        displayOtherRevealed(players, activePlayer, screen)
        if turn == activePlayer.num and not (drawnTile is None):
            displayDrawn(drawnTile, activePlayer.hand, screen)
        displayDead(deadTiles, screen)
        displayDeck(deck, screen)
        pygame.display.update()

        tossedTile = middleTurn(players[turn], drawnTile, deadTiles, screen)

        screen.fill(GREEN)
        displayHand(activePlayer.hand, screen)
        displayOtherHands(players, activePlayer, screen)
        displayRevealed(activePlayer.revealed, screen)
        displayOtherRevealed(players, activePlayer, screen)
        displayDead(deadTiles, screen)
        displayDeck(deck, screen)
        pygame.display.update()
        FPS.tick(30)

    # exited while loop
    endGame(players, turn, dealer)

    
runGame()