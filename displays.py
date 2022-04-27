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
    
    handWidth = len(hand) * tileWidth
    coverRect = pygame.Rect(MARGIN + handWidth, HEIGHT - tileHeight - MARGIN, 
                            tileWidth * 4, tileHeight)
    pygame.draw.rect(screen, GREEN, coverRect, 0)

def displayDrawn(tile, hand, screen):
    xFinal, yFinal = (  MARGIN + len(hand) * tile.width + MARGIN, 
                        HEIGHT - tile.height - MARGIN)
    tile.slideTile(screen, xFinal, yFinal)

    tile.update()
    tile.draw(screen)

def displayRevealed(revealed, screen):
    index = 0
    for set in revealed:
        setIndex = revealed.index(set)
        for i in range(len(set)):
            tile = set[i]
            tile.location = 'revealed'
            offset = 10 * setIndex
            xFinal, yFinal = (  MARGIN + offset + tile.width * index, 
                                HEIGHT - 2.2*tile.height - MARGIN)
            tile.slideTile(screen, xFinal, yFinal)
            
            tile.update()
            tile.draw(screen)
            index += 1

def displayDead(deadTiles, screen):
    # where to start drawing dead tiles
    deadX, deadY = (WIDTH - MARGIN - rowLength + MARGIN, 
                    HEIGHT - stacksPerSide * tileWidth)

    for i in range(len(deadTiles)):
        tile = deadTiles[i]
        xFinal, yFinal = (  deadX + (i % tilesPerRow) * tileWidth, 
                            deadY + (i // tilesPerRow) * tileHeight)
        tile.slideTile(screen, xFinal, yFinal)
        
        tile.update()
        tile.draw(screen)

def displayTossed(tile, deadTiles, screen):
    deadX, deadY = (WIDTH - MARGIN - rowLength + MARGIN, 
                    HEIGHT - stacksPerSide * tileWidth)
    xFinal, yFinal = (  deadX + (len(deadTiles) % tilesPerRow) * tileWidth + 10, 
                        deadY + (len(deadTiles) // tilesPerRow) * tileHeight + 10)
    tile.slideTile(screen, xFinal, yFinal)

    tile.update()
    tile.draw(screen)

def displayOtherHands(players, activePlayer, screen):
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
                tile.slideTile(screen, xFinal, yFinal)

                tile.update()
                tile.draw(screen)
            elif playerNum == 2:
                xFinal, yFinal = (  WIDTH - MARGIN - i * tileWidth - tileWidth, 
                                    MARGIN)
                tile.slideTile(screen, xFinal, yFinal)

                tile.update()
                tile.draw(screen)
            elif playerNum == 3:
                xFinal, yFinal = (  MARGIN, 
                                    MARGIN + i * tileWidth)
                tile.slideTile(screen, xFinal, yFinal)

                tile.update()
                tile.draw(screen)

def displayOtherRevealed(players, activePlayer, screen):
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
                    tile.slideTile(screen, xFinal, yFinal)

                    tile.update()
                    tile.draw(screen)
                elif playerNum == 2:
                    xFinal, yFinal = (  WIDTH - MARGIN - tileIndex * tileWidth - tileWidth - offset, 
                                        MARGIN + 2 * tileDepth)
                    tile.slideTile(screen, xFinal, yFinal)

                    tile.update()
                    tile.draw(screen)
                elif playerNum == 3:
                    xFinal, yFinal = (  MARGIN + 2 * tileDepth, 
                                        MARGIN + tileIndex * tileWidth + offset)
                    tile.slideTile(screen, xFinal, yFinal)

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
    # referenced https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
    font = pygame.font.Font(None, 32)
    headerFont = pygame.font.Font(None, 82)
    prompt = 'please enter your name:'
    header = 'ITS MAHJTIME!!!!!'
    inputW, inputH = 140, 32
    inputBox = pygame.Rect( (WIDTH - inputW)/2, (HEIGHT - inputH)/2, 
                            inputW, inputH)
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
                    if inputBox.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    # change the color of the input box.
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
        headerSurface = headerFont.render(header, True, color)
        # Resize the box if the text is too long.
        width = max(200, txtSurface.get_width()+10)
        inputBox.w = width
        # Blit the text.
        centerX = 3 * (headerSurface.get_rect(center = screen.get_rect().center).x) // 4
        centerY = headerSurface.get_rect(center = screen.get_rect().center).y - 4 * MARGIN
        screen.blit(promptSurface, (inputBox.x, inputBox.y - 32))
        screen.blit(txtSurface, (inputBox.x + 5, inputBox.y + 5))
        screen.blit(headerSurface, (centerX + 10, centerY))
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
        pygame.display.update()

    return rects, booleans

def getAction(rects, booleans, screen):
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
    displayButtons(None, None, None, screen)

def displaySidebar(screen, text=''):
    # sideBar = pygame.Rect(WIDTH, 0, SIDEBAR, HEIGHT)
    # pygame.draw.rect(screen, WHITE, sideBar)
    chatBox(text, screen)
    pygame.display.update()

def displayEndGame(players, turn, screen):
    for player in players:
        if player.won:
            winner = player

    for tile in winner.hand:
        tile.location = 'hu'
        tile.update()
        tile.draw(screen)
    
    # whoever tossed out winning card is loser, unless winner drew card
    # not using loser rn, might impliment betting / drinking  
    losers = [ players[turn] ]
    if losers[0] is winner:
        losers = [  players[(turn + 1) % 4], 
                    players[(turn + 2) % 4], 
                    players[(turn + 3) % 4] ]
    
    messageBox = pygame.Rect(WIDTH/4, HEIGHT/4, WIDTH/2, HEIGHT/2)
    pygame.draw.rect(screen, PINK, messageBox)
    winFont = pygame.font.Font(None, 54)
    buttonFont = pygame.font.Font(None, 24)
    winMsg = f'{winner.name} won!!!'
    playMsg = 'PLAY AGAIN?'
    quitMsg = 'QUIT'
    buttonWidth = 7*MARGIN
    buttonHeight = 3*MARGIN
    playButtonRect = pygame.Rect(   (WIDTH - buttonWidth)/3, 3*(HEIGHT - buttonHeight)/5 - MARGIN, 
                                    buttonWidth, buttonHeight)
    quitButtonRect = pygame.Rect(   2*(WIDTH - buttonWidth)/3, 3*(HEIGHT - buttonHeight)/5 - MARGIN, 
                                    buttonWidth, buttonHeight)

    winText = winFont.render(winMsg, True, BLACK)
    playText = buttonFont.render(playMsg, True, BLACK)
    quitText = buttonFont.render(quitMsg, True, BLACK)
    centerX = 3 * (winText.get_rect(center = screen.get_rect().center).x) // 4
    centerY = winText.get_rect(center = screen.get_rect().center).y - 4 * MARGIN
    screen.blit(winText, (centerX, centerY))
    pygame.draw.rect(screen, MINT, playButtonRect, 0, buttonHeight//2)
    pygame.draw.rect(screen, MINT, quitButtonRect, 0, buttonHeight//2)
    screen.blit(playText, (playButtonRect.x + 12, playButtonRect.y + 23))
    screen.blit(quitText, (quitButtonRect.x + 45, quitButtonRect.y + 23))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButtonRect.collidepoint(event.pos):
                    return True
                elif quitButtonRect.collidepoint(event.pos):
                    return False