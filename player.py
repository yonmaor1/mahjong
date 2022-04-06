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
        # needs two (or three) additional copies of the tossed
        # tile in hand 
        if self.hand.count(tile) >= 2:
            return True
        return False

    def pong(self, tile):
        # revels pong and removes tiles from hand
        self.revealed.append([tile, tile, tile])
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)

    def canKong(self, tile):
        # returns True of player has 3 additional copies of the tossed tile in
        # their hand 
        if self.hand.count(tile) == 3:
            return True
        return False
    
    def kong(self, tile):
        # revelas the Kong and removes tiles from hand
        # tile is drawn in playerTurn 
        self.revealed.append([tile, tile, tile, tile])
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)

    def canChi(self, tile):
        # returns True of player has 3 consequtive tiles given the tossedTile
        
        value, suit = tile[0], tile[1]

        # can only Chi with suit tiles
        if suit is None:
            return False
        
        if (((value - 1, suit) and (value - 2, suit)) in self.hand or 
            ((value + 1, suit) and (value + 2, suit)) in self.hand or
            ((value - 1, suit) and (value + 1, suit)) in self.hand):
            return True
        
        return False

    @staticmethod
    def isChi(tiles):
        # takes a [list] of 3 tiles, and returns True if they are consequtive
        # tiles of the same suit 
        values = [ tiles[0][0], tiles[1][0], tiles[2][0] ]
        values.sort()
        suits = [ tiles[0][1], tiles[1][1], tiles[2][1] ]
        
        if ((suits[0] == suits[1] == suits[2]) and 
            (values[0] + 1 == values[1]) and 
            (values[1] + 1 == values[2])):
            return True
        
        return False

    @staticmethod
    def isConsecutive(tiles):
        # takes a [list] of tiles and returns True if they are all consequtive
        # and share the same suit 
        for i in range(len(tiles) - 1):
            if (tiles[i][0] + 1 != tiles[i+1][0] and 
                tiles[i][1] != tiles[i+1][1]):
                return False

        return True

    @staticmethod
    def isPong(tiles):
        # takes a [list] of tiles and returns True if the list contains 3 
        # identical tiles
        if tiles[0] == tiles[1] == tiles[2]:
            return True

        return False

    @staticmethod
    def isSet(tiles):
        # takes a set of 3 tiles and returns True if they form a set        
        if Player.isPong(tiles) or Player.isChi(tiles):
            return True
        
        return False

    def getChiTiles(self, tossedTile, tiles):
        # destructivly modifies [list] tiles to contain the tiles
        # selected by the player 
        otherTiles = input('''Please enter comma seperated indecies of the 
                            tiles you would like to chi''')
        otherTiles = otherTiles.split(',')
        index1 = int(otherTiles[0])
        index2 = int(otherTiles[1])

        chiTile1 = self.hand[index1]
        chiTile2 = self.hand[index2]

        tiles = [ tossedTile, chiTile1, chiTile2 ]
        return tiles

    def getChiTilesAI(self, tossedTile):
        # destructivly modifies [list] tiles to contain the tiles
        # selected by mahjbot
        value, suit = tossedTile[0], tossedTile[1]
        tiles = []

        if (value + 1, suit) and (value + 2, suit) in self.hand:
            tiles = [ tossedTile, (value + 1, suit), (value + 2, suit) ]
        elif (value - 1, suit) and (value - 2, suit) in self.hand:
            tiles = [ tossedTile, (value - 1, suit), (value - 2, suit) ]
        elif (value - 1, suit) and (value + 1, suit) in self.hand:
            tiles = [ tossedTile, (value - 1, suit), (value + 1, suit) ]
    
        return tiles

    def chi(self, tossedTile):
        # gets selected tiles, revels them and removes them from hand
        tiles = []

        if self.isAI:
            tiles = self.getChiTilesAI(tossedTile)
        
        else:
            tiles = self.getChiTiles(tossedTile, tiles)

            while not ( Player.isChi(tiles) ):
                print('These tiles dont form a set', end='')
                
                tiles = self.getChiTiles(tossedTile, tiles)

        self.revealed.append(tiles)
        self.hand.remove(tiles[0])
        self.hand.remove(tiles[1])
        self.hand.remove(tiles[2])
    
    def canHu(self, tile, sets = []):
        # checks if player can Hu (win the game)
        if len(sets) == len(self.hand):
            return True

        else:
            for tile in self.hand:
                ...
    
    def hu(self, tile):
        ...

    def drawTile(self, deck):
        # take a random tile from the deck, adds to to player's hand
        # then remove it from the deck
        newTile = random.choice(deck)
        self.hand.append(newTile)
        deck.remove(newTile)

        print(f'Drawn Tile: {newTile}', end='')
        print(f'Hand: {self.hand}')

    def tossTile(self):
        # tosses a selected tile from player's hand
        tileToToss = input('What do you want to toss? Please input an index')
        
        return self.hand.pop(tileToToss)

    def tossTileAI(self):
        # tosses a tile from AI player's hand
        tileToToss = None

        for tile in self.hand:
            # first check for a tile not in a pair
            value, suit = tile[0], tile[1]
            if (self.hand.count(tile) >= 1):
                continue
            elif (value + 1, suit) or (value - 1, suit) in self.hand:
                continue
            elif (value + 2, suit) or (value - 2, suit) in self.hand:
                continue
            tileToToss = tile

        if tileToToss is None:
            # if all tiles are in pairs check for tiles not in sets
            for tile in self.hand:
                if self.canPong(tile) or self.canChi(tile):
                    continue
                tileToToss = tile

        if tileToToss is None:
            # if all tiles are in sets pick a random tile
            tileToToss = random.choice(self.hand)

        return self.hand.pop(tileToToss)

# should this be in mahjong.py?
def giveHands(players, deck):
    # initializes players with hands
    players[0].hand = getHand(deck)
    players[1].hand = getHand(deck)
    players[2].hand = getHand(deck)
    players[3].hand = getHand(deck)

def getHand(deck):
    # draws 16 random cards from the deck, then removes them from the deck
    hand = []
    while len(hand) < 16:
        newTile = random.choice(deck)
        hand.append(newTile)
        deck.remove(newTile)

    return hand

def sortHand(hand):
    # sorts hand by suite (not by value)
    nonSuits = []
    nums = []
    dots = []
    sticks = []

    for tile in hand:
        if tile[1] == None:
            nonSuits.append(tile)
        elif tile[1] == 'number':
            nums.append(tile)
        elif tile[1] == 'dot':
            dots.append(tile)
        elif tile[1] == 'stick':
            sticks.append(tile)

    hand = nonSuits + nums + dots + sticks
    return hand