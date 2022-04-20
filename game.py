from mahjong import *

pygame.init()

FPS = pygame.time.Clock()

WHITE = (255,255,255)

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

running = True

def displayHand(hand, screen):
    for i in range(len(hand)):
        tile = hand[i]
        margin = (WIDTH - tile.width * 16) / 2
        
        tile.x, tile.y = (  margin + tile.width * i, 
                            HEIGHT - tile.height - margin)
        
        tile.update()
        tile.draw(screen)

def displayRevealed(revealed, screen):
    index = 0
    for set in revealed:
        for i in range(len(set)):
            tile = set[i]
            margin = (WIDTH - tile.width * 16) / 2
            offset = 10 * (index // 3)
            tile.x, tile.y = (  margin + offset + tile.width * index, 
                                HEIGHT - 2.2*tile.height - margin)
            
            tile.update()
            tile.draw(screen)
            index += 1

def displayDeadTiles(deadTiles, screen):
    # where to start drawing dead tiles
    deadX, deadY = 100, 100
    tilesPerRow = 10

    for i in range(len(deadTiles)):
        tile = deadTiles[i]
        tile.x, tile.y = (  deadX + (i % tilesPerRow) * tile.width, 
                            deadY + (i // tilesPerRow) * tile.height)
        
        tile.update()
        tile.draw(screen)

def getActiveName(screen):
    font = pygame.font.Font(None, 32)
    prompt = 'please enter your name:'
    inputW, inputH = 140, 32
    inputBox = pygame.Rect((WIDTH - inputW)/2, (HEIGHT - inputH)/2, inputW, inputH)
    colorInactive = pygame.Color('lightskyblue3')
    colorActive = pygame.Color('dodgerblue2')
    color = colorInactive
    active = False
    text = ''
    gettingName = True

    while gettingName:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the inputBox rect.
                    if inputBox.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = colorActive if active else colorInactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill(WHITE)

        # Render the current text.
        txtSurface = font.render(text, True, color)
        promptSurface = font.render(prompt, True, color)
        # Resize the box if the text is too long.
        width = max(200, txtSurface.get_width()+10)
        inputBox.w = width
        # Blit the text.
        screen.blit(promptSurface, (inputBox.x, inputBox.y-32))
        screen.blit(txtSurface, (inputBox.x+5, inputBox.y+5))
        # Blit the inputBox rect.
        pygame.draw.rect(screen, color, inputBox, 2)
        pygame.display.update()

def getTossedTile(player):
    # check for mouse press to toss tile
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for tile in player.hand:
                    if tile.rect.collidepoint(pos):
                        tossedTile = tile
                        return tossedTile

def runGame():
    activeName = getActiveName(screen)
    screen.fill(WHITE)

    players = initPlayers(activeName)
    # BUG: active player will change after a round ends
    activePlayer = players[0]
    deck, deadTiles, turn, dealer = initGame(players)
    
    displayHand(activePlayer.hand, screen)
    pygame.display.update()
    
    #deck, tossedTile, deadTiles, turn = firstTurn(players, deck, deadTiles, turn)
    players[0].drawTile(deck)
    tossedTile = getTossedTile(players[0])

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        (deck, tossedTile, action, deadTiles, turn, dealer) = playRound(players,
                                                                        deck, 
                                                                        tossedTile, 
                                                                        deadTiles, 
                                                                        turn, 
                                                                        dealer)

        playerTurn(players[turn], action, tossedTile, deck)

        if players[turn] == activePlayer:
            tossedTile = getTossedTile(players[0])
        else:
            tossedTile = players[turn].tossTileAI()

        

        screen.fill(WHITE)
        displayHand(activePlayer.hand, screen)
        displayRevealed(activePlayer.revealed, screen)
        displayDeadTiles(deadTiles, screen)

        pygame.display.update()
        FPS.tick(30)

    
runGame()