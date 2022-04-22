from tile import *
from globals import *

def displayHand(hand, screen):
    # print(len(hand))
    for i in range(len(hand)):
        tile = hand[i]
        
        tile.x, tile.y = (  MARGIN + tile.width * i, 
                            HEIGHT - tile.height - MARGIN)
        
        tile.update()
        tile.draw(screen)

def displayDrawn(tile, hand, screen):
    tile.x, tile.y = (  MARGIN + len(hand) * tile.width + MARGIN, 
                        HEIGHT - tile.height - MARGIN)

    tile.update()
    tile.draw(screen)

def displayRevealed(revealed, screen):
    index = 0
    for set in revealed:
        for i in range(len(set)):
            tile = set[i]
            offset = 10 * (index // 3)
            tile.x, tile.y = (  MARGIN + offset + tile.width * index, 
                                HEIGHT - 2.2*tile.height - MARGIN)
            
            tile.update()
            tile.draw(screen)
            index += 1

def displayDead(deadTiles, screen):
    # where to start drawing dead tiles
    deadX, deadY = (WIDTH - MARGIN - rowLength + MARGIN, 
                    HEIGHT - stacksPerSide * tileWidth)

    for i in range(len(deadTiles)):
        tile = deadTiles[i]
        tile.x, tile.y = (  deadX + (i % tilesPerRow) * tileWidth, 
                            deadY + (i // tilesPerRow) * tileHeight)
        
        tile.update()
        tile.draw(screen)

def displayTossed(tile, deadTiles, screen):
    deadX, deadY = (WIDTH - MARGIN - rowLength + MARGIN, 
                    HEIGHT - stacksPerSide * tileWidth)
    tile.x, tile.y = (  deadX + (len(deadTiles) % tilesPerRow) * tileWidth + 10, 
                        deadY + (len(deadTiles) // tilesPerRow) * tileHeight + 10)

    tile.update()
    tile.draw(screen)

def displayOtherHands(players, activePlayer, screen):
    num = activePlayer.num
    passivePlayers = [ players[(num+1)%4], players[(num+2)%4], players[(num+3)%4] ]
    for player in passivePlayers:
        playerNum = passivePlayers.index(player) + 1
        for i in range(len(player.hand)):
            tile = player.hand[i]
            tile.theta = playerNum * 90
            tile.location = 'passiveHand'
            if playerNum == 1:
                tile.x, tile.y = (  WIDTH - MARGIN - tileDepth, 
                                    HEIGHT - MARGIN - i * tileWidth - tileWidth)

                tile.update()
                tile.draw(screen)
            elif playerNum == 2:
                tile.x, tile.y = (  WIDTH - MARGIN - i * tileWidth - tileWidth, 
                                    MARGIN)

                tile.update()
                tile.draw(screen)
            elif playerNum == 3:
                tile.x, tile.y = (  MARGIN, 
                                    MARGIN + i * tileWidth)

                tile.update()
                tile.draw(screen)

def displayOtherRevealed(players, activePlayer, screen):
    num = activePlayer.num
    passivePlayers = [ players[(num+1)%4], players[(num+2)%4], players[(num+3)%4] ]
    for player in passivePlayers:
        playerNum = passivePlayers.index(player) + 1
        index = 0
        for set in player.revealed:
            for i in range(len(set)):
                tile = set[i]
                tile.theta = playerNum * 90
                offset = 10 * (index // 3)

                if playerNum == 1:
                    tile.x, tile.y = (  WIDTH - MARGIN - 2*tileDepth - tileHeight, 
                                        HEIGHT - MARGIN - i * tileWidth - tileWidth)

                    tile.update()
                    tile.draw(screen)
                elif playerNum == 2:
                    tile.x, tile.y = (  WIDTH - MARGIN - i * tileWidth - tileWidth, 
                                        MARGIN + 2*tileDepth)

                    tile.update()
                    tile.draw(screen)
                elif playerNum == 3:
                    tile.x, tile.y = (  MARGIN + 2*tileDepth, 
                                        MARGIN + i * tileWidth)

                    tile.update()
                    tile.draw(screen)

                tile.x, tile.y = (  MARGIN + offset + tile.width * index, 
                                    HEIGHT - 2.2*tile.height - MARGIN)
                
            
                index += 1

def displayDeck(deck, screen):
    for i in range(0, len(deck[:-1]), 2):
        topTile = deck[i]
        bottomTile = deck[i+1]

        if topTile.side == 0:
            # print('side 0:', end='')
            # print(topTile.index)
            x, y = (MARGIN + topTile.width * topTile.index, 
                    HEIGHT - topTile.height * 2 - MARGIN * 3)

            topTile.x, topTile.y = bottomTile.x, bottomTile.y = x, y 
            
            topTile.draw(screen)
            bottomTile.draw(screen)

        if topTile.side == 1:
            # print('side 1:', end='')
            # print(topTile.index)
            topTile.theta = 90
            bottomTile.theta = 90


            x, y = (MARGIN + rowLength,
                    HEIGHT - (topTile.width * topTile.index) - tileHeight )
            topTile.x, topTile.y = bottomTile.x, bottomTile.y = x, y

            topTile.update()
            bottomTile.update()
            
            topTile.draw(screen)
            bottomTile.draw(screen)

        if topTile.side == 2:
            # print('side 2:', end='')
            # print(topTile.index)
            topTile.theta = 180
            bottomTile.theta = 180

            x, y = (WIDTH - MARGIN - (tileWidth * topTile.index) - tileWidth,
                    HEIGHT - MARGIN - rowLength - tileWidth)
            topTile.x, topTile.y = bottomTile.x, bottomTile.y =  x, y

            topTile.update()
            bottomTile.update()

            topTile.draw(screen)
            bottomTile.draw(screen)

        if topTile.side == 3:
            # print('side 3:', end='')
            # print(topTile.index)
            topTile.theta = 270
            bottomTile.theta = 270

            x, y = (WIDTH - MARGIN - rowLength - topTile.height,
                    MARGIN + (topTile.width * topTile.index) )
            topTile.x, topTile.y = bottomTile.x, bottomTile.y = x, y
            
            topTile.update()
            bottomTile.update()

            topTile.draw(screen)
            bottomTile.draw(screen)

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
