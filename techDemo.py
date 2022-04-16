import pygame, socket, sys
from pygame.locals import *
from mahjong import *

deck = getDeck()
hand = sortHand(getHand(deck))
yon = Player('yon', 0, False)
yon.hand = hand
print(sortHand(yon.hand))


pygame.init()

FPS = pygame.time.Clock()

WHITE = (255,255,255)

# screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

running = True

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

    def draw(self, surface):
        pygame.transform.scale(self.image, self.size)
        margin = (WIDTH - self.width * 16) / 2
        surface.blit(self.image, (  margin + self.width * self.index, 
                                    HEIGHT - self.height - margin))

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # tile.update()

    screen.fill(WHITE)
    for i in range(len(hand)):
        tile = Tile(hand[i][0], hand[i][1], i)
        tile.draw(screen)

    pygame.display.update()
    FPS.tick(30)