import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random, time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
DIALOGUE = None
SAUSAGE_TWINS = None
SAUSAGE_TIMER = 0

######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Sparkle(GameElement):
    IMAGE = "Sparkle"
    SOLID = False

class Poo(GameElement):
    IMAGE = "Poo"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Um. You just touched poop! You now have a %r in your inventory. Cool... I guess..." % self)
    def __repr__(self):
        return self.IMAGE

class Character(GameElement):
    IMAGE = "Princess"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Char_bot(Character):
    IMAGE = "Horns"
    SOLID = True

    def interact(self, player):
        global DIALOGUE
        DIALOGUE = self
    def conversation(self, player, choice):
        pass

class Ally(Char_bot):
    def conversation(self, player, choice):
        global DIALOGUE
        GAME_BOARD.draw_msg(unicode("%s: What do you want?" % self.IMAGE + unichr(10) + "A. A sandwich" + unichr(10) + "B. A friend" )) 
        if choice == 'a':
            GAME_BOARD.draw_msg("Gosh, %s, so grabby! I'm not giving you anything!" % player.IMAGE)
            DIALOGUE = None
            return

        elif choice == 'b':
            GAME_BOARD.draw_msg(unicode("Awwwwww, %s, I'll be your friend! Want a bread?" % player.IMAGE))
            bread1 = Food()
            bread1.IMAGE = "Bread"
            GAME_BOARD.register(bread1)
            GAME_BOARD.set_el(self.x-1, self.y+1, bread1)
            DIALOGUE = None
            return
class Adversary(Char_bot):
    def movement(self):
        i = random.randint(1, 4)

        if i == 1:
            next_x = self.x+1
            next_y = self.y

        if i == 2:
            next_x = self.x-1
            next_y = self.y
        if i == 3:
            next_x = self.x
            next_y = self.y-1
        if i == 4:
            next_x = self.x
            next_y = self.y+1

        if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT:
            GAME_BOARD.del_el(self.x, self.y)
            GAME_BOARD.set_el(next_x, next_y, self)
        # time.sleep(2)


    def conversation(self, player, choice):
        global DIALOGUE
        DIALOGUE = None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Gotcha some bling! You have a %r in your inventory!" % self)
    def __repr__(self):
        return self.IMAGE

class Food(GameElement):
    IMAGE = "Bread"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Gotcha some food! You have a %r in your inventory!" % self)
    def __repr__(self):
        return self.IMAGE

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
    ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)


    for rock in rocks:
        print rock

    sparkle = Sparkle()
    GAME_BOARD.register(sparkle)
    GAME_BOARD.set_el(5,2, sparkle)

    ham = Food()
    ham.IMAGE = "Ham"
    GAME_BOARD.register(ham)
    # GAME_BOARD.set_el(1, 2, ham)

    lettuce = Food()
    lettuce.IMAGE = "Lettuce"
    GAME_BOARD.register(lettuce)
    # GAME_BOARD.set_el(3, 1, lettuce)

    cheese = Food()
    cheese.IMAGE = "Cheese"
    GAME_BOARD.register(cheese)
    # GAME_BOARD.set_el(3, 1, cheese)

    eggy = Food()
    eggy.IMAGE = "LittleEggy"
    GAME_BOARD.register(eggy)
    # GAME_BOARD.set_el(3, 1, eggy)

    poo = Poo()
    GAME_BOARD.register(poo)
    GAME_BOARD.set_el(2, 3, poo)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2,PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("Welcome, princess-face. Press 'i' to see your inventory. Move around with your arrow keys.")

    bot1 = Ally()
    GAME_BOARD.register(bot1)
    GAME_BOARD.set_el(6,5, bot1)

    global SAUSAGE_TWINS
    SAUSAGE_TWINS = Adversary()
    SAUSAGE_TWINS.IMAGE = "SausageTwins"
    GAME_BOARD.register(SAUSAGE_TWINS)
    GAME_BOARD.set_el(1,7, SAUSAGE_TWINS)

def keyboard_handler():
    direction = None
    choice = None
    global DIALOGUE
    global SAUSAGE_TIMER

    if DIALOGUE:
        if KEYBOARD[key.A]:
            choice = "a"
        elif KEYBOARD[key.B]:
            choice = "b"
        DIALOGUE.conversation(PLAYER, choice)

   

    elif KEYBOARD[key.UP]:
        # GAME_BOARD.draw_msg("You pressed up")
        direction = "up"
    elif KEYBOARD[key.I]:
        GAME_BOARD.erase_msg()
        GAME_BOARD.draw_msg("Inventory: %s" % PLAYER.inventory)

    elif KEYBOARD[key.RIGHT]:
        # GAME_BOARD.draw_msg("You're right")
        direction = "right"
    elif KEYBOARD[key.LEFT]:
        # GAME_BOARD.draw_msg("You left")
        direction = "left"
    elif KEYBOARD[key.DOWN]:
        # GAME_BOARD.draw_msg("Going down")
        direction = "down"


    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x > GAME_WIDTH-1:
            next_x = GAME_WIDTH-1

        elif next_y > GAME_HEIGHT-1:
            next_y = GAME_HEIGHT-1

        elif next_x < 0:
            next_x = 0

        elif next_y < 0:
            next_y = 0

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:

            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
    SAUSAGE_TIMER += 1
    if SAUSAGE_TIMER % 7 == 0:
        SAUSAGE_TWINS.movement()


