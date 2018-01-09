import pygame
import Colors
import random


#Initializing pygame and the fonts
pygame.init()
pygame.font.init()

#Setting the title and reolutions
title = "WinterBread"
resolution = (800, 600)

gameDisplay = pygame.display.set_mode(resolution)
pygame.display.set_caption(title)


#A function to easier make labels
def label(text, font, size, color):
    myfont = pygame.font.SysFont(font, size)
    return myfont.render(text, 1, color)

#The label to keep track of the health
healthLabel = label("Health:", "Consolas", 15, Colors.black)



#The block is basicly Player's class
class Block:

    #   Initializing the Block
    def __init__(self, color, x, y, w, h):
        self.color = color #Color of the player
        self.x = x #Player X
        self.y = y #Player Y
        self.width = w #Player Width
        self.height = h #Player Height
        self.speed = 0.05 #Player Moving speed
        self.moving = False #Current state of moving
        self.health = 100 #Health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #Used for collision detection

        self.exp = 0 #Exp
        self.expgain = 1 #How much exp to add to the 'exp' variable
        self.expmax = 3 #The max of exp before a levelup
        self.level = 1 #The level

        self.points = 0 #Keeping score!

    #   Drawing the player/block
    def draw(self):
        gameDisplay.fill(self.color, rect=[self.x, self.y, self.width, self.height])

    #   Showing the health, and if the health is less than 35, then the healthbar is red or else green
    def show_health(self):
        if player.health <= 35:
            tmp_color = Colors.red #healthbar = red
        else:
            tmp_color = Colors.green #healthbar = green
        gameDisplay.fill(Colors.black, rect=[10, 30, 100, 10]) #Displaying the background for the healthbar
        gameDisplay.fill(tmp_color, rect=[10, 30, self.health, 10]) #Displaying the healthbar

    #   Autokills the player. Just for testing purposes.
    def auto_kill(self):
        self.health -= 2
        if self.health <= 0:
            self.health = 100

    #   Checking if the player is ready to levelup; returns True or False
    def check_level_up(self):
        if player.exp >= player.expmax: #If exp is greater than expgain; levelup
            player.level += 1  #level increments by 1
            player.exp = player.exp - player.expmax
            player.expmax += player.expgain #New expmax
            player.expgain += 1*random.randint(1, 5) #new expgain
            return True
        else:
            return False

    #Draws the levelbar
    def level_bar(self):
        gameDisplay.fill(Colors.black, rect=[120, 30, 100, 10])
        tmp_exp = (float(player.exp) / float(player.expmax)) * 100
        gameDisplay.fill(Colors.nice_blue, rect=[120, 30, tmp_exp, 10])

    #Moves the player if a mousebutton is held down!
    def move(self):
        if self.moving:
            Mousex, Mousey = pygame.mouse.get_pos()
            player.x += -(player.x - Mousex) * player.speed
            player.y += -(player.y - Mousey) * player.speed

            self.rect.x = self.x
            self.rect.y = self.y

    #Keeps the player inside the view
    def dont_move_into_walls(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 800 - self.width:
            self.x = 800 - self.width
        if self.y <= 0 + 50:
            self.y = 0 + 50
        elif self.y >= 600 - self.height:
            self.y = 600 - self.height

#The Enemy Class
class Enemy:

    #Initializing the Enemy
    #Taking a color, x, y, w, h
    def __init__(self, color, x, y, w, h):
        self.color = color #color of the enemy
        self.x = x #Enemy X
        self.y = y #Enemy Y
        self.width = w #Enemy Width
        self.height = h #Enemy height
        self.speed = random.randint(10, 500) #!!!random!!! Enemy speed
        self.speed = float(self.speed)/10000
        self.health = 50 #Health?
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #Rect for collision detection

    #Moving the towards the player
    def move(self, player):
        self.x += -(self.x - player.x) * self.speed
        self.y += -(self.y - player.y) * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

    #Drawing the enemy
    def draw(self):
        gameDisplay.fill(self.color, rect=[self.x, self.y, self.width, self.height])

    #Keeping the enemy inside of the view
    def dont_move_into_walls(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 800 - self.width:
            self.x = 800 - self.width
        if self.y <= 0 + 50:
            self.y = 0 + 50
        elif self.y >= 600 - self.height:
            self.y = 600 - self.height

#The point class
class Point():

    #initializing the Point class
    def __init__(self, color, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h) #For collision
        self.color = color #The color

    #Drawing the point
    def draw(self):
        gameDisplay.fill(self.color, rect=[self.rect.x, self.rect.y, self.rect.width, self.rect.height])

    #setting a new "RANDOM" location
    def new(self):
        self.rect.x = random.randint(1,780)
        self.rect.y = random.randint(50, 580)



"""PRE GAME"""
#For the player
player = Block(Colors.black, 200, 200, 20, 20) #Making the player object
player.health = 100 #Setting the health
player.level = 1 #setting the level


#For the enemy
enemyList = [] #Need a list for keeping track of all the enemies
enemyList.append(Enemy(Colors.nice_red, 700, 500, 20, 20)) #Adding the first enemy


point = Point(Colors.yellow, 400, 400, 20, 20) #Making the point object
point.new() #Creating a new location


clock = pygame.time.Clock() #The clock keeps time of the FPS (Frames Per Second)
exitGame = False #Do not exit
level_count = 300 #300/60=5 minutes



"""GAME LOOP"""
while not exitGame:
    clock.tick(60) #60fps

    for event in pygame.event.get(): #Getting events
        if event.type == pygame.QUIT: #Quitting
            exitGame = True
        if event.type == pygame.MOUSEBUTTONDOWN: #Holding down the key
            player.moving = True
        elif event.type == pygame.MOUSEBUTTONUP: #Letting go of the key
            player.moving = False

    #the player is killed!
    if player.health <= 0:
        while not exitGame:
            clock.tick(25) #60fps

            for event in pygame.event.get():
                if event.type == pygame.quit():
                    exitGame = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    MouseX, MouseY = pygame.mouse.get_pos()
                    if MouseX >= 150 and MouseX <= 350 and MouseY >= 200 and MouseY <= 300:
                        pass
                    elif MouseX >= 450 and MouseX <= 650 and MouseY >= 200 and MouseY <= 300:
                        gameExit = True

            #Making the labels for the menu
            pygame.font.init()
            pygame.init()

            gameOverLabel = label("GAME OVER!", "Consolas", 36, Colors.black)
            finalScoreLabel = label("Your final score is: " + str(player.points), "Consolas", 20, Colors.black)

            restartLabel = label("New Game", "Consolas", 20, Colors.white)
            exitLabel = label("Exit Game", "Consolas", 20, Colors.white)

            #Making the panel
            gameDisplay.fill(Colors.wierd_blue, rect=[100, 100, 600, 400])
            gameDisplay.fill(Colors.nice_gray, rect=[100, 100, 600, 30])
            gameDisplay.fill(Colors.nice_green, rect=[150, 200, 200, 100])
            gameDisplay.fill(Colors.nice_red, rect=[450, 200, 200, 100])

            #Putting in the labels on the panel
            gameDisplay.blit(gameOverLabel, (300, 350))
            gameDisplay.blit(finalScoreLabel, (200, 400))

            gameDisplay.blit(restartLabel, (210, 240))
            gameDisplay.blit(exitLabel, (500, 240))

            pygame.display.update()

    #Drawing the background
    gameDisplay.fill(Colors.white)

    #Moving entities
    player.move()
    for i in enemyList: #Moving all the enemies
        i.move(player)

    #Wall collision
    player.dont_move_into_walls()
    for i in enemyList: #Collision detection for all the enemies
        i.dont_move_into_walls()

    #Drawing stuff!
    player.draw()
    for i in enemyList: #Drawing all the enemies
        i.draw()
    point.draw()

    #Getting points
    if player.rect.colliderect(point.rect): #If the player collides to a point
        player.points += 1 #palyer point +1
        point.new() #new position for the point
        player.exp += player.expgain #exp = exp + expgain
        if player.points%5 == 0: #if the remainder of playerpoints devided by 5 is zero
            enemyList.append(Enemy(Colors.nice_red, 700, 500, 20, 20)) # add a new enemy


    #Drawing bar for text, health and exp/level
    gameDisplay.fill(Colors.nice_gray, rect=[0,0,800,50])
    gameDisplay.fill(Colors.dark_nice_gray, rect=[0,0,800,8])

    #Level and exp labels
    levelLabel = label("Level: " + str(player.level), "Consolas", 15, Colors.black)
    expLabel = label(str(player.exp) + "/" + str(player.expmax), "Consolas", 10, Colors.white)

    #Drawing the exp bar
    player.level_bar()


    # Health
    player.show_health() #Showint the health of the player
    #player.auto_kill() #Temperary killing the player for demo

    #Colliding to the enemies will kill the player
    for i in enemyList:
        if player.rect.colliderect(i.rect):
            player.health -= 1

    #Keeping the health at 100 and not above
    if player.health > 100:
        player.health = 100

    #Displaying labels
    gameDisplay.blit(healthLabel, (10, 10))
    gameDisplay.blit(levelLabel, (120, 10))
    gameDisplay.blit(expLabel, (122, 30))

    # Level Exp
    level_up = player.check_level_up() #Checking to see if player leveled up
    levelUpLabel = label("Level " + str(player.level), "Consolas", 14, Colors.black) #Creating the leveled up label
    if level_up or level_count != 300: #Checking if the player leveled up or if 5 seconds have gone
        gameDisplay.fill(Colors.orange, rect=[690, 60, 100, 50]) #drawing a box
        gameDisplay.fill(Colors.orange_orange, rect=[690, 60, 100, 10])
        if level_count >= 300: #Cheking if the seconds are at zero
            level_count = 0 #Setting the seoncds to zero
            player.health += 15
        level_count += 1    #Increasint the seconds. 1 second = 60 level_counts
        level_up = False    #Doing so that this if statement will only allow the "seconds"
        gameDisplay.blit(levelUpLabel, (700,80)) #Displaying the label

    #Updating the screen
    pygame.display.update()



pygame.quit() #Deinitializing pygame
quit() #quitting... :(
