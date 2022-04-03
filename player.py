import random

class Player:
    def __init__(self, name, num, isAI):
        self.name = name
        self.num = num
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
        self.revealed.append([tile, tile, tile])
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)

    def canKong(self, tile):
        if self.hand.count(tile) == 3:
            return True
        return False
    
    def kong(self, tile):
        self.revealed.append([tile, tile, tile, tile])
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

    def chi(self, tossedTile):
        otherTiles = input('Please enter comma seperated indecies of the tiles you would like to chi')
        otherTiles = otherTiles.split(',')
        index1 = int(otherTiles[0])
        index2 = int(otherTiles[1])

        chiTile1 = self.hand[index1]
        chiTile2 = self.hand[index2]

        self.revealed.append([tossedTile, chiTile1, chiTile2])
        self.hand.remove(tossedTile)
        self.hand.remove(chiTile1)
        self.hand.remove(chiTile2)

    @staticmethod
    def isSet(tiles):
        # takes a set of 3 tiles and returns True if they form a set        
        if tiles[0] == tiles[1] == tiles[2]:
            return True

        # check is same suite
        elif tiles[0][1] == tiles[1][1] == tiles[2][1]:
            # check if values directly follow one another
            values = [tiles[0][0], tiles[1][0], tiles[2][0]]
            values.sort()
            if (values[0] + 1 == values[1]) and (values[1] + 1 == values[2]):
                return True
        
        return False
    
    def canHu(self, tile):
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

def giveHands(players, deck):
    players[0].hand = getHand(deck)
    players[1].hand = getHand(deck)
    players[2].hand = getHand(deck)
    players[3].hand = getHand(deck)