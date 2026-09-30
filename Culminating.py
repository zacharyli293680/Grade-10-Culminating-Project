## Import
from graphics import *

## Window
WIDTH = 1200
HEIGHT = 900
win = GraphWin("Aliens", WIDTH, HEIGHT, autoflush=False)

## Gameplay settings
FRAME_DELAY = 0.02        # 50 frames per second
SHIP_SPEED = 10           # pixels per frame while an arrow key is held
LASER_SPEED = 30
UFO_SPEED = 20
BOSS_MAX_HEALTH = 100
DAMAGE_PER_HIT = 10       # 10 hits to win
POINTS_PER_HIT = 100
WIN_TIME_BONUS = 3000     # bonus shrinks by 1 every frame (60 s to zero), so faster wins score more

## Start positions
SHIP_START = Point(600, 800)
UFO_START = Point(600, 150)
OFFSCREEN = Point(-100, -100)   # where lasers wait when they are not flying
SCORE_HUD_POS = Point(50, 87.5)
SCORE_WIN_POS = Point(740, 480)  # next to "SCORE:" on the win screen
SCORE_LOSE_POS = Point(730, 470) # next to "SCORE:" on the lose screen

## Hitboxes: how close two anchors must be (in x and y) to count as a hit
UFO_HIT_X = 70
UFO_HIT_Y = 66
SHIP_HIT_X = 40
SHIP_HIT_Y = 86

## Menu buttons as (left, right, top, bottom) pixel boxes
BTN_PLAY = (190, 1015, 385, 465)
BTN_CREDITS = (190, 990, 520, 580)
BTN_RULES = (180, 1030, 665, 725)
BTN_EXIT = (180, 1040, 785, 860)
BTN_RETURN = (170, 1045, 745, 835)

## Game states
HOME, RULES, PLAYING, LOST, WON, CREDITS = 0, 1, 2, 3, 4, 5

## Screens
home = Image(Point(600, 450), "Gamestate_0.png")
rules = Image(Point(600, 450), "Gamestate_1.png")
game = Image(Point(600, 450), "Gamestate_2.png")
lose = Image(Point(600, 450), "Gamestate_3.png")
won = Image(Point(600, 450), "Gamestate_4.png")
credit = Image(Point(600, 450), "Gamestate_5.png")

## Entities
spaceship = Image(SHIP_START, "Spaceship.png")
ufo = Image(UFO_START, "Ufo.png")
laser = Image(OFFSCREEN, "Blue_Laser.png")
red_laser = Image(OFFSCREEN, "Red_Laser.png")

## HUD
outline = Rectangle(Point(100, 75), Point(1100, 100))
outline.setFill("gray25")
outline.setOutline("white")

bar = Rectangle(Point(100, 75), Point(1100, 100))   # red part = boss health left
bar.setFill("red")
bar.setOutline("white")

scoreText = Text(SCORE_HUD_POS, "0")
scoreText.setTextColor("white")
scoreText.setSize(25)

healthText = Text(Point(1150, 87.5), "100%")
healthText.setTextColor("white")
healthText.setSize(25)

## Keyboard: remember which keys are held down so the ship moves smoothly
keys_down = set()

def on_key_press(event):
    keys_down.add(event.keysym)

def on_key_release(event):
    keys_down.discard(event.keysym)

win.bind_all("<KeyPress>", on_key_press, add="+")
win.bind_all("<KeyRelease>", on_key_release, add="+")
win.bind_all("<FocusOut>", lambda event: keys_down.clear(), add="+")

## Game variables
gamestate = HOME
boss_health = BOSS_MAX_HEALTH
score = 0
frames = 0            # frames played in the current game
laserMove = False     # is the player's laser flying?
ufo_laser = False     # is the UFO's laser flying?
move_right = True

## Helper functions
def clicked(m, box):
    """True if mouse click m landed inside box."""
    return box[0] < m.getX() < box[1] and box[2] < m.getY() < box[3]

def move_to(obj, point):
    """Move a graphics object so its anchor sits on point."""
    a = obj.getAnchor()
    obj.move(point.getX() - a.getX(), point.getY() - a.getY())

def hit(a, b, dx, dy):
    """True if the anchors of a and b are within dx horizontally and dy vertically."""
    pa, pb = a.getAnchor(), b.getAnchor()
    return abs(pa.getX() - pb.getX()) < dx and abs(pa.getY() - pb.getY()) < dy

def update_health():
    """Redraw the boss health bar and percentage."""
    global bar
    bar.undraw()
    width = 1000 * boss_health / BOSS_MAX_HEALTH
    bar = Rectangle(Point(100, 75), Point(100 + width, 100))
    bar.setFill("red")
    bar.setOutline("white")
    if boss_health > 0:
        bar.draw(win)
    healthText.setText(f"{boss_health}%")

def start_game():
    """Reset everything and show the play screen."""
    global gamestate, boss_health, score, frames, laserMove, ufo_laser, move_right
    gamestate = PLAYING
    boss_health = BOSS_MAX_HEALTH
    score = 0
    frames = 0
    laserMove = False
    ufo_laser = False
    move_right = True
    move_to(spaceship, SHIP_START)
    move_to(ufo, UFO_START)
    move_to(laser, OFFSCREEN)
    move_to(red_laser, OFFSCREEN)
    game.draw(win)
    spaceship.draw(win)
    ufo.draw(win)
    outline.draw(win)
    update_health()
    scoreText.setText("0")
    scoreText.draw(win)
    healthText.draw(win)

def end_game(screen, new_state, score_pos):
    """Take down the play screen and show a win or lose screen with the score."""
    global gamestate, laserMove, ufo_laser
    gamestate = new_state
    laserMove = False
    ufo_laser = False
    for obj in (laser, red_laser, spaceship, ufo, game, outline, bar, scoreText, healthText):
        obj.undraw()
    screen.draw(win)
    scoreText.setSize(36)
    scoreText.setText(str(score))
    move_to(scoreText, score_pos)
    scoreText.draw(win)

def show_menu():
    """Return to the home screen from any other screen."""
    global gamestate
    gamestate = HOME
    scoreText.undraw()
    scoreText.setSize(25)
    move_to(scoreText, SCORE_HUD_POS)
    home.draw(win)

## Main loop
home.draw(win)
while not win.isClosed():
    time.sleep(FRAME_DELAY)
    m = win.checkMouse()   # this also refreshes the window
    if win.isClosed():     # the window's X button was pressed
        break

    ## Home page buttons
    if gamestate == HOME:
        if m is not None:
            if clicked(m, BTN_PLAY):
                home.undraw()
                start_game()
            elif clicked(m, BTN_CREDITS):
                gamestate = CREDITS
                home.undraw()
                credit.draw(win)
            elif clicked(m, BTN_RULES):
                gamestate = RULES
                home.undraw()
                rules.draw(win)
            elif clicked(m, BTN_EXIT):
                win.close()
                break

    ## Rules, credits, win and lose screens all have one Return button
    elif gamestate == RULES:
        if m is not None and clicked(m, BTN_RETURN):
            rules.undraw()
            show_menu()
    elif gamestate == CREDITS:
        if m is not None and clicked(m, BTN_RETURN):
            credit.undraw()
            show_menu()
    elif gamestate == LOST:
        if m is not None and clicked(m, BTN_RETURN):
            lose.undraw()
            show_menu()
    elif gamestate == WON:
        if m is not None and clicked(m, BTN_RETURN):
            won.undraw()
            show_menu()

    ## Game code
    elif gamestate == PLAYING:
        frames += 1

        ## Ship movement (arrow keys can be held down)
        ship_x = spaceship.getAnchor().getX()
        half_ship = spaceship.getWidth() / 2
        if "Left" in keys_down and ship_x - SHIP_SPEED >= half_ship:
            spaceship.move(-SHIP_SPEED, 0)
        if "Right" in keys_down and ship_x + SHIP_SPEED <= WIDTH - half_ship:
            spaceship.move(SHIP_SPEED, 0)

        ## Player laser: one on screen at a time
        if "space" in keys_down and not laserMove:
            move_to(laser, spaceship.getAnchor())
            laser.draw(win)
            laserMove = True
        if laserMove:
            laser.move(0, -LASER_SPEED)
            if laser.getAnchor().getY() < 0:
                laser.undraw()
                move_to(laser, OFFSCREEN)
                laserMove = False

        ## UFO laser: fires again as soon as the last one leaves the screen
        if not ufo_laser:
            move_to(red_laser, ufo.getAnchor())
            red_laser.draw(win)
            ufo_laser = True
        red_laser.move(0, LASER_SPEED)
        if red_laser.getAnchor().getY() > HEIGHT:
            red_laser.undraw()
            move_to(red_laser, OFFSCREEN)
            ufo_laser = False

        ## UFO movement: bounce between the window edges
        ufo_x = ufo.getAnchor().getX()
        half_ufo = ufo.getWidth() / 2
        if move_right:
            if ufo_x + UFO_SPEED <= WIDTH - half_ufo:
                ufo.move(UFO_SPEED, 0)
            else:
                move_right = False
        else:
            if ufo_x - UFO_SPEED >= half_ufo:
                ufo.move(-UFO_SPEED, 0)
            else:
                move_right = True

        ## Collision: player laser hits the UFO (laser is used up by the hit)
        if laserMove and hit(laser, ufo, UFO_HIT_X, UFO_HIT_Y):
            laser.undraw()
            move_to(laser, OFFSCREEN)
            laserMove = False
            boss_health -= DAMAGE_PER_HIT
            score += POINTS_PER_HIT
            update_health()
        scoreText.setText(str(score))

        ## Game over checks (a kill and a hit on the same frame counts as a win)
        if boss_health <= 0:
            score += max(0, WIN_TIME_BONUS - frames)
            end_game(won, WON, SCORE_WIN_POS)
        elif ufo_laser and hit(red_laser, spaceship, SHIP_HIT_X, SHIP_HIT_Y):
            end_game(lose, LOST, SCORE_LOSE_POS)
