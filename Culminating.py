## Import
from graphics import *
import random

##Code to find coordinates for switching between gamestates
##while True:
##    m = win.checkMouse()
##    if m != None:
##        print(m.getX, m.getY)

##Create the win
win = GraphWin("Aliens", 1200, 900, autoflush=False)

##Create the entities
home = Image(Point(600,450),"Gamestate_0.png")

rules = Image(Point(600,450),"Gamestate_1.png")

game = Image(Point(600,450),"Gamestate_2.png")

lose = Image(Point(600,450),"Gamestate_3.png")

won = Image(Point(600,450),"Gamestate_4.png")

credit = Image(Point(600,450),"Gamestate_5.png")

spaceship = Image(Point(600,800),"Spaceship.png")

ufo = Image(Point(600,150),"Ufo.png")

laser = Image(Point(0,0),"Blue_Laser.png")

red_laser = Image(Point(0,0), "Red_Laser.png")

outline = Rectangle(Point(100, 75), Point(1100, 100))
outline.setFill("green")
outline.setOutline("white")

bar = Rectangle(Point(50, 75), Point(50, 100))
bar.setFill("red")
bar.draw(win)

scoreText = Text(Point(50,87.5), "0")
scoreText.setTextColor("white")
scoreText.setSize(25)

healthText = Text(Point(1150,87.5), "0%")
healthText.setTextColor("white")
healthText.setSize(25)

##Setting variables

health = 100
home.draw(win)
gamestate = 0
laserMove = False
counter=0
hitboxX = 50
hitboxY = 50
hitboXX = 20
hitboXY = 70
move_right = True
timesHit = 0
spaceshipHit = 0
ufo_laser = False
score = 0

##Function for health bar
def update_health(new_health):
    global health
    global bar
    health = new_health
    new_width = (1000 * health) / 100
    bar.undraw()
    bar = Rectangle(Point(1100, 75), Point(1100 - new_width, 100))
    bar.setFill("red")
    bar.setOutline("white")
    bar.draw(win)

##main
while True:
    ##Game runs at 50fps
    time.sleep(0.02)
    m = win.checkMouse()
    key = win.checkKey()
    ##Home page buttons
    if gamestate == 0 and m != None:
        if 190 < m.getX() < 990 and 520 < m.getY() < 580:
            gamestate = 5
            home.undraw()
            credit.draw(win)
        if 190 < m.getX() < 1015 and 385 < m.getY() < 465:
            gamestate = 2
            home.undraw()
            game.draw(win)
            spaceship.draw(win)
            ufo.draw(win)
            scoreText.draw(win)
            healthText.draw(win)
            outline.draw(win)
        if 180 < m.getX() < 1030 and 665 < m.getY() < 725:
            gamestate = 1
            home.undraw()
            rules.draw(win)
        if 180 < m.getX() < 1040 and 785 < m.getY() < 860:
            win.close()
    ##Game Rules Code
    elif gamestate == 1 and m != None:
        if 170 < m.getX() < 1045 and 745 < m.getY() < 835:
            gamestate = 0
            rules.undraw()
            home.draw(win)
    ##Game Code
    elif gamestate == 2:
        score += 1
        ## Keyboard Input
        if key == "Left":
            if spaceship.getAnchor().getX() > spaceship.getWidth()/2:
                spaceship.move(-15, 0)
        elif key == "Right":
            if spaceship.getAnchor().getX() < 1200 - spaceship.getWidth()/2:
                spaceship.move(15, 0)
        elif key == "space":
            if laser.getAnchor().getY() <= 0:
                laser.move(spaceship.getAnchor().getX() - laser.getAnchor().getX(), spaceship.getAnchor().getY() - laser.getAnchor().getY())
                laser.draw(win)
                laserMove = True
        ## Laser Code
        if laserMove:
            laser.move(0, -30)
            if laser.getAnchor().getY() < 0:
                laser.undraw()
                laserMove = False
        if ufo_laser == False:
            red_laser.move(ufo.getAnchor().getX() - red_laser.getAnchor().getX(), ufo.getAnchor().getY() - red_laser.getAnchor().getY())
            red_laser.draw(win)
            ufo_laser = True
        if ufo_laser:
            red_laser.move(0, 30)
            if red_laser.getAnchor().getY() > 900:
                red_laser.undraw()
                ufo_laser = False
        ## Colision Detection
        if abs(ufo.getAnchor().getX() - laser.getAnchor().getX()) < hitboxX + 20 and abs(ufo.getAnchor().getY() - laser.getAnchor().getY()) < hitboxY + 16:
            timesHit += 1
            update_health(timesHit)
            healthText.undraw()
            healthText.setText(f'{timesHit}%')
            healthText.draw(win)
        if timesHit == 100:
            timesHit = 0
            gamestate = 4
            laser.move(0, -(laser.getAnchor().getY() + 30))
            laser.undraw()
            red_laser.undraw()
            spaceship.undraw()
            ufo.undraw()
            game.undraw()
            outline.undraw()
            won.draw(win)
            scoreText.undraw()
            scoreText.setSize(36)
            scoreText.move(690,392.5)
            scoreText.draw(win)
            healthText.undraw()
        else:
            scoreText.undraw()
            scoreText.setText(f'{score}')
            scoreText.draw(win)
        if abs(spaceship.getAnchor().getX() - red_laser.getAnchor().getX()) < hitboXX + 20 and abs(spaceship.getAnchor().getY() - red_laser.getAnchor().getY()) < hitboXY + 16:
            spaceshipHit += 1
        if spaceshipHit == 1:
            timesHit = 0
            healthText.setText("0%")
            spaceshipHit = 0
            gamestate = 3
            red_laser.move(0, +(red_laser.getAnchor().getY() + 30))
            laser.undraw()
            red_laser.undraw()
            spaceship.undraw()
            ufo.undraw()
            game.undraw()
            outline.undraw()
            lose.draw(win)
            scoreText.undraw()
            scoreText.setSize(36)
            scoreText.move(680,382.5)
            scoreText.draw(win)
            healthText.undraw()
        else:
            scoreText.undraw()
            scoreText.setText(f'{score}')
            scoreText.draw(win)
        ##UFO movement
        if move_right:
            if ufo.getAnchor().getX() < 1150:
                ufo.move(20, 0)
            else:
                move_right = False
        elif move_right == False:
            if ufo.getAnchor().getX() > 50:
                ufo.move(-20, 0)
            else:
                move_right = True
    ##Lose Screen Code
    elif gamestate == 3 and m != None:
        if 170 < m.getX() < 1045 and 745 < m.getY() < 835:
            gamestate = 0
            lose.undraw()
            scoreText.undraw()
            scoreText.setSize(25)
            scoreText.move(-680,-382.5)
            home.draw(win)
            score = 0
    ##Win Screen Code
    elif gamestate == 4 and m != None:
        if 170 < m.getX() < 1045 and 745 < m.getY() < 835:
            gamestate = 0
            scoreText.undraw()
            scoreText.setSize(25)
            scoreText.move(-690,-392.5)
            won.undraw()
            home.draw(win)
            score = 0
    ##Credit Screen Code
    elif gamestate == 5 and m != None:
        if 170 < m.getX() < 1045 and 745 < m.getY() < 835:
            gamestate = 0
            credit.undraw()
            home.draw(win)
    


    


