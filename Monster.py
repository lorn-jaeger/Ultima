# 
# Author: Lorn Jaeger
# 
# Description: A class to describe the monster data and operations for the
#              Ultima 0.1 game. 
#

from enum import Enum, auto
import time
import StdDraw
import picture
import random
from Tile import Tile

class MonsterType(Enum):
    INVALID = auto()
    SKELETON = auto()
    ORC = auto()
    BAT = auto()
    SLIME = auto()
#adding comment to test commit
class Monster:

    # Construct a new monster
    # 
    # param world	- the world the monster moves about in
    # param code	- the string code that distinguishes types of monsters
    # param x		- the x position of the monster
    # param y		- the y position of the monster
    # param hp		- hit points - damage sustained by the monster
    # param damage	- damage the monster causes
    # param sleepMs	- delay between time monster moves
    def __init__(self, world, code, x, y, hp, damage, sleepMs):
            self.world = world
            self.x = int(x)
            self.y = int(y)
            self.hp = int(hp)
            self.damage = int(damage)
            self.sleep = int(sleepMs)/1000
            self.counter = 0                    # Counter for the damage timer
            
            
            if code == "SK":
                self.type = MonsterType.SKELETON
            elif code == "OR":
                self.type = MonsterType.ORC
            elif code == "BA":
                self.type = MonsterType.BAT
            elif code =="SL":
                self.type = MonsterType.SLIME
            else:
                self.type == MonsterType.INVALID
            
            
        
    # The avatar has attacked a monster!
    #
    # param points	- number of hit points to be subtracted from monster
    def incurDamage(self, points):
        self.counter += 3
        self.hp -= points

    #
    # Draw this monster at its current location
    def draw(self):
        
        drawX = (self.x + 0.5) * Tile.SIZE
        drawY = (self.y + 0.5) * Tile.SIZE

        if self.world.tiles[self.x][self.y].getLit():
            
            
            if self.type == MonsterType.SKELETON:
                StdDraw.picture(picture.Picture("rec/skeleton.gif"), drawX, drawY)
            elif self.type == MonsterType.ORC:
                StdDraw.picture(picture.Picture("rec/orc.gif"), drawX, drawY)
            elif self.type == MonsterType.BAT:
                StdDraw.picture(picture.Picture("rec/bat.gif"), drawX, drawY)
            elif self.type == MonsterType.SLIME:
                StdDraw.picture(picture.Picture("rec/slime.gif"), drawX, drawY)

            

    #
    # Get the number of hit points the monster has remaining
    # 
    # return the number of hit points
    def getHitPoints(self):
        return self.hp

    #
    # Get the amount of damage a monster causes
    # 
    # return amount of damage monster causes
    def getDamage(self):
        return self.damage

    #
    # Get the x position of the monster
    # 
    # return x position
    def getX(self):
        return self.x

    #
    # Get the y position of the monster
    # 
    # return y position
    def getY(self):
        return self.y

    #
    # Set the new location of the monster
    # 
    # param x the new x location
    # param y the new y location
    def setLocation(self, x, y):
        self.x = x
        self.y = y


    #
    # Thread that moves the monster around periodically
    def run(self):
        
        # While the monster is alive
        while self.hp > 0:
            time.sleep(self.sleep)
            # Increment damage counter
            if self.counter > 0:
                self.counter -= 1
            # Generate a random direction
            direction = random.randint(0, 4)
            deltaX = 0
            deltaY = 0
            if direction == 1:
                deltaY = 1
            elif direction == 2:
                deltaY = -1
            elif direction == 3:
                deltaX = -1
            elif direction == 4:
                deltaX = 1
    
            x = self.getX() + deltaX
            y = self.getY() + deltaY
            # Check again that the monster is still alive
            # Avoids the monster leaving ghost occupied tiles
            # Then move
            if self.hp > 0:
                self.world.monsterMove(self, x, y)

