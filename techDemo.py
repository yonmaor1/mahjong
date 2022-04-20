import pygame, socket, sys
from pygame.locals import *
from mahjong import *


# game inits
deck = getDeck()
hand = sortHand(getHand(deck))
revealed = [ [(1, 'number'), (1, 'number'), (1, 'number')], [(1, 'stick'), (2, 'stick'), (3, 'stick')], [(1, 'circle'), (2, 'circle'), (3, 'circle')] ]
yon = Player('yon', 0, False)
yon.hand = hand
yon.revealed = revealed
print(sortHand(yon.hand))


pygame.init()

FPS = pygame.time.Clock()

WHITE = (255,255,255)

# screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

running = True

# get input
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


class Tile:
    def __init__(self, value, suit, index):
        self.value = value
        self.suit = suit
        self.index = index

        if self.suit is None:
            self.imgRef = f'img/{self.value}.jpg'
        else:
            self.imgRef = f'img/{self.value}{self.suit}.jpg'
        self.image = pygame.image.load(self.imgRef)
        self.scaleFactor = 44/36 # height to width ratio
        self.width = 45
        self.size = self.width, self.width * self.scaleFactor
        self.width, self.height = self.size
        self.image = pygame.transform.scale(self.image, self.size)

    def update(self):
        pressedKeys = pygame.key.get_pressed()
        for i in range(9):
            # pygame.K_1 == 49
            if pressedKeys[i+49]:
                # print(i)
                self.value = i + 1

        if pressedKeys[K_c]:
            self.suit = 'circle'
        if pressedKeys[K_s]:
            self.suit = 'stick'
        if pressedKeys[K_n]:
            self.suit = 'num'

        if self.suit is None:
            self.imgRef = f'img/{self.value}.jpg'
        else:
            self.imgRef = f'img/{self.value}{self.suit}.jpg'
        self.image = pygame.image.load(self.imgRef)
        self.image = pygame.transform.scale(self.image, self.size)


def displayHand(hand, screen):
    for i in range(len(hand)):
        tile = Tile(hand[i][0], hand[i][1], i)
        tile.drawInHand(screen)

def displayRevealed(revealed, screen):
    # offset to add space between sets
    offset = 0
    index = 0
    for set in revealed:
        for i in range(len(set)):
            tile = Tile(set[i][0], set[i][1], i)
            pygame.transform.scale(tile.image, tile.size)
            margin = (WIDTH - tile.width * 16) / 2
            screen.blit(tile.image, (  margin + offset + tile.width * index, 
                                    HEIGHT - 2.2*tile.height - margin))
            index += 1
        offset += 10

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
                    gettingName = False
                    print(text)
                    activeName = text
                    text = ''
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

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displayHand(hand, screen)
    displayRevealed(revealed, screen)

    pygame.display.update()
    FPS.tick(30)