import pygame, socket, sys
from pygame.locals import *

pygame.init()

FPS = pygame.time.Clock()

WHITE = (255,255,255)

# screen
screen = pygame.display.set_mode((400,400))
screen.fill(WHITE)

running = True

class Tile:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

        self.imgRef = f'img/{value}{suit}.jpg'
        self.image = pygame.image.load(self.imgRef)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

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

        
        self.imgRef = f'img/{self.value}{self.suit}.jpg'
        self.image = pygame.image.load(self.imgRef)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def draw(self, surface):
        pygame.transform.scale(self.image, (100, 100))
        surface.blit(self.image, (200,200))

tile = Tile(2, 'circle')

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    tile.update()

    screen.fill(WHITE)

    tile.draw(screen)

    pygame.display.update()
    FPS.tick(30)