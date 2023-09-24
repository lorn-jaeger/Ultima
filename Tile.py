#
# Author: Michele Van Dyne and Lorn Jaeger
#
# Description: Class to describe tile data and operations for the Ultima 0.1
#              game.
#

from enum import Enum, auto
import picture
import StdDraw

#Enumeration class to handle different tile types
class TileType(Enum):
    INVALID = auto()
    FLOOR = auto()
    LAVA = auto()
    WATER = auto()
    FOREST = auto()
    GRASS = auto()
    MOUNTAIN = auto()
    WALL = auto()

# Class that handles all data and operations on tiles
class Tile:
    # Static variable associated with tiles to specity the size
    SIZE = 16

    # Constructor for a tile
    #
    # Paramter is a string or character that specifies the
    #   type of tile
    def __init__(self, code):
        self.lit = False              # Is the tile lit?
        self.occupied = None          # What is the object standing on the tile
    
        if code == "B":
            self.type = TileType.FLOOR
        elif code == "L":
            self.type = TileType.LAVA
        elif code == "W":
            self.type = TileType.WATER
        elif code =="F":
            self.type = TileType.FOREST
        elif code == "G":
            self.type = TileType.GRASS
        elif code == "M":
            self.type = TileType.MOUNTAIN
        elif code == "S":
            self.type = TileType.WALL
        else:
            self.type = TileType.INVALID
            
    # Method to set the occupant of a tile       
    #       
    # None indicates an empty tile
    def setOccupied(self, obj):
            self.occupied = obj
            

    # Accessor for the lit instance variable
    #
    # Returns a True if the tile is lit, False otherwise
    def getLit(self):
        return self.lit

    # Mutator for the lit instance variable
    #
    # Input parament value is a boolean variable
    def setLit(self, value):
        self.lit = value

    # Does light pass through this tile
    #
    # Returns True if the tile is opaque, False otherwise
    def isOpaque(self):
        if self.type == TileType.FLOOR or \
           self.type == TileType.LAVA or \
           self.type == TileType.WATER or \
           self.type == TileType.GRASS or \
           self.type == TileType.INVALID:
               return False
        else:
            return True
        
    # Does this tile do damage
    #
    # Returns 1 if true, 0 if false
    def getDamage(self):
        if self.type == TileType.LAVA:
            return(1)
        else:
            return(0)

    # Can the hero walk through this tile
    #
    # Returns True if the tile can be moved through,
    #    False otherwise
    def isPassable(self):
        if self.type == TileType.WATER or \
           self.type == TileType.MOUNTAIN or \
           self.type == TileType.WALL:
               return False
        else:
            return True

    # Draw the tile at the given location
    #
    # Input parameters x and y are integers specifying
    #    the tile's position within the world grid
    def draw(self, x, y):
        drawX = (x + 0.5) * self.SIZE
        drawY = (y + 0.5) * self.SIZE

        if self.lit:
            if self.type == TileType.FLOOR:
                StdDraw.picture(picture.Picture("brickfloor.gif"), drawX, drawY)
            elif self.type == TileType.LAVA:
                StdDraw.picture(picture.Picture("lava.gif"), drawX, drawY)
            elif self.type == TileType.WATER:
                StdDraw.picture(picture.Picture("water.gif"), drawX, drawY)
            elif self.type == TileType.GRASS:
                StdDraw.picture(picture.Picture("grasslands.gif"), drawX, drawY)
            elif self.type == TileType.FOREST:
                StdDraw.picture(picture.Picture("forest.gif"), drawX, drawY)
            elif self.type == TileType.MOUNTAIN:
                StdDraw.picture(picture.Picture("mountains.gif"), drawX, drawY)
            elif self.type == TileType.WALL:
                StdDraw.picture(picture.Picture("stonewall.gif"), drawX, drawY)
        else:
            StdDraw.picture(picture.Picture("blank.gif"), drawX, drawY)

#
# Main code for testing the Tile class
#
if __name__ == "__main__":
    # Set up test parameters
    SIZE 	= 16
    WIDTH 	= 7
    HEIGHT 	= 2

    # Set up a StdDraw canvas on which to draw the tiles
    StdDraw.setCanvasSize(WIDTH * SIZE, HEIGHT * SIZE)
    StdDraw.setXscale(0.0, WIDTH * SIZE)
    StdDraw.setYscale(0.0, HEIGHT * SIZE)

    # Create a list of codes to test tile creation
    codes = ["B", "L", "W", "F", "G", "M", "S"]
    for i in range(0, WIDTH):
        for j in range(0, HEIGHT):
            tile = Tile(codes[i])
            # Light every second tile
            if (i + j) % 2 == 0:
                tile.setLit(True)
            print("%d %d : lit %s\topaque %s\tpassable %s" %(i, j, tile.getLit(), tile.isOpaque(), tile.isPassable()))
            tile.draw(i, j)
    StdDraw.show(5000)
