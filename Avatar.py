#
# Author: Michele Van Dyne and Lorn Jaeger
#
# Description: Avatar class that describes the data and operations of the
#              main player in the Ultima 0.0 games.
#
import StdDraw
from Tile import Tile
import picture

class Avatar :

    # Constructor for the avatar class
    #
    # Input parameters x and y are the initial integer positions of the
    #    avatar within the world
    def __init__(self, x, y, hp, damage, torch):
        self.x = x                 # current x location
        self.y = y                 # current y location
        self.torch = torch         # how powerful the torch is
        self.TORCH_DELTA = 0.5     # increment/decrement of torch power
        self.hp = hp               # current hp
        self.damage = damage       # damage done to monsters
    # Mutator method to set the avatar to a new location
    #
    # Input parameters are the new integer x and y position
    def setLocation(self, x, y):
        self.x = x
        self.y = y

    # Accessor method
    #
    # Returns the x position of the avatar
    def getX(self):
        return self.x
    
    # Accessor method
    #
    # Returns the y position of the avatar
    def getY(self):
        return self.y
        
    # Accessor method
    #
    # Return remaining hit points   
    def getHitPoints(self):
        return self.hp
    
    # Accessor method
    #
    # Return damage avatar causes
    def getDamage(self):
        return self.damage
    
    # Incure damage to avatar
    #
    # Update health points
    def incurDamage(self, damage):
        self.hp -= damage
    
    # Accessor method
    #
    # Returns the current radius of the torch
    def getTorchRadius(self):
        return self.torch

    # Make our torch more powerful
    #
    # Increases the radius of the torch
    def increaseTorch(self):
        self.torch += self.TORCH_DELTA
        
    # Make our torch less powerful
    #
    # Decreases the radius of the torch
    def decreaseTorch(self):
        self.torch -= self.TORCH_DELTA
        if self.torch < 2.0:
            self.torch = 2.0

    # Draw the avatar
    #
    # Uses the avatar's current position to place and draw the avatar
    #    on the canvas
    def draw(self):
        drawX = (self.x + 0.5) * Tile.SIZE
        drawY = (self.y + 0.5) * Tile.SIZE
        StdDraw.picture(picture.Picture("avatar.gif"), drawX, drawY)

# Main code to test the avatar class    
if __name__ == "__main__":
    # Create an avatar at 5,5
    avatar = Avatar(5, 5)
    print("%d %d %.1f" %(avatar.getX(), avatar.getY(), avatar.getTorchRadius()))
    # Change the avatar's position
    avatar.setLocation(1, 4)
    print("%d %d %.1f" %(avatar.getX(), avatar.getY(), avatar.getTorchRadius()))
    # Increase the torch radius
    avatar.increaseTorch()
    print("%d %d %.1f" %(avatar.getX(), avatar.getY(), avatar.getTorchRadius()))
    # Decrease the torch radius 6 times to make sure it doesn't go below 2.0
    for i in range(0, 6):
        avatar.decreaseTorch()
        print("%d %d %.1f" %(avatar.getX(), avatar.getY(), avatar.getTorchRadius()))
