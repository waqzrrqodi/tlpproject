import sys
import time
import random
import subprocess as sp
import os
from platform import system
import pkg_resources



# Check if the user has the required packages installed
if system() == "Windows":
    required = {'progressbar', 'emoji', 'pydub'}
else:
    required = {'progressbar', 'emoji', 'pydub', 'getch'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

# for clearing console (windows and unix systems)
CLEAR = "cls"
if os.name == "posix":
    CLEAR = "clear"
def clear_screen():
    """Clears the screen"""
    sp.call(CLEAR, shell=True)

# If the user is missing any of the required packages, install them
if missing:
    print("Installing dependencies... \nThis may take a while")
    sp.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=sp.DEVNULL)
    clear_screen()
    print("Dependencies installed")
    time.sleep(0.5)
    clear_screen()

from pydub import AudioSegment
from pydub.playback import play
import ui_elements as ui
import characters as ch

if system() == "Windows":
    from msvcrt import getch as getkey
else:
    from getch import getch as getkey_linux # For linux systems, getch is not included in the standard library on windows.

def animate_text(text, sleep_time):
    '''
    Makes text appear one letter at a time at a given speed
    fast, slow, or default
    '''
    FAST = 0.03
    SLOW = 0.1
    DEFAULT = 0.05
    if sleep_time == "fast":
        sleep_time = FAST
    elif sleep_time == "slow":
        sleep_time = SLOW
    else:
        sleep_time = DEFAULT
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sleep_time)
    time.sleep(1)

def wait_for_keypress():
    if system() == "Windows":
        getkey()
    else:
        getkey_linux()

def intro():
    clear_screen() # Clears the screen
    print(ui.intro_name)
    wait_for_keypress()

#-------------------------------------------------------------------------Player and Enemy-----------------------------------------------------------------
valma = ch.Enemy("Waldy", 200, 1000, "God")
simon = ch.Enemy("Simpa", 50, 100, "Human")
goblin = ch.Enemy("Lwittle Gwoblin", 50, 100, "Monster")
bilo = ch.Enemy("Bilo, the Town Rapist", 100, 50, "Human")
qlex = ch.Enemy("Steroid Beast", 25, 400, "Monster")
pangloss = ch.Enemy("Pangloss", 200, 50, "Human")
bandits = ch.Enemy("Bandits", 100, 100, "Human")
neo = ch.Enemy("Neo Järnmalm", 200, 200, "Human")
fulcrum = ch.Enemy("Fulcrum", 250, 100, "Yodie Gang")
bill = ch.Enemy("Retired Orthodox Rabbi Bill Clinton", 300, 40, "Human")
player = None

#-------------------------------------------------------------------------Selection System-----------------------------------------------------------------
class DefaultActionMenu():
    """
    Default player_action menu that is used in the game.
    """
    def default_action_menu(self, action_1, action_2, action_3):
        """
        This is the default player_action menu that is used in the game.
        It is used in the main game loop and in the menu system.
        """
        while True:
            # Prompt the player to attack or defend
            player_action = input("What do you want to do? (A)ttack, (D)efend?")

            # Handle the player's player_action
            try:
                if player_action.lower() == "a":
                    print("Select Attack")
                    if selection == 1:
                        print(f"{action_1} selected")
                        return 1
                    if selection == 2:
                        print(f"{action_2} selected")
                        return 2
                    if selection == 3:
                        print(f"{action_3} selected")
                        return 3
                    # Calculate the damage dealt by the player
                    print(f"You attack the enemy and deal {damage} points of damage!")
                elif player_action.lower() == "d":
                    # Reduce the damage taken by the player by 50%
                    print(f"You defend against the enemy's attack and take {damage * 0.5} points of damage.")

            except(IndexError,ValueError):
                print("Invalid player_action. Please try again.")
                continue

            except:
                print("Unknown error hath occured")
                print(ui.ui_actionmenu)
                selection = int(input("Your command -->"))
                continue


    def fight_menu(self, action_1, action_2, action_3):
        """
        The menu of the choices of the player's attacks.
        """
        clear_screen()
        print(ui.ui_actionmenu)
        ATTACK = "a"
        DEFEND = "d"
        HEAL = "h"
        MORE_INFO = "i"
        player_action = None
        selection = input("What doth thou wish to do? (A)ttack, (D)efend, (H)eal, or get more (i)nfo? --> ")
        try:
            if selection.lower() == ATTACK:
                print(f"Attack Selected")
                return "attack"

            elif selection == DEFEND:
                print(f"Defend selected")
                return "defend"

            elif selection == HEAL:
                print(f"Heal selected")
                return "heal"

            elif selection == MORE_INFO:
                print("Prints more info about the player's attacks and info about the enemy")
                user_choice = input("Please type b to go back --> ")
                if user_choice.lower() == "b":
                    self.fight_menu()
                else:
                    print("Invalid input")
                    self.fight_menu()
            else:
                print("Invalid input")
                self.fight_menu()
        except(IndexError,ValueError):
            print("Invalid input")
            self.fight_menu()
        except:
            print("Unknown error hath occured")
            self.fight_menu()
        return player_action


    def subclass_selection(self, subclass_1, subclass_2):
        """
        The menu of the choices of the subclasses (Human or Beast) of the player and the name of the player.
        """
        clear_screen()
        print(ui.characterselect)
        HUMAN = "1"
        BEAST = "2"
        MORE_INFO = "i"
        player_subclass = None
        choice = input("What is your choice? --> ")
        try:
            if choice == HUMAN:
                print(f"{subclass_1} selected")
                player_subclass = ch.Human()
            elif choice == BEAST:
                print(f"{subclass_2} selected")
                player_subclass = ch.Beast()
            elif choice == MORE_INFO:
                clear_screen()
                print(f"{ui.class_info}")
                user_choice = input("Please type b to go back (or y?)--> ")
                if user_choice == "b" or user_choice == "B":
                    PlayerAndNameSelect()
                elif user_choice == "y" or user_choice == "Y":
                    print("Hidden user aquired! (not really) \nYou are the god now.")
                    player = ch.More_Info_Player()
            else:
                print("Please enter a valid input...")
                time.sleep(1)
                input("Press enter to continue...")
                return
            return player_subclass
        except ValueError:
            print("Please enter a valid number.")
            return

#-------------------------------------------------------------------------Player and Name Selection-----------------------------------------------------------------
class PlayerAndNameSelect(DefaultActionMenu):
    """for selecting the player and the name of the player"""
    def __init__(self):
        clear_screen()
        self.player_subclass = None
        self.name = None
        while True:
            if self.player_subclass is None:
                self.player_select()
            else:
                break
        self.name_select()
        global player
        player = self.create_player()
    def player_select(self):
        """
        player selection menu
        """
        self.player_subclass = self.subclass_selection("Human", "Beast")
    def name_select(self):
        """
        name selection menu
        """
        self.name = input("What is your name? --> ")
        print(f"Welcome {self.name} the {self.player_subclass.SUBCLASS}")
    def create_player(self):
        """
        creates the player
        """
        player = ch.Player(self.player_subclass.STRENGHT, self.player_subclass.HP, self.name, self.player_subclass.SUBCLASS, self.player_subclass.SPEED)
        return player

#-----------------------------------------------------------------------------------Menus-------------------------------------------------------------------------
def menu():
    """
    The menu system of the game that is used to navigate, save, and exit the game.
    """
    GOTO_TUTORIAL = "1"
    SAVE_AND_EXIT = "2"
    INVENTORY = "3"
    CONTINUE = ""
    clear_screen()
    print(ui.ui_textbox)
    menu_choice = input("What do thau wish to do? ");
    if menu_choice == GOTO_TUTORIAL:
        #tutorial()
        print("tutoral")
    if menu_choice == SAVE_AND_EXIT:
        print("Save + Exit")
    if menu_choice == INVENTORY:
        print("inv")
    if menu_choice == CONTINUE:
        animate_text("Continuing with story...", "default")

def tutorial():
    # This is the tutorial to make sure the player knows how to play the game
    user_input = input("Wouldst thou like to see the tutorial, or art thou bold enough to continue without it? (y/n) --> ")
    try:
        if user_input.lower() == "y":
            print("Tutorial")
        elif user_input.lower() == "n":
            print("Continuing without tutorial...")
        else:
            print("Invalid input")
            tutorial()
    except:
        print("Unknown error hath occured")
        tutorial()
            

def level_choice():
    # Choose level and "difficulty"
    pass

#-----------------------------------------------------------------------FIGHTING-----------------------------------------------------------------------#
class FightLoopTM(DefaultActionMenu):


    def __init__(self):
        self.player_health = player.health
        self.player_max_health = player.max_health
        self.player_weapon = player.weapon
        self.armour = player.armour
        self.enemy_health = enemy.health
        self.damage = enemy.damage
        self.fight_loop()

    def attack(self):
        self.enemy_health -= self.player_weapon.damage
        print(f"Thou attacketh the foe and dealeth {self.player_weapon.damage} points of damage!")

    def run(self):
        if random.randint(1, 100) <= 20:
            print("You try to run, but the enemy blocks thau escape!")
            self.fight_loop()
        elif random.randint(1, 100) <= 5:
            print("You try to run, but thau trips and falls, shattering every bone in your body.")
            death()
        else:
            print("Thau successfully run away from the fight!")
            print("Though it came with an item loss")

    def defend(self, damage):
        if self.armour != None:
            print(f"You defend against the enemy's attack and take {damage * self.armour.defense} points of damage.")
        else:
            # Reduce the damage taken by the player by 50% or maybe probability of taking damage?
            print(f"You defend against the enemy's attack and take {damage * 0.5} points of damage.")

    def heal(self):
        if self.player_health != self.player_max_health:
            pass
            # Show the player it's inventory and ask them to select an item to use to heal
            # Calculate the amount of health restored by the player and add it to the player's health
            # If the player's health is greater than the player's maximum health, set the player's health to the player's maximum health
        elif self.player_health == self.player_max_health:
            print("Thou art already at full health!")

    def enemy_attack(self, damage):
        # "Oh no, the enemy hath practiced jujutsu and maketh double damage."
        # damage = damage * 2
        # "Oh no, the enemy hath drunken a kong strong and maketh triple damage."
        # damage = damage * 3
        attack_probability = random.randint(1, 100)
        if attack_probability <= 20:
            print(f"The enemy attacks you and deals {damage} points of damage.")
        elif attack_probability <= 5:
            print(f"Oh no, The enemy is listening to some banger tunes and attacks you with double ({damage * 2}) points of damage.")

    def fight_loop(self):
        '''The proprieatary fighting loop of the game (no copying pls) which is used to fight enemies and makes the shots about what happens next'''
        while self.player_health > 0 or self.enemy_health > 0:
            # Display the current health of the player and the enemy
            print(f"Player health: {self.player_health}")
            print(f"Enemy health: {self.enemy_health}")

            # Display the fight menu and get the user's selection
            user_selection = self.fight_menu()
            if user_selection == "attack":
                self.attack()
            elif user_selection == "run":
                self.run()
            elif user_selection == "defend":
                self.defend(self.damage)
            elif user_selection == "heal":
                self.heal()

            # Check if the enemy has been defeated
            if self.enemy_health <= 0:
                print("Thou hast defeated the enemy!")
                break

            # Enemy attacks the player
            self.enemy_attack(self.damage)

            # Check if the player has been a "has been"
            if self.player_health <= 0: death()

#--------------------------------------------------------------Death and Endings-----------------------------------------------------------------------#




def death():
    print("You have died")
    # if player does something stupid and dies play ending 1
    # if player dies in a boss fight play ending 2
    # if player dies in a normal fight play ending 3
    print("Game over")
    # Prints the ending and stats of the player and their achievements.
    wait_for_keypress()
    time.sleep(2)
    quit()

def ending1():
    pass

def ending2():
    pass

def ending3():
    pass

#-------------------------------------------------------------------------Game Functions-----------------------------------------------------------------


intro()
PlayerAndNameSelect()
menu()
tutorial()
    # while True:
    # level_choice() with narration and the story
    # default action menu
    # if there is enemy spawn enemy and enter fight loop
    # if there is chest spawn chest and enter chest loop and inventory loop
    # if there is trap spawn trap and enter trap loop
    # Continue story with different parts of the story depending on the level obsticles
    # Go back to top of loop
    # Give player option to go back to menu
    # If player goes back to menu give them option to save and exit or continue