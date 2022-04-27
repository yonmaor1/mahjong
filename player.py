from pygame.locals import *
from tile import *
from globals import *

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
        else:
            return False

    def pong(self, tossedTile):
        # revels pong and removes tiles from hand
        print(f'{self.name} will pong')
        pong = [tossedTile]
        while len(pong) < 3:
            index = self.hand.index(tossedTile)
            pongTile = self.hand.pop(index)
            pong.append(pongTile)
        
        self.revealed.append(pong)
        for tile in pong:
            tile.location = 'revealed'
            tile.update()
            if tile in self.hand:
                self.hand.remove(tile)

    def canKong(self, tile):
        # returns True of player has 3 additional copies of the tossed tile in
        # their hand 
        if self.hand.count(tile) == 3:
            return True
        else:
            return False
    
    def kong(self, tossedTile):
        # revelas the Kong and removes tiles from hand
        # tile is drawn in playerTurn 
        print(f'{self.name} will kong')
        kong = [tossedTile]
        while len(kong) < 4:
            index = self.hand.index(tossedTile)
            pongTile = self.hand.pop(index)
            kong.append(pongTile)
        
        self.revealed.append(kong)
        for tile in kong:
            tile.location = 'revealed'
            tile.update()
            if tile in self.hand:
                self.hand.remove(tile)

    def canChi(self, tile):
        # returns True of player has 3 consequtive tiles given the tossedTile
        
        value, suit = tile.value, tile.suit

        # can only Chi with suit tiles
        if suit is None:
            return False
        
        if (tile - 1  in self.hand and tile - 2 in self.hand):
            print(f'{tile - 1}, {tile - 2}')
            return True
        elif (tile + 1  in self.hand and tile + 2 in self.hand):
            print(f'{tile + 1}, {tile + 2}')
            return True
        elif (tile - 1  in self.hand and tile + 1 in self.hand):
            print(f'{tile - 1}, {tile + 1}')
            return True
        
        return False

    @staticmethod
    def isChi(tiles):
        # takes a [list] of 3 tiles, and returns True if they are consequtive
        # tiles of the same suit 
        if None in tiles:
            print('Nonetype found in chi')
            return False

        suits = [ tile.suit for tile in tiles ]
        if (None in suits):
            # can only Chi suit cards
            return False

        values = [ tile.value for tile in tiles ]
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
            if (tiles[i].value + 1 != tiles[i+1].value and 
                tiles[i].value != tiles[i+1].value):
                return False

        return True

    @staticmethod
    def isPong(tiles):
        # takes a [list] of tiles and returns True if the list contains 3 
        # identical tiles
        if repr(tiles[0]) == repr(tiles[1]) == repr(tiles[2]):
            return True

        return False

    @staticmethod
    def isSet(tiles):
        # takes a list of 3 tiles and returns True if they form a set        
        if Player.isPong(tiles) or Player.isChi(tiles):
            return True
        
        return False

    # this function is not used, AI chooses tiles for player
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
        chi = [tossedTile]
        # the for loops here are to allow for tile sliding, by ensuring the
        # tiles the player chis are the actual tile ojects in their hand rather
        # then creating new tile instances 
        if tossedTile + 1 in self.hand and tossedTile + 2 in self.hand:
            for tile in self.hand:
                if (tile == tossedTile + 1 or tile == tossedTile + 2):
                    if tile not in chi:
                        chi.append(tile)
                if len(chi) == 3:
                    break
        elif tossedTile - 1  in self.hand and tossedTile - 2 in self.hand:
            for tile in self.hand:
                if (tile == tossedTile - 1 or tile == tossedTile - 2):
                    if tile not in chi:
                        chi.append(tile)
                if len(chi) == 3:
                    break
        elif tossedTile - 1 in self.hand and tossedTile + 1 in self.hand:
            for tile in self.hand:
                if (tile == tossedTile - 1 or tile == tossedTile + 1):
                    if tile not in chi:
                        chi.append(tile)
                if len(chi) == 3:
                    break

        print(sorted(chi))
    
        return sorted(chi)

    def chi(self, tossedTile):
        # gets selected tiles, revels them and removes them from hand
        print(f'{self.name} will chi')

        chi = self.getChiTilesAI(tossedTile)

        self.revealed.append(chi)
        for tile in chi:
            tile.location = 'revealed'
            tile.update()
            if tile != tossedTile:
                self.hand.remove(tile)

    def findPairs(self, currentHand):
        # returns a list containing every pair in players hand
        pairs = []
        for i in range(len(currentHand)-1):
            tile1 = currentHand[i]
            for j in range(i + 1, len(currentHand)):
                tile2 = currentHand[j]
                if tile1 == tile2:
                    pairs.append([tile1, tile2])

        pairsNoRepeats = []
        for pair in pairs:
            if pair not in pairsNoRepeats:
                pairsNoRepeats.append(pair)
            
        return pairsNoRepeats

    @staticmethod
    def canHuGivenPair(currentHand, sets = []):
        # takes a hand, excluding a pair, and returns true of the hand can be
        # arranged entirely into sets of 3 (backtracking!!!)
        
        if len(currentHand) == 0:
                return sets

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
                            if solution != False:
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

        if len(currentHand) == 2:
            if currentHand[0] == currentHand[1]:
                return True

        for pair in pairs:
            # checks if player can Hu, given every possible pair
            for tile in pair:
                currentHand.remove(tile)
            solution = Player.canHuGivenPair(currentHand)
            if not solution:
                currentHand += pair
            else:
                self.hand = solution
                return True
        return False

    def drawTile(self, deck):
        # take a random tile from the deck, adds to to player's hand
        # then remove it from the deck
        tile = deck.pop(0)
        tile.location = 'hand'
        tile.theta = 90 * self.num
        tile.oldSize = tile.size
        tile.update()
        if tile.suit == 'season' or tile.suit == 'flower':
            self.tossTile(tile)
            tile = self.drawTileFromBack(deck)

        return tile

    def drawTileFromBack(self, deck):
        tile = deck.pop()
        tile.location = 'hand'
        tile.update()
        if tile.suit == 'season' or tile.suit == 'flower':
            self.tossTile(tile)
            tile = self.drawTileFromBack(deck)

        return tile

    def tossTile(self, tile):
        # tosses a selected tile from player's hand
        self.hand.remove(tile)
        tile.oldSize = tile.size
        tile.location = 'tossed'
        tile.update()
        for i in range(len(self.hand)):
            # move all the tiles back
            self.hand[i].index = i
                
        return tile

    def getTossedTile(self, drawnTile):
        # check for mouse press to toss tile
        tossedTile = None
        while tossedTile is None:
            for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for tile in self.hand:
                            if tile.rect.collidepoint(pos):
                                tossedTile = tile
                                return tossedTile
                        if drawnTile != None and drawnTile.rect.collidepoint(pos):
                                tossedTile = drawnTile
                                return tossedTile

    def tossTileAI(self):
        # tosses a tile from AI player's hand
        tileToToss = None

        for tile in self.hand:
            # first check for a tile not in a pair
            value, suit = tile.value, tile.suit
            if (self.hand.count(tile) >= 1):
                continue
            elif Tile(value + 1, suit) or Tile(value - 1, suit) in self.hand:
                continue
            elif Tile(value + 2, suit) or Tile(value - 2, suit) in self.hand:
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

        for i in range(len(self.hand)):
            # move all the tiles back
            self.hand[i].index = i

        print(tileToToss)
        print(tileToToss.location)
        tileToToss.location = 'tossed'
        tileToToss.update()
        return tileToToss

def giveHands(players, deck):
    # initializes players with hands
    players[0].hand = sortHand(getHand(deck))
    players[1].hand = sortHand(getHand(deck))
    players[2].hand = sortHand(getHand(deck))
    players[3].hand = sortHand(getHand(deck))

    for player in players:
        print(len(player.hand))

def replaceFlowers(players, deck):
    # make sure player doesn't have seasons or flowers
    for player in players:
        print(len(player.hand))
        season = Tile(None, 'season', 'deck', None)
        flower = Tile(None, 'flower', 'deck', None)
        while season in player.hand:
            player.tossTile(season)
            tile = player.drawTileFromBack(deck)
            player.hand.append(tile)

        
        while flower in player.hand:
            player.tossTile(flower)
            tile = player.drawTileFromBack(deck)
            player.hand.append(tile)

    return players

def getHand(deck):
    # draws 16 cards from the deck, then removes them from the deck
    hand = []
    while len(hand) < 16:
        tile = deck.pop(0)
        hand.append(tile)
        tile.location = 'hand'
        tile.update()

    return hand

def nonSuitSort(hand):
    dungs = []
    nans = []
    xis = []
    beis = []

    zhongs = []
    fas = []
    boxs = []

    for tile in hand:
        if tile.value == 'dung':
            dungs.append(tile)
        elif tile.value == 'nan':
            nans.append(tile)
        elif tile.value == 'xi':
            xis.append(tile)
        elif tile.value == 'bei':
            beis.append(tile)
        
        elif tile.value == 'zhong':
            zhongs.append(tile)
        elif tile.value == 'fa':
            fas.append(tile)
        elif tile.value == 'box':
            boxs.append(tile)

    sortedHand = []
    sortedHand += ( dungs + nans + xis + beis + 
                    zhongs + fas + boxs )
        
    return sortedHand

def sortHand(hand):
    # sorts hand by suite (not by value)
    nonSuits = []
    nums = []
    circles = []
    sticks = []

    for tile in hand:
        if tile.suit == None:
            nonSuits.append(tile)
        elif tile.suit == 'number':
            nums.append(tile)
        elif tile.suit == 'circle':
            circles.append(tile)
        elif tile.suit == 'stick':
            sticks.append(tile)

    nonSuits = nonSuitSort(nonSuits)
    nums.sort()
    circles.sort()
    sticks.sort()

    sortedHand = nonSuits + nums + circles + sticks
    return sortedHand