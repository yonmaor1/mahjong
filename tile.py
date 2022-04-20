from pygame.locals import *
import pygame, sys, random
WIDTH, HEIGHT = 800, 800

# class to draw tiles
class Tile:
    def __init__(self, value, suit, location, index):
        self.value = value
        self.suit = suit
        self.location = location
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

        # location
        '''margin = (WIDTH - self.width * 16) / 2
        if self.location == 'hand':
            self.x, self.y = (  margin + self.width * self.index, 
                                HEIGHT - self.height - margin)
        elif self.location == 'revealed':
            # offset to space out each set
            offset = 10 * (index // 3)
            self.x, self.y = (  margin + offset + self.width * index, 
                                HEIGHT - 2.2*self.height - margin)
        else:
            self.x, self.y = (0, 0)'''
        
        self.x, self.y = 0, 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def __repr__(self):
        return f'({self.value}, {self.suit})'

    def tup(self):
        return (self.value, self)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load(self.imgRef)
        self.image = pygame.transform.scale(self.image, self.size)
    
    def draw(self, surface):
        pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, (self.x,self.y))

    
    def drawInHand(self, surface):
        pygame.transform.scale(self.image, self.size)
        margin = (WIDTH - self.width * 16) / 2
        surface.blit(self.image, (  margin + self.width * self.index, 
                                    HEIGHT - self.height - margin))

    def drawInRevealed(self, surface):
        pygame.transform.scale(self.image, self.size)
        margin = (WIDTH - self.width * 16) / 2
        surface.blit(self.image, (  margin + self.width * self.index, 
                                    HEIGHT - 2.2*self.height - margin))

