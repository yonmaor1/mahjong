from pygame.locals import *
from globals import *

# class to draw tile
class Tile:
    def __init__(self, value, suit, location = None, index = None):
        self.value = value
        self.suit = suit
        self.location = location
        self.index = index

        if type(value) == int:
            if value < 1 or value > 9:
            # this fixes a bug in canChi, where the program crashed when it
            # tries to find a Tile smaller then 1 or greater then 9 
                return

        if self.location == 'deck':
            self.imgRef = 'img/blank.PNG'
        elif self.suit is None:
            self.imgRef = f'img/{self.value}.PNG'
        else:
            self.imgRef = f'img/{self.value}{self.suit}.PNG'
        
        self.image = pygame.image.load(self.imgRef)
        self.scaleFactor = tileRatio # height to width ratio
        self.width = tileWidth
        self.height = tileHeight
        self.size = self.width, self.height
        self.width, self.height = self.size
        self.depth = tileDepth
        self.image = pygame.transform.scale(self.image, self.size)
        
        self.x, self.y = 0, 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.theta = 0

    def __repr__(self):
        return f'({self.value}, {self.suit})'

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.value == other.value and self.suit == other.suit

    def tup(self):
        return (self.value, self)

    def update(self):

        if self.location == 'passiveHand':
            self.imgRef = 'img/topView.PNG'
            self.rect = pygame.Rect(self.x, self.y, self.width, self.depth)
            self.size = self.width, self.depth
        elif self.location != 'passiveHand':
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.size = self.width, self.height
        
        if self.location != 'passiveHand':
            if self.location == 'deck' or self.suit == 'flower':
                self.imgRef = 'img/blank.PNG'
            elif self.suit is None:
                self.imgRef = f'img/{self.value}.PNG'
            else:
                self.imgRef = f'img/{self.value}{self.suit}.PNG'

        if self.location == 'tossed':
            self.theta = 0
        
        self.image = pygame.image.load(self.imgRef)
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.theta)
    
    def draw(self, surface):
        pygame.transform.scale(self.image, self.size)
        pygame.transform.rotate(self.image, self.theta)
        surface.blit(self.image, (self.x,self.y))

    
    def drawInHand(self, surface):
        pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, (  MARGIN + self.width * self.index, 
                                    HEIGHT - self.height - MARGIN))

    def drawInRevealed(self, surface):
        pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, (  MARGIN + self.width * self.index, 
                                    HEIGHT - 2.2*self.height - MARGIN))

