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
        suits = [ tiles[0][1], tiles[1][1], tiles[2][1] ]
        if (suits[0] == None or
            suits[1] == None or
            suits[2] == None):
            # can only Chi suit cards
            return False

        values = [ tiles[0][0], tiles[1][0], tiles[2][0] ]
        values.sort()
        
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
        # takes a list of 3 tiles and returns True if they form a set        
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
        # one of the tiles isn't in hand because it's the tossed tile
        if tiles[0] in self.hand:
            self.hand.remove(tiles[0])
        if tiles[1] in self.hand:
            self.hand.remove(tiles[1])
        if tiles[2] in self.hand:
            self.hand.remove(tiles[2])

    def findPairs(self, currentHand):
        # returns a list containing every pair in players hand
        pairs = []
        for tile in currentHand:
            if currentHand.count(tile) >= 2:
                pairs.append([tile, tile])

        return pairs

    @ staticmethod
    def canHuGivenPair(currentHand, sets = []):
        # takes a hand, excluding a pair, and returns true of the hand can be
        # arranged entirely into sets of 3 (backtracking)
        
        if len(currentHand) == 0:
                return True

        else:
            # check every triple
            for i in range(len(currentHand) - 2):
                for j in range(i+1, len(currentHand) - 1):
                    for k in range(j+1, len(currentHand)):
                        tiles = [   currentHand[i], 
                                    currentHand[j], 
                                    currentHand[k] ]
                        if Player.isSet(tiles):
                            sets += tiles
                            for tile in tiles:
                                currentHand.remove(tile)
                            solution = Player.canHuGivenPair(currentHand, sets)
                            if solution:
                                return solution
                            else:
                                # undo
                                currentHand += tiles
                                for tile in tiles:
                                    sets.remove(tile)
            return False
                                
    def canHu(self, tossedTile):
        # checks if player can Hu (win the game)
        currentHand = self.hand + [tossedTile]
        pairs = self.findPairs(currentHand)
        for pair in pairs:
            # checks if player can Hu, given every possible pair
            for tile in pair:
                currentHand.remove(tile)
            if not Player.canHuGivenPair(currentHand):
                currentHand += pair
            else:
                return True
        return False

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
        
        return self.hand.pop(int(tileToToss))

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

        self.hand.remove(tileToToss)

        return tileToToss

# should this be in mahjong.py?
def giveHands(players, deck):
    # initializes players with hands
    players[0].hand = sortHand(getHand(deck))
    players[1].hand = sortHand(getHand(deck))
    players[2].hand = sortHand(getHand(deck))
    players[3].hand = sortHand(getHand(deck))

def getHand(deck):
    # draws 16 random cards from the deck, then removes them from the deck
    hand = []
    while len(hand) < 16:
        newTile = random.choice(deck)
        hand.append(newTile)
        deck.remove(newTile)

    return hand

def tupleSort(hand):
    # modified merge sort from https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#mergesort
    def merge(A, B):
        if ((len(A) == 0) or (len(B) == 0)):
            return A+B
        else:
            if (A[0][0] < B[0][0]):
                return [A[0]] + merge(A[1:], B)
            else:
                return [B[0]] + merge(A, B[1:])
    
    if (len(hand) < 2):
        return hand
    else:
        mid = len(hand)//2
        left = tupleSort(hand[:mid])
        right = tupleSort(hand[mid:])
        return merge(left, right)

def nonSuitSort(hand):
    sortedHand = []
    for tile in hand:
        if not tile in sortedHand:
            sortedHand += [tile for i in range(hand.count(tile))]
        
    return sortedHand


def sortHand(hand):
    # sorts hand by suite (not by value)
    nonSuits = []
    nums = []
    circles = []
    sticks = []

    for tile in hand:
        if tile[1] == None:
            nonSuits.append(tile)
        elif tile[1] == 'number':
            nums.append(tile)
        elif tile[1] == 'circle':
            circles.append(tile)
        elif tile[1] == 'stick':
            sticks.append(tile)

    nonSuits = nonSuitSort(nonSuits)
    nums = tupleSort(nums)
    circles = tupleSort(circles)
    sticks = tupleSort(sticks)


    sortedHand = nonSuits + nums + circles + sticks
    return sortedHand