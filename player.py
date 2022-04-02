import random

class Player:
    def __init__(self, name, isAI):
        self.name = name
        self.isAI = isAI
        self.isPlaying = False
        self.isDealer = False
        self.hand = []
        self.revealed = []

    def pong(self, tile):
        ...

    def kong(self, tile):
        ...

    def chi(self, tile):
        ...

    def hu(self, tile):
        ...

    def drawTile(self, deck):
        newTile = random.choice(deck)
        self.hand.append(newTile)
        deck.remove(newTile)

        print(f'Drawn Tile: {newTile}', end='')
        print(f'Hand: {self.hand}')

    def tossTile(self):
        ...

    
def getHand(deck):
    indecies = []
    hand = []
    while len(hand) < 16:
        newTile = random.choice(deck)
        hand.append(newTile)
        deck.remove(newTile)

    return hand

def giveHands(player1, player2, player3, player4, deck):
    player1.hand = getHand(deck)
    player2.hand = getHand(deck)
    player3.hand = getHand(deck)
    player4.hand = getHand(deck)
