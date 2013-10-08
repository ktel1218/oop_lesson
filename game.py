import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
DIALOGUE = False

######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

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
        GAME_BOARD.draw_msg(unicode("%s: What do you want?" % self.IMAGE + unichr(10) + "A. A sandwich" + unichr(10) + "B. A friend" )) 
        global DIALOGUE
        DIALOGUE = IMAGE



        # if option == 'a':
        #     choose(a)
        #     GAME_BOARD.draw_msg(unicode("Gosh, %s, so grabby!" % player.IMAGE))
        # elif option == 'b':
        #     GAME_BOARD.draw_msg(unicode("Awwwwww, %s, I'll be your friend! Want a sandwich?" % player.IMAGE))
        #     player.inventory.append('Sandwich')

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Gotcha some bling! You have a %r in your inventory!" % self)
    def __repr__(self):
        return self.IMAGE

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
    ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2,PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("Welcome, princess-face.")

    gem1 = Gem()
    GAME_BOARD.register(gem1)
    GAME_BOARD.set_el(3, 1, gem1)

    gem2 = Gem()
    gem2.IMAGE = "OrangeGem"
    GAME_BOARD.register(gem2)
    GAME_BOARD.set_el(3, 4, gem2)

    bot1 = Char_bot()
    GAME_BOARD.register(bot1)
    GAME_BOARD.set_el(6,5, bot1)

def keyboard_handler():
    direction = None
    option = None
    global DIALOGUE

    if KEYBOARD[key.UP]:
        GAME_BOARD.draw_msg("You pressed up")
        direction = "up"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
        GAME_BOARD.draw_msg("Inventory: %s" % PLAYER.inventory)

    elif KEYBOARD[key.RIGHT]:
        GAME_BOARD.draw_msg("You're right")
        direction = "right"
    elif KEYBOARD[key.LEFT]:
        GAME_BOARD.draw_msg("You left")
        direction = "left"
    elif KEYBOARD[key.DOWN]:
        GAME_BOARD.draw_msg("Going down")
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
            print PLAYER.inventory




        
        # else:
        #     GAME_BOARD.draw_msg("AHAHAH. CAN'T!!!")
    if DIALOGUE:
        choice = None
        if KEYBOARD[key.A]:
            choice = "a"
            Char_bot.conversation(PLAYER, choice)
            # DIALOGUE = False
        elif KEYBOARD[key.B]:
            choice = "b"
            Char_bot.conversation(PLAYER, choice)

            # DIALOGUE = False      