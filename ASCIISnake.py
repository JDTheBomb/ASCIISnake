#############AsciSnake###############
"""
This ascii snake code takes key input and gives visual output.
This is ascii snake so print statements are the visual output.
"""
import os
import sys
import tty
import termios
import signal
from platform import system
from time import sleep
from random import randint


def getkey(): #made a get key function only using built in python libraries
  """Get a single key press and return the resulting character."""

  def timeout_handler(signum, frame): #we need a time out so were not stuck on an input prompt
    raise TimeoutError

  # Set up the signal handler for the timeout
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(1) #A 1 second timeout

  # Get the key press
  try:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1) #read the first byte of input data
  except TimeoutError:
    return None
  finally:
    # Reset the terminal settings
    signal.alarm(0)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  if ch == "\x1b": #this for loop fixes arrow key inputs because arrow key inputs return 3 bytes.
    ch += sys.stdin.read(2)
  return ch


class Screen:  #Create a screen class that has properties that can be edited and so the code isn't big.

  def __init__(self, width, height, backGroundColor=" "): #Setting Basic Data
    self.width = width
    self.height = height
    self.backGroundColor = backGroundColor
    self.grid = [backGroundColor * width] * height

  def render(self): #Basically a for loop that goes through the grid list and prints it out.
    print("+" + ("-" * self.width) + "+")
    for row in range(0, self.height):
      print("|" + self.grid[row] + "|")
    print("+" + ("-" * self.width) + "+\n")

  def clear(self):
    self.grid = [self.backGroundColor * self.width] * self.height
    os.system("cls" if system() == "Windows" else "clear") #clears the screen based on operating system


class Snake:  #Have a snake with properties that we can draw onto the screen.

  def __init__(self, x, y, snakecolor="O", startingLength=5): #Basic snake data that is customizable
    self.snakecolor = snakecolor
    self.startX = x
    self.startY = y
    self.startingLength = startingLength
    self.reset()

  def draw(self, GS): #draws snake onto any game screen you give this function.
    for i in self.body:  ##Loop through the snake body
      row = GS.grid[i[1]%GS.height]
      GS.grid[i[1]%GS.height] = row[:(i[0]-1)%GS.width] + self.snakecolor + row[(i[0])%(GS.width+1):]

  def move(self): #moves the snake based on the speed variable.
    speed = (abs(self.speedx) if abs(self.speedx) > 0 else abs(self.speedy))
    self.body.insert(0, [
      self.body[0][0] + (self.speedx if 0 >= abs(self.speedy) else 0),
      self.body[0][1] + (self.speedy if 0 >= abs(self.speedx) else 0)
    ])
    self.body.pop()

  def getScore(self): #Gets the score based on length
    return len(self.body) - self.startingLength - 1

  def isCollided(self): # checks for self snake collision
    for i in range(0,len(self.body)):
      for j in range(0,len(self.body)):
        if i!=j:
          if self.body[i]==self.body[j]:
            return True
    return False

  def grow(self): #adds onto the snake
    self.body.append(self.body[-1])
  def reset(self): #resets the snake so you can have an endless game without starting the file again.
    self.speedx = 1
    self.speedy = 0
    self.body = [[self.startX, self.startY]]
    for i in range(1, self.startingLength+1):
      self.body.append([self.startX - i, self.startY])

def drawApples(GS,apples,color): #simple apple draw function
      for i in apples:  ##Loop through the snake body
        row = GS.grid[i[1]]
        GS.grid[i[1]] = row[:i[0]-1] + color + row[i[0]:]

gameScreen = Screen(30, 10, " ") #make a game screen for user to see
player = Snake(15, 5, "o") #make a player for user to use
wins = 0 # lets keep track of wins
while True: #infinite games
  player.reset() #reset the player each game.
  notDead = True
  apples = [] #keep a list of the apples
  for i in range(0,3): #add apples.
    apples.append(
      [randint(0,gameScreen.width-1)
       ,randint(0,gameScreen.height-1)]
    )
    
  while notDead: #keep the snake going until dead.
    print("Press 'e' to exit.") #inform user
    print("Press asdw or arrowkeys to move")
    print("Wins:", wins)
    print("Score:", player.getScore())

    drawApples(gameScreen, apples, 'x') #draw apples function
    player.draw(gameScreen) #we want to see the snake
    gameScreen.render() #we want to see the screen
    k = getkey() #lets get movement down with the keys
    if k == '':
      pass
    elif k == '\x1b[A' and player.speedy!=1 or k == "W" or k == "w":
      player.speedy = -1
      player.speedx = 0
    elif k == '\x1b[B' and player.speedy!=-1 or k == "S" or k == "s":
      player.speedy = 1
      player.speedx = 0
    elif k == '\x1b[C' and player.speedx!=-1 or k == "D" or k == "d":
      player.speedy = 0
      player.speedx = 1
    elif k == '\x1b[D'and player.speedx!=1 or k == "A" or k == "a":
      player.speedy = 0
      player.speedx = -1
    elif k == 'e':
      quit()
    player.move()
    
    if player.isCollided() or not (gameScreen.width>=player.body[0][0]>=0) or not (gameScreen.height-1>=player.body[0][1]>=0): #check player collision
      notDead = False
    for i in range(0,len(apples)): #check apple collision
      if apples[i] == player.body[0]:
        apples.pop(i)
        player.grow()
        apples.append(
          [randint(0,gameScreen.width-1)
           ,randint(0,gameScreen.height-1)]
        )
    if len(player.body) == gameScreen.width*gameScreen.height: #check if the snake filled the screen.
      print("PLAYER WINS!!!!")
      wins+=1
      notDead = False
    
    sleep(0.1) #let their be basically a cooldown so we don't overwelm the computer and so we have frames
    gameScreen.clear() #clear the terminal for frames
