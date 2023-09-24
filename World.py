#
# Author: Michele Van Dyne and Lorn Jaeger
#
# Description: World class that holds all information about tiles and
#              characters in the Ultima 0.1 game

from Tile import Tile
from Avatar import Avatar
from Monster import Monster
import math
import sys
import StdDraw
import random
import threading

class World:

    # Constructor for the world
    #
    # Input parameter is a file name holding the configuration information
    #    for the world to be created
    #    The constructor reads in file data, stores it in appropriate
    #    attributes and sets up the window within which to draw.
    #    It also initializes the lighting in the world.
    def __init__(self, filename):
        # ALlow for Ultima.py to aquire a lock
        self.lock = threading.Lock()
        
        with open(filename, 'r') as f:
            # Read in the first line of text
            line = f.readline().split()
            
            # Translate that line to width and height
            self.width = int(line[0])
            self.height = int(line[1])
            
            # Read in the second line of text
            line = f.readline().split()
            
            # Translate that into the avatar position
            self.avatar = Avatar(int(line[0]), int(line[1]), int(line[2]), int(line[3]), float(line[4]))
            self.tiles = [[None for i in range(self.height)] for j in range(self.width)]
            
            # Read in the rest of the file and parse into color blocks
            line = f.read().split()
            index = 0
            for i in range(0, self.height):
                for j in range(0, self.width):
                    self.tiles[j][self.height - i - 1] = Tile(line[index])
                    index += 1
            
            # After all the tiles are created the rest of the file is monsters
            # Create all monsters
            line = line[self.width*self.height:]
            i = 0
            # Keep track of number of monsters as a game ending condition
            self.monsterList = []
            while i < len(line):
                monster = Monster(self, line[i], line[i+1], line[i+2], line[i+3], line[i+4], line[i+5])
                self.monsterList.append(monster)
                # Set the tile the monster stands on as occupied
                self.tiles[int(line[i+1])][int(line[i+2])].setOccupied(monster)
                # Start the monster thread
                threading.Thread(target=monster.run, daemon=True).start()
                i += 6
            f.close()

        # Set up the window for drawing
        StdDraw.setCanvasSize(self.width * Tile.SIZE, self.height * Tile.SIZE)
        StdDraw.setXscale(0.0, self.width * Tile.SIZE)
        StdDraw.setYscale(0.0, self.height * Tile.SIZE)

        # Initial lighting
        self.light(self.avatar.getX(), self.avatar.getY(), self.avatar.getTorchRadius())
        self.draw()



    # Accept keyboard input and performs the appropriate action
    # 
    # Input parameter is a character that indicates the action to be taken
    def handleKey(self, ch):
        deltaX = 0
        deltaY = 0
        if ch == 'w':
            deltaY = 1
        elif ch == 's':
            deltaY = -1
        elif ch == 'a':
            deltaX = -1
        elif ch == 'd':
            deltaX = 1
        elif ch == '+':
            self.avatar.increaseTorch()
        elif ch == '-':
            self.avatar.decreaseTorch()
            
        if deltaX != 0 or deltaY != 0:    
            self.avatarMove(deltaX, deltaY)    
        
        # Update lighting to reflect avatars new position
        self.setLit(False)
        self.light(self.avatar.getX(), self.avatar.getY(), self.avatar.getTorchRadius())
        
        
    # Check if avatar is alive
    #   
    # Used as a condition to end the game
    def avatarAlive(self):
        return(self.avatar.getHitPoints() > 0)
    
        
    # Moves a monster given a monster object and x,y coordinates
    #
    # Checks if tile at coordinates is valid and passable and not ocuupied by 
    # a monster. If an avatar is present, incur damage. If not, move to the tile
    # take damage and update occupation status.
    def monsterMove(self, monster, x, y):
        # Check if tile is valid to move to
        if x >= 0 and x < self.width and \
           y >= 0 and y < self.height and \
           self.tiles[x][y].isPassable() and not\
           isinstance(self.tiles[x][y].occupied, Monster):

            # Do damage to avatar if present
            if x == self.avatar.getX() and y == self.avatar.getY():
                self.avatar.incurDamage(monster.getDamage())

                
            else:
                # Do damage associated with tile
                monster.incurDamage(self.tiles[x][y].getDamage())
                # Set previous tile to unoccupied
                self.tiles[monster.getX()][monster.getY()].setOccupied(None)
                # Update position
                monster.setLocation(x, y)
                self.tiles[x][y].setOccupied(monster)
                monster.draw()
        
     
    # Checks for a variety of cases and moves the avatar
    #
    # Called by the method handleKey if a direction key is pressed
    def avatarMove(self, x, y):
        # Get prospective x,y coordinates
        x = self.avatar.getX() + x
        y = self.avatar.getY() + y

        # Check if coords are in bounds
        if x >= 0 and x < self.width and \
           y >= 0 and y < self.height:
        
           tile = self.tiles[x][y]
           # Check if passable
           if tile.isPassable():
               # Check for a monster, if present do damage to the occupier
               if tile.occupied != None:
                   tile.occupied.incurDamage(self.avatar.damage)
               # Otherwise, move avatar
               else:   
                  self.avatar.incurDamage(tile.getDamage())
                  self.avatar.setLocation(x, y)
        
    
    # Draw all the lit tiles
    #
    # Only action is to draw all the components associated with the world
    def draw(self):
        # First update the lighting of the world
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.tiles[x][y].draw(x, y)
        # Draw all monsters
        for monster in self.monsterList:
            if monster.hp <= 0:
                self.monsterList.remove(monster)
                self.tiles[monster.getX()][monster.getY()].setOccupied(None)
            else:
                monster.draw()
        # Draw avatar
        self.avatar.draw()

    # Light the world
    #
    # Input parameters are the x and y position of the avatar and the
    #    current radius of the torch.
    #    Calls the recursive lightDFS method to continue the lighting
    # Returns the total number of tiles lit
    def light(self, x, y, r):
        result = self.lightDFS(x, y, x, y, r)
        print("light(%d, %d, %.1f) = %d" %(x, y, r, result))
        return result
    
    # Recursively light from (x, y) limiting to radius r
    #
    # Input parameters are (x,y), the position of the avatar,
    #    (currX, currY), the position that we are currently looking
    #    to light, and r, the radius of the torch.
    # Returns the number of tiles lit
    def lightDFS(self, x, y, currentX, currentY, r):
        if currentX < 0 or currentY < 0 or \
           currentX >= self.width or currentY >= self.height or \
           self.tiles[currentX][currentY].getLit():
                return 0
        
        result = 0
        deltaX = x - currentX
        deltaY = y - currentY
        
        dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)

        if dist < r:
            self.tiles[currentX][currentY].setLit(True)
            result += 1
                                                            
            if not self.tiles[currentX][currentY].isOpaque():
                result += self.lightDFS(x, y, currentX - 1, currentY, r)	# west		
                result += self.lightDFS(x, y, currentX + 1, currentY, r)	# east
                result += self.lightDFS(x, y, currentX, currentY - 1, r)	# north
                result += self.lightDFS(x, y, currentX, currentY + 1, r)	# south							
        return result
            
    # Turn all the lit values of the tiles to a given value. Used
    #    to reset lighting each time the avatar moves or the torch
    #    strength changes
    #
    # Input paramter is a boolean value, generally False, to turn off
    #    the light, but is flexible to turn the light on in some future
    #    version
    def setLit(self, value):
        for x  in range(0, self.width):
            for y in range(0, self.height):
                self.tiles[x][y].setLit(value)
                
            
    #
    # Return the length of the list of monsters
    def getNumMonsters(self):
        return len(self.monsterList)
    
# Main code to test the world class
if __name__ == "__main__":
    world0 = World(sys.argv[1])
    world0.draw()
    StdDraw.show()
