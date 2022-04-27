from mahjong import *
from globals import *

pygame.init()

# screen
screen = pygame.display.set_mode((WIDTH + SIDEBAR, HEIGHT))
screen.fill(GREEN)

running = True


def runGame(activeName = None):
    if activeName is None:
        activeName = getActiveName(screen)

    screen.fill(GREEN)

    players = initPlayers(activeName)
    # BUG: active player will change after a round ends
    activePlayer = players[0]
    deck, deadTiles, turn, dealer = initGame(players)
    drawnTile = activePlayer.drawTile(deck)
    
    pygame.draw.rect(screen, WHITE, SIDEBARRECT, 0)
    displayHand(activePlayer.hand, screen)
    displayOtherHands(players, activePlayer, screen)
    displayDrawn(drawnTile, activePlayer.hand, screen)
    displayDeck(deck, screen)
    displaySidebar(screen)
    displayButtons(activePlayer, None, 0, screen)
    pygame.display.update()

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
    displaySidebar(screen)
    displayButtons(activePlayer, tossedTile, 0, screen)
    pygame.display.update()

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

        if players[turn].canHu(drawnTile):
            players[turn].won = True
            break

        # screen.fill(GREEN)
        displayRevealed(activePlayer.revealed, screen)
        displayHand(activePlayer.hand, screen)
        if turn == activePlayer.num and not (drawnTile is None):
            displayDrawn(drawnTile, activePlayer.hand, screen)
        displayOtherHands(players, activePlayer, screen)
        displayOtherRevealed(players, activePlayer, screen)
        displayDead(deadTiles, screen)
        displayDeck(deck, screen)
        if action != None and action != False:
            displaySidebar(screen, f'{players[turn].name} will {action}')
        else:
            displaySidebar(screen)
        displayButtons(activePlayer, tossedTile, turn, screen)
        pygame.display.flip()

        tossedTile = middleTurn(players[turn], drawnTile, deadTiles, screen)
        for player in players:
            if player.canHu(drawnTile):
                player.won = True
                break

        # screen.fill(GREEN)
        pygame.draw.rect(screen, GREEN, BOARD, 0)
        displayOtherHands(players, activePlayer, screen)
        displayRevealed(activePlayer.revealed, screen)
        displayHand(activePlayer.hand, screen)
        displayOtherRevealed(players, activePlayer, screen)
        displayDead(deadTiles, screen)
        displayDeck(deck, screen)
        displaySidebar(screen)
        displayButtons(activePlayer, tossedTile, turn, screen)
        pygame.display.flip()
        FPS.tick(30)

    # exited while loop
    keepPlaying = endGame(players, turn, screen)
    if keepPlaying:
        runGame(activeName)
    else: 
        pygame.quit()
        sys.exit()


    
runGame()