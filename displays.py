from tile import *
from globals import *

def displayHand(hand, screen):
    for i in range(len(hand)):
        tile = hand[i]

        # same fix as in displayOtherHands, still bad
        if tile is None:
                hand.remove(tile)
                i -= 1
                continue
        
        tile.x, tile.y = (  MARGIN + tile.width * i, 
                            HEIGHT - tile.height - MARGIN)
        
        tile.update()
        tile.draw(screen)

def displayDrawn(tile, hand, players, activePlayer, turn, deadTiles, deck, tossedTile, screen):
    if tile is None:
        return

    xFinal, yFinal = (  MARGIN + len(hand) * tile.width + MARGIN, 
                        HEIGHT - tile.height - MARGIN)
    slideTile(tile, screen, xFinal, yFinal, players, activePlayer, turn, deadTiles, deck, tossedTile)

    tile.update()
    tile.draw(screen)

def displayRevealed(revealed, players, activePlayer, turn, deadTiles, deck, tossedTile, screen):
    index = 0
    for set in revealed:
        for i in range(len(set)):
            tile = set[i]
            tile.location = 'revealed'
            offset = 10 * (index // 3)
            xFinal, yFinal = (  MARGIN + offset + tile.width * index, 
                                HEIGHT - 2.2*tile.height - MARGIN)
            slideTile(tile, screen, xFinal, yFinal, players, activePlayer, turn, deadTiles, deck, tossedTile)
            
            tile.update()
            tile.draw(screen)
            index += 1

def displayDead(deadTiles, players, activePlayer, turn, deck, tossedTile, screen):
    # where to start drawing dead tiles
    deadX, deadY = (WIDTH - MARGIN - rowLength + MARGIN, 
                    HEIGHT - stacksPerSide * tileWidth)

    for i in range(len(deadTiles)):
        tile = deadTiles[i]
        xFinal, yFinal = (  deadX + (i % tilesPerRow) * tileWidth, 
                            deadY + (i // tilesPerRow) * tileHeight)
        slideTile(tile, screen, xFinal, yFinal, players, activePlayer, turn, deadTiles, deck, tossedTile)
        
        tile.update()
        tile.draw(screen)

def displayTossed(tile, players, activePlayer, turn, deadTiles, deck, screen):
    if tile is None:
        return

    deadX, deadY = (WIDTH - MARGIN - rowLength + MARGIN, 
                    HEIGHT - stacksPerSide * tileWidth)
    xFinal, yFinal = (  deadX + (len(deadTiles) % tilesPerRow) * tileWidth + 10, 
                        deadY + (len(deadTiles) // tilesPerRow) * tileHeight + 10)
    slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, None)
    tile.update()
    tile.draw(screen)

def displayOtherHands(players, activePlayer, turn, deadTiles, deck, tossedTile, screen):
    num = activePlayer.num
    passivePlayers = [ players[(num+1)%4], players[(num+2)%4], players[(num+3)%4] ]
    for player in passivePlayers:
        playerNum = passivePlayers.index(player) + 1
        for i in range(len(player.hand)):
            tile = player.hand[i]

            # BUG: when player tries to pong / chi draw tile is Nonetype
            # horrendous fix to this bug...
            if tile is None:
                player.hand.remove(tile)
                i -= 1
                continue

            tile.theta = playerNum * 90
            tile.location = 'passiveHand'
            if playerNum == 1:
                xFinal, yFinal = (  WIDTH - MARGIN - tileDepth, 
                                    HEIGHT - MARGIN - i * tileWidth - tileWidth)
                slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, tossedTile)

                tile.update()
                tile.draw(screen)
            elif playerNum == 2:
                xFinal, yFinal = (  WIDTH - MARGIN - i * tileWidth - tileWidth, 
                                    MARGIN)
                slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, tossedTile)

                tile.update()
                tile.draw(screen)
            elif playerNum == 3:
                xFinal, yFinal = (  MARGIN, 
                                    MARGIN + i * tileWidth)
                slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, tossedTile)

                tile.update()
                tile.draw(screen)

def displayOtherRevealed(players, activePlayer, turn, deadTiles, deck, tossedTile, screen):
    num = activePlayer.num
    passivePlayers = [ players[(num+1)%4], players[(num+2)%4], players[(num+3)%4] ]
    for player in passivePlayers:
        playerNum = passivePlayers.index(player) + 1
        tileIndex = 0
        for set in player.revealed:
            setIndex = player.revealed.index(set)
            for i in range(len(set)):
                tile = set[i]
                tile.theta = playerNum * 90
                offset = 10 * setIndex

                if playerNum == 1:
                    xFinal, yFinal = (  WIDTH - MARGIN - 2 * tileDepth - tileHeight, 
                                        HEIGHT - MARGIN - tileIndex * tileWidth - tileWidth - offset)
                    slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, tossedTile)

                    tile.update()
                    tile.draw(screen)
                elif playerNum == 2:
                    xFinal, yFinal = (  WIDTH - MARGIN - tileIndex * tileWidth - tileWidth - offset, 
                                        MARGIN + 2 * tileDepth)
                    slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, tossedTile)

                    tile.update()
                    tile.draw(screen)
                elif playerNum == 3:
                    xFinal, yFinal = (  MARGIN + 2 * tileDepth, 
                                        MARGIN + tileIndex * tileWidth + offset)
                    slideTile(tile, screen, xFinal, yFinal,  players, activePlayer, turn, deadTiles, deck, tossedTile)

                    tile.update()
                    tile.draw(screen)
            
                tileIndex += 1

def displayDeck(deck, screen):
    for i in range(0, len(deck[:-1]), 2):
        topTile = deck[i]
        bottomTile = deck[i+1]

        if topTile.side == 0:
            x, y = (MARGIN + topTile.width * topTile.index, 
                    HEIGHT - topTile.height * 2 - MARGIN * 3)

            topTile.x, topTile.y = bottomTile.x, bottomTile.y = x, y 
            
            topTile.draw(screen)
            bottomTile.draw(screen)

        if topTile.side == 1:
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
            topTile.theta = 270
            bottomTile.theta = 270

            x, y = (WIDTH - MARGIN - rowLength - tileHeight,
                    MARGIN + (tileWidth * topTile.index) )
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

def chatBox(text, screen):
    fontHeight = 32
    font = pygame.font.Font(None, fontHeight)
    prompt = 'CHAT:'
    inputW, inputH = SIDEBAR - 2*MARGIN, SIDEBAR - MARGIN
    inputBox = pygame.Rect(WIDTH + MARGIN, 2*MARGIN, inputW, inputH)
    color = (140,140,140)
    text = f'>>>{text}'

    pygame.draw.rect(screen, color, inputBox)

    # Render the current text.
    textSurface = font.render(text, True, WHITE)
    promptSurface = font.render(prompt, True, color)
    
    # Blit the text.
    screen.blit(promptSurface, (inputBox.x, inputBox.y - fontHeight))
    screen.blit(textSurface, (inputBox.x+5, inputBox.y+5))
    # Blit the inputBox rect.
    pygame.draw.rect(screen, color, inputBox, 2)
    pygame.display.update()

def displayButtons(player, tossedTile, turn, screen):
    buttonWidth = SIDEBAR - 2*MARGIN
    buttonHeight = 3*MARGIN

    passButton = pygame.Rect( WIDTH + MARGIN, HEIGHT - 1*(MARGIN + buttonHeight), 
                            buttonWidth, buttonHeight)
    huButton = pygame.Rect( WIDTH + MARGIN, HEIGHT - 2*(MARGIN + buttonHeight), 
                            buttonWidth, buttonHeight)
    chiButton = pygame.Rect(WIDTH + MARGIN, HEIGHT - 3*(MARGIN + buttonHeight), 
                            buttonWidth, buttonHeight)
    kongButton = pygame.Rect(WIDTH + MARGIN, HEIGHT - 4*(MARGIN + buttonHeight), 
                            buttonWidth, buttonHeight)
    pongButton = pygame.Rect(WIDTH + MARGIN, HEIGHT - 5*(MARGIN + buttonHeight), 
                            buttonWidth, buttonHeight)

    rects = [ pongButton, kongButton, chiButton, huButton, passButton ]

    fontHeight = buttonHeight - 4
    font = pygame.font.Font(None, fontHeight)
    
    pongText = font.render('pong', True, WHITE)
    kongText = font.render('kong', True, WHITE)
    chiText = font.render('chi', True, WHITE)
    huText = font.render('hu', True, WHITE)
    passText = font.render('pass', True, WHITE)

    texts = [ pongText, kongText, chiText, huText, passText ]

    if tossedTile is None:
        booleans = [ False, False, False, False, False ]
    else:
        playerTurn = player.num
        canChi = player.canChi(tossedTile) and turn == playerTurn

        booleans = [player.canPong(tossedTile), player.canKong(tossedTile), 
                    canChi, player.canHu(tossedTile)]
        canPass = (turn == playerTurn) and (True in booleans)
        booleans.append(canPass)
    
    for i in range(len(rects)):
        rect = rects[i]
        text = texts[i]

        if booleans[i]:
            color = GREEN
        else:
            color = (140,140,140)

        pygame.draw.rect(screen, color, rect, 0, 5)
        screen.blit(text, (rect.x+5, rect.y+5))

    return rects, booleans

def getAction(rects, booleans):
    actions = [ 'pong', 'kong', 'chi', 'hu', False ]
    # if player wants to pass, action is False
    action = None
    while action is None:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(rects)):
                        button = rects[i]
                        canAction = booleans[i]
                        # If the user clicked on the inputBox rect.
                        if button.collidepoint(event.pos) and canAction:
                            # Toggle the active variable.
                            action = actions[i]
                            return action

def displaySidebar(screen, text=''):
    sideBar = pygame.Rect(WIDTH, 0, SIDEBAR, HEIGHT)
    pygame.draw.rect(screen, WHITE, sideBar)
    chatBox(text, screen)
    pygame.display.update()

def slideTile(tile, screen, x1, y1, players, activePlayer, turn, deadTiles, deck, tossedTile, xStep = 5):
    if tile is None:
        return

    x0, y0 = tile.x, tile.y
    if ((x0, y0) == (0,0) or (x0, y0) == (x1, y1)):
        # don't slide when initializing game or redrawing
        tile.x, tile.y = x1, y1
        # self.update()
        # self.draw(screen)
        # pygame.display.update()
        return 

    try:
        xSteps = int(abs(x1 - x0) // xStep)
        yStep = abs(y1 - y0) / xSteps
        xPositions = frange(x0, x1, xStep)
        yPositions = frange(y0, y1, yStep)
        for i in range(xSteps + 1):
            if i > 0:
                # erase last drawing
                prevRect = pygame.Rect( xPositions[i-1], yPositions[i-1], 
                                        tile.width, tile.height)
                pygame.draw.rect(screen, GREEN, prevRect)
                for player in players:
                    for tile in player.hand:
                        if prevRect.colliderect(tile.rect):
                            tile.draw(screen)
                for tile in deck:
                    if prevRect.colliderect(tile.rect):
                        tile.draw(screen)
                for tile in deadTiles:
                    if prevRect.colliderect(tile.rect):
                        tile.draw(screen)
                if tossedTile != None:
                    if prevRect.colliderect(tossedTile.rect):
                            tile.draw(screen)

            xPos = xPositions[i]
            yPos = yPositions[i]
            tile.x, tile.y = xPos, yPos
            tile.update()
            tile.draw(screen)
            pygame.display.update()

    except:
        if tile is None:
            return
            
        tile.x, tile.y = x1, y1
        tile.update()
        tile.draw(screen)
        pygame.display.update()
        return 

def displayAll(players, activePlayer, turn, deadTiles, deck, tossedTile, screen):
    pygame.draw.rect(screen, GREEN, BOARD)
    displayHand(activePlayer.hand, screen)
    displayOtherHands(players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
    displayRevealed(activePlayer.revealed, players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
    displayOtherRevealed(players, activePlayer, turn, deadTiles, deck, tossedTile, screen)
    displayDead(deadTiles, players, activePlayer, turn, deck, tossedTile, screen)
    displayDeck(deck, screen)
    displaySidebar(screen)
    displayButtons(activePlayer, tossedTile, turn, screen)
    pygame.display.update()