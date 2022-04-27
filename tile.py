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
        self.oldSize = self.size = self.width, self.height
        self.width, self.height = self.size
        self.depth = tileDepth
        self.image = pygame.transform.scale(self.image, self.size)
        
        self.x, self.y = 0, 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.theta = 0

    def __repr__(self):
        return f'({self.value}, {self.suit})'

    def __add__(self, x):
        if isinstance(x, int) and self.suit != None and (self.value + x) <= 9:
            return Tile(self.value + x, self.suit)
        elif not isinstance(x, int):
            print(f'{x} not an int')
        elif self.suit is None:
            print('tile arithmatic not supported for winds / dragons')
        elif (self.value + x) > 9:
            print('value out of range')
            return Tile(self.value + x, self.suit)

    def __sub__(self, x):
        if isinstance(x, int) and self.suit != None and (self.value - x) >= 1:
            return Tile(self.value - x, self.suit)
        elif not isinstance(x, int):
            print(f'{x} not an int')
        elif self.suit is None:
            print('tile arithmatic not supported for winds / dragons')
        elif (self.value - x) < 1:
            print(f'value out of range')
            return Tile(self.value - x, self.suit)

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        if not isinstance(other, Tile) or self.suit != other.suit:
            return False
        
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, Tile) or self.suit != other.suit:
            return False
        
        return self.value > other.value

    def __le__(self, other):
        if not isinstance(other, Tile) or self.suit != other.suit:
            return False
        
        return self.value <= other.value

    def __ge__(self, other):
        if not isinstance(other, Tile) or self.suit != other.suit:
            return False
        
        return self.value >= other.value

    def __int__(self):
        return self.value

    def tup(self):
        return (self.value, self)

    def update(self):
        if self.location == 'passiveHand':
            self.imgRef = 'img/topView.PNG'
            self.rect = pygame.Rect(self.x, self.y, tileWidth, tileDepth)
            self.width, self.height = tileWidth, tileDepth
            self.size = tileWidth, tileDepth
        else:
            # if tile not in passive hand
            self.rect = pygame.Rect(self.x, self.y, tileWidth, tileHeight)
            self.width, self.height = tileWidth, tileHeight
            self.size = tileWidth, tileHeight
    
            if self.location == 'deck':
                # display blank tile if in deck
                self.imgRef = 'img/blank.PNG'
            elif self.suit is None:
                self.imgRef = f'img/{self.value}.PNG'
            else:
                self.imgRef = f'img/{self.value}{self.suit}.PNG'

        if self.location == 'tossed':
            # always orient upright once tossed
            self.theta = 0
        
        self.image = pygame.image.load(self.imgRef)
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.theta)
    
    def draw(self, surface):
        # pygame.transform.scale(self.image, self.size)
        # pygame.transform.rotate(self.image, self.theta)
        surface.blit(self.image, (self.x,self.y))

    
    def drawInHand(self, surface):
        pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, (  MARGIN + self.width * self.index, 
                                    HEIGHT - self.height - MARGIN))

    def drawInRevealed(self, surface):
        pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, (  MARGIN + self.width * self.index, 
                                    HEIGHT - 2.2*self.height - MARGIN))

    def slideTile(self, screen, x1, y1, xStep = 5):
        screenshot = pygame.image.save(screen, "img/firstFrame.jpg")
        x0, y0 = self.x, self.y
        if (x0, y0) == (0,0) or (x0, y0) == (x1, y1):
           # don't slide when initializing game
            self.x, self.y = x1, y1

            return 

        try:
            xSteps = int(abs(x1 - x0) // xStep)
            yStep = abs(y1 - y0) / xSteps
            xPositions = frange(x0, x1, xStep)
            yPositions = frange(y0, y1, yStep)
            for i in range(xSteps + 1):
                if i > 0:
                    # erase last drawing
                    self.size = self.width, self.height
                    prevImg = pygame.image.load('img/green.png')
                    prevImg = pygame.transform.scale(prevImg, self.oldSize)
                    prevImg = pygame.transform.rotate(prevImg, self.theta)
                    firstFrame = pygame.image.load('img/firstFrame.jpg')
                    screen.blit(firstFrame, (0, 0))
                    screen.blit(prevImg, (xPositions[0], yPositions[0]))

                xPos = xPositions[i]
                yPos = yPositions[i]
                self.x, self.y = xPos, yPos
                self.update()
                self.draw(screen)
                pygame.display.update()

        except Exception as e:
            print(e)
            self.x, self.y = x1, y1
            self.update()
            self.draw(screen)
            pygame.display.update()
            return 


