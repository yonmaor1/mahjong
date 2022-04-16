from mahjong import *

pygame.init()

FPS = pygame.time.Clock()

WHITE = (255,255,255)

# screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

running = True

# class to draw tiles
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


def runGame():
    players = initPlayers()
    # BUG: active player will change after a round ends
    activePlayer = players[0]
    screen.fill(WHITE)
    for i in range(len(activePlayer.hand)):
        # draw activePlayer's hand
        tile = Tile(activePlayer.hand[i][0], activePlayer.hand[i][1], i)
        tile.draw(screen)
    
    deck, tossedTile, deadTiles, turn, dealer = firstTurn(players)
    while True:
        (deck, tossedTile, deadTiles, turn, dealer) = playRound(players,
                                                                deck, 
                                                                tossedTile, 
                                                                deadTiles, 
                                                                turn, 
                                                                dealer)
        
        for i in range(len(activePlayer.hand)):
            # draw activePlayer's hand
            tile = Tile(activePlayer.hand[i][0], activePlayer.hand[i][1], i)
            tile.draw(screen)

runGame()