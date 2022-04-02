import random

class Player:
    def __init__(self, name, isAI):
        self.name = name
        self.isAI = isAI
        self.isPlaying = False
        self.isDealer = False
        self.hand = []
        self.revealed = []
        self.won = False

    def canPong(self, tile):
        if self.hand.count(tile) >= 2:
            return True
        return False

    def pong(self, tile):
        self.revealed += [tile, tile, tile]
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)

    def canKong(self, tile):
        if self.hand.count(tile) == 3:
            return True
        return False
    
    def kong(self, tile):
        self.revealed += [tile, tile, tile, tile]
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)

    def canChi(self, tile):
        value, suit = tile
        if (((value - 1, suit) and (value - 2, suit)) in self.hand or 
            ((value + 1, suit) and (value + 2, suit)) in self.hand or
            ((value - 1, suit) and (value + 1, suit)) in self.hand):
            return True
        
        return False

    def chi(self, tossedTile, handTile1, handTile2):
        self.revealed += [tossedTile, handTile1, handTile2]
        self.hand.remove(tossedTile)
        self.hand.remove(handTile1)
        self.hand.remove(handTile2)

    def hu(self, tile):
        ...

    def drawTile(self, deck):
        newTile = random.choice(deck)
        self.hand.append(newTile)
        deck.remove(newTile)

        print(f'Drawn Tile: {newTile}', end='')
        print(f'Hand: {self.hand}')

    def tossTile(self):
        tileToToss = input('What do you want to toss?')
        while tileToToss not in self.hand:
            print(f'{tileToToss} is not in your hand', end = '')
            tileToToss = input('What do you want to toss?')

        self.hand.remove(tileToToss)
        return tileToToss

    
def getHand(deck):
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
