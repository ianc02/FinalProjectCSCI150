from typing import *
import random
import keyboard
import time
from monster import *

# This was written in Python 3.7
# "pip3 install keyboard" was entered into the terminal. I am not
# sure if that would effect someone else running the file.
# If not, all you need to do is hit the run button.

# This is a game in which a player is given basic instructions on how
# the game works, and then are left to their own devices to move openly
# around the board and discover different areas, fight monsters, and
# play through a short story.

# If you want to play through the whole game (approx 30 - 45 min)
# I highly recommend doing the bag side quest by talking to the
# stranger in the Town and carrying a couple potions at any given time.


# These dictionaries are used to tell the program how much
# each item weighs and their cost in the store.
weight_dictionary = {"food": 1, "snorkel": 0, "lantern": 0,
                     "potion": 2, "dagger": 2, "sword": 4, "shield": 5}
price_dictionary = {"food": 3, "potion": 10, "dagger": 25, "sword": 100}

# been_to is used to keep track of certain locations the player has entered
# so that they cannot be looted again.
been_to = {}

# This makes a 25X25 grid of ',' characters as the map. It does this
# by creating a list called map that has 25 Lists whose contents are
# each 25 Lists, which is the Y-axis and X-axis respectively.
map = []
for y in range(25):
    x = []
    for space in range(25):
        x.append(",")
    map.append(x)

# This function adds everything in to the map to make it look how it should.
# It is also called every turn so that it can fix anything like a player
# placing a road on a River. At the very end, it sees what locations the
# player has been to and will mark them off with an 'L'.


def restore_map():
    for y in range(9):
        map[y][5] = "R"
    map[9][4] = "B"
    map[10][4] = "R"
    for y in range(11, 16):
        map[y][y-6] = "R"
    map[16][8] = "R"
    for y in range(17, 20):
        map[y][7] = "R"
    map[20][6] = "R"
    map[21][6] = "B"
    map[22][5] = "R"
    map[23][4] = "R"
    map[24][4] = "R"
    map[2][7] = "C"
    map[6][16] = "C"
    map[23][0] = "C"
    map[5][1] = "T"
    map[2][18] = "T"
    map[9][12] = "T"
    map[23][13] = "T"
    map[13][2] = "S"
    map[21][1] = "M"
    map[20][10] = "A"
    map[9][0] = "A"
    map[3][12] = "A"
    map[7][19] = "A"
    map[18][15] = "A"
    for y in range(16, 25):
        for x in range(18, 25):
            map[y][x] = "F"
    map[16][17] = "F"
    map[14][19] = "F"
    map[13][21] = "F"
    map[14][21] = "F"
    map[13][23] = "F"
    map[14][23] = "F"
    map[15][24] = "F"
    for x in range(20, 23):
        map[15][x] = "F"
    map[19][17] = "F"
    map[22][16] = "F"
    map[23][17] = "F"
    map[24][17] = "F"
    for place in been_to:
        map[place][been_to[place]] = "L"

# This function prints the map onto the screen by clearing out the screen,
# and then joining each term in the map_list with some space between them.


def make_map(map_list: List[List[str]]):
    print("\n"*50)
    for y in map_list:
        print("   ".join(y))


# The combat function is called from a method and takes in
# the player as a class and where they are at on the map to
# determine what kind of monster they get.
def combat(player, spot: str):
    special_check = False
    spawn_chance = 0
    monster = FieldMonster()
    enemy = "Field Monster"

    # These if statements are used to determine what monster is used,
    # their spawn chance, and their special ability if they have one.
    if spot == ",":
        monster = FieldMonster()
        spawn_chance = 0.15
    if spot == "C":
        # The cave monster does not have a spawn chance due to how
        # the actual cave gameplay is set up.
        monster = CaveMonster()
        special_check = monster.check_bleed()
        enemy = "Cave Monster"
    if spot == "R":
        monster = RiverMonster()
        spawn_chance = 0.5
        special_check = monster.check_poison()
        enemy = "River Monster"
    if spot == "F":
        monster = ForestMonster()
        spawn_chance = 0.25
        special_check = monster.check_dodge()
        enemy = "Forest Monster"

    # This if statement determines if the monster spawns or not.
    if random.random() <= spawn_chance or spot == "C":
        print(f"You encountered a {enemy}!")
        start_time = time.time()
        over = False
        while not over:

            # These are determined if the function should continue based on
            # Player and monster health.
            player.check_health()
            monster.check_health()
            if player.dead and monster.dead:
                print("Sorry, You died, but you took out the monster too.")
                break
            elif player.dead:
                print("You have failed your quest...")
                break
            elif monster.dead:
                print("You killed the monster!")
                gold = monster.loot_drop()
                player.wallet += gold
                print(f"You got {gold} gold!")
                input("Press Enter")
                break

            # This checks how much time has passed since the combat function
            # started, turns it into a whole number, and every 3 seconds
            # the enemy attacks and every 2 seconds the player attacks.
            if ((time.time() - start_time) // 1) % 3 == 0:
                # If the player has a shield, they have
                # a 20% chance to block attacks.
                if random.randint(1, 5) == 1 and player.shield:
                    print("You blocked their attack!")
                else:
                    player.health -= monster.attack
                    # If the player is fighting a cave monster, every
                    # time the monster attacks, it has a 7% chance to
                    # make its special ability active.
                    if spot == "C":
                        if special_check:
                            monster.attack += 1
                            print("You're bleeding. Enemy damage grows now.")
                    if player.health < 0:
                        player.health = 0
                    print(f"You got hit! Your health is now {player.health}")

            if ((time.time() - start_time) // 1) % 2 == 0:
                # If the player is fighting a River Monster, they have a
                # 7% chance of being poisoned as they attack.
                if spot == "R":
                    if special_check:
                        player.health -= 2
                        print("You're poisoned. You'll take extra damage \
every time you attack now")
                # This if statement is used to see if the
                # monster is a Forest Monster and if it's special
                # ability (dodging) is active.
                if spot != "F" or spot == "F" and not special_check:
                    monster.health -= player.attack
                    if monster.health < 0:
                        monster.health = 0
                    print(f"You hit your enemy! Enemy health is \
now {monster.health}")
                else:
                    print("The monster dodged your attack!")
                    special_check = monster.check_dodge()
            # The function has to sleep for one second since the entire
            # battle would take place in a few milliseconds otherwise
            # due to the equation above.
            time.sleep(1)


class Player:

    def __init__(self):
        self.previous_x_position = 12
        self.previous_y_position = 12
        self.x_position = 12
        self.y_position = 12
        self.health = 20
        self.attack = 1
        self.hunger = 20
        self.bag = False
        self.eating = False
        self.dead = False
        self.inventory = {"food": 2}
        self.name = ""
        self.snorkel = False
        self.lantern = False
        self.wallet = 0
        self.bag_quest_completed = 0
        self.main_quest_completed = 0
        self.medallion = False
        self.mist = False
        self.shield = False
        self.won = False

    def ask_name(self):
        self.name = input("What is your username?")

    # This method checks player health, and, if the player is dead but have
    # a potion, it heals them back to half health.
    def check_health(self):
        if self.health > 20:
            self.health = 20
        if self.health <= 0:
            if "potion" in self.inventory and self.inventory["potion"] > 0:
                print("You manage to drink your potion before you die, \
saving your life")
                self.health = 10
                self.inventory["potion"] -= 1
            else:
                self.health = 0
                self.dead = True

    # This method runs every turn, and checks for items in inventory that
    # effect some object of the player.
    def check_important_item(self):
        for item in self.inventory:
            if item == "snorkel":
                if self.main_quest_completed < 2:
                    self.main_quest_completed = 2
                self.snorkel = True
            if item == "lantern":
                self.lantern = True
            if item == "dagger":
                if self.inventory["dagger"] > 0:
                    self.attack = 2
            if item == "sword":
                if self.inventory["sword"] > 0:
                    self.attack = 5
            if item == "shield":
                if self.inventory["shield"] > 0:
                    self.shield = True

    # This method takes in a list of what is available and
    # adds it to the inventory. It lists what the player has and
    # then what they can add.
    def add_to_inventory(self, available: List[str]):
        still_adding = True
        while still_adding:
            # total is the total weight the player is carrying.
            total = 0
            for item in self.inventory:
                total += ((weight_dictionary[item]) * self.inventory[item])
            if self.inventory != {}:
                print(f"You are carrying")
                for item in self.inventory:
                    print(item)
                    print(self.inventory[item])
            else:
                print("You are not carrying anything")
            print(f"Total weight is {total}")
            print("Type 'done' if you are done adding items.")
            print(f'The following is available: {", ".join(available)}')
            if not available:
                print("There is nothing more to grab")
                input("Press Enter")
                break
            added = input("What would you like to add to \
your inventory?").lower()
            if added == "done":
                break
            if added in available:
                if not self.bag:
                    max_weight = 10
                else:
                    max_weight = 20
                # This checks if what the player wants to add weighs too much.
                if weight_dictionary[added] + total > max_weight:
                    print("Sorry, that weighs too much.")
                    done = False
                    while not done:
                        # If the player wants to add something that
                        # weighs too much They have the option to drop
                        # something from their inventory.
                        drop = input("Would you like to drop something? \
'Y' or 'N'.").lower()
                        if drop == "y":
                            dropped_item = input("What item would you like \
to drop?").lower()
                            if dropped_item in self.inventory:
                                if self.inventory[dropped_item] > 0:
                                    self.inventory[dropped_item] -= 1
                                done = True
                                if self.inventory[dropped_item] == 0:
                                    print("You don't have any to drop!")
                            else:
                                print("You don't have that item!")
                        elif drop == 'n':
                            done = True
                            still_adding = False
                        else:
                            print("That is not a valid entry.")
                else:
                    if added not in self.inventory:
                        self.inventory[added] = 1
                    elif added in self.inventory:
                        self.inventory[added] += 1
                    available.pop(available.index(added))
            else:
                print("Sorry, that item is not available.")

    # This method determines if the player is eating or not
    # If they are, and have food, it adds 10 to the hunger and
    # takes a food out of the inventory.
    # If not, it takes one away from the hunger and if hunger
    # is above 10, it adds one health point.
    def hunger_value(self):
        if self.eating:
            if "food" in self.inventory and self.inventory["food"] > 0:
                if self.hunger < 20:
                    self.hunger += 10
                    self.eating = False
                if self.hunger >= 20:
                    self.hunger = 20
                    self.eating = False
                self.inventory["food"] -= 1
            else:
                print("\nYou are all out of food.")
                input("Press Enter")
                self.eating = False
        else:
            if self.hunger >= 10:
                self.health += 1
            self.hunger -= 1
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger == 0:
            self.health -= 1

    # This method takes in the parameter 'going' and uses that to
    # determine what action is done to the player.
    def check_structure(self, going: str):
        time.sleep(.5)
        if going != "F" and going != "&":
            self.mist = False
        if going == ",":
            combat(self, going)
        if going == "H":
            print("\nYou find some rest in your home.")
            input("Press Enter")
            self.hunger = 20
            self.health = 20
        if going == "S":
            print("\nYou enter a magical spring that heals all wounds!")
            print("Health is now restored to maximum.")
            self.health = 20
            input("Press Enter")

        # Abandoned houses are one of the few structures
        # that cannot be entered twice.
        if going == "A":
            print("You find an abandoned house. You step over old photos")
            print("as you search for any remaining useful items.")
            loot = ["food", "food"]
            if random.randint(1, 100) <= 50:
                loot.append("food")
            if random.randint(1, 100) <= 20:
                loot.append("dagger")
            if random.randint(1, 100) <= 10:
                loot.append("potion")
            self.add_to_inventory(loot)
            been_to[self.y_position] = self.x_position

        # The town is the most diverse place the player can go.
        # All towns are the same at any point and are the central
        # hub for what the player should do.
        # depending on what the player chooses, it
        # runs the appropriate method.
        if going == "T":
            print("\nYou enter the town. Everyone looks uneasy")
            print("as they know doom lurks at every turn.")
            done_asking = False
            while not done_asking:
                if self.won:
                    return None
                if self.bag_quest_completed < 4:
                    town_choice = input("Where do you want to go? 'store', \
'stranger', 'cemetery', or 'leave'?").lower()
                else:
                    town_choice = input("Where do you want to go? 'store', \
'cemetery', or 'leave?").lower()
                if town_choice == "store":
                    self.town_store()
                elif town_choice == "stranger":
                    self.side_quest_bag()
                elif town_choice == "cemetery":
                    self.town_cemetery()
                elif town_choice == "leave":
                    break
                else:
                    print("That is not a valid entry!")
        # The mineshaft is the other structure that cannot be entered twice
        # If the player takes the lantern.
        if going == "M":
            print("You find an old mineshaft. Inside is a lantern, ")
            print("useful for looking in the dark. \
Do you take take some items?")
            done_asking = False
            while not done_asking:
                take_lantern = input("'Y' or 'N'").lower()
                if take_lantern == 'y':
                    print("There are 3 items available: lantern, food, food")
                    self.add_to_inventory(["lantern", "food", "food"])
                    if "lantern" in self.inventory:
                        been_to[self.y_position] = self.x_position
                    break
                elif take_lantern == "n":
                    break
                elif take_lantern != 'y' and take_lantern != "n":
                    print("That is not a valid entry.")

        if going == "C":
            self.cave(going)

        # If the player has a snorkel, they are able to fight
        # River Monsters and find the shield.
        if going == "R":
            if not self.snorkel:
                print("\nYou can cross, but you can't go under the \
water without the right gear.")
                input("Press Enter")
            else:
                combat(self, going)

        # If the player has gets the medallion, the map is now visible while
        # in the forest.
        if going == "F":
            print("\n"*50)
            if not self.medallion:
                self.mist = True
            combat(self, going)

    # This method checks if the player has a lantern, assigns
    # random numbers to each passageway, and runs the
    # appropriate response depending on which path the player
    # chooses to go down.
    def cave(self, going):
        if "lantern" not in self.inventory:
            print("\nIt is too dark to see.")
            input("Press Enter")
        else:
            been_in_loot = False
            passageway = [1, 2, 3]
            loot = random.randint(0, 2)
            monster = random.randint(0, 1)
            loot_passage = passageway[loot]
            passageway.pop(loot)
            monster_passage = passageway[monster]
            passageway.pop(monster)
            exit_passage = passageway[0]
            print("\nYou enter the cave, uneasy and chilled to the bone.")
            print("You are met with three passageways, which do you take?")
            done_choosing = False
            while not done_choosing:
                passage_choice = 1
                correct_choice = False
                while not correct_choice:
                    passage_choice = (input("'1', '2', or '3'."))
                    if passage_choice == "1" or passage_choice == "2" \
                            or passage_choice == "3":
                        passage_choice = int(passage_choice)
                        break
                    else:
                        print("That is not an appropriate response!")
                if passage_choice == loot_passage and not been_in_loot:
                    gold = random.randint(5, 15)
                    print(f"Congrats! You found {gold} gold!")
                    self.wallet += gold
                    been_in_loot = True
                    if self.y_position == 2:
                        print("You also found a snorkel and some food. \
That's useful!")
                        self.add_to_inventory(["snorkel", "food", "food"])
                elif passage_choice == loot_passage and been_in_loot:
                    print("You shouldn't have been greedy...")
                    combat(self, going)
                    if self.dead:
                        break
                elif passage_choice == monster_passage:
                    print("You find yourself in a monster lair!")
                    combat(self, going)
                    if self.dead:
                        break
                elif passage_choice == exit_passage:
                    print("You leave the cave through the exit.")
                    input("Press Enter")
                    break

    # The store is similar to the add_to_inventory method, but
    # the player cannot drop items to purchase others.
    def town_store(self):
        print('"Welcome adventurer! What would you like to buy?')
        print('I have got food, potions, and weapons!"')
        print("Store prices are as follows:")
        for item in price_dictionary:
            print(item)
            print(price_dictionary[item])

        finished_buying = False
        while not finished_buying:

            total_weight = 0
            for item in self.inventory:
                total_weight += (weight_dictionary[item] *
                                 self.inventory[item])
            print(f"You are holding {total_weight} weight.")
            print(f"You have {self.wallet} gold.")

            buying = input("What would you like to buy? Enter 'done' to \
quit or 'check' to check inventory.").lower()
            if buying == "done":
                break

            if buying == "check":
                for item in self.inventory:
                    print("You have:")
                    print(item)
                    print(self.inventory[item])

            if buying in price_dictionary:

                if self.wallet - price_dictionary[buying] < 0:
                    print("You don't have enough money for that!")

                else:

                    if self.bag:
                        if weight_dictionary[buying] + total_weight > 20:
                            print("That weighs too much!")
                        else:
                            if buying in self.inventory:
                                self.inventory[buying] += 1
                                self.wallet -= price_dictionary[buying]
                            else:
                                self.inventory[buying] = 1
                                self.wallet -= price_dictionary[buying]

                    else:
                        if weight_dictionary[buying] + total_weight > 10:
                            print("That weighs too much!")
                        else:
                            if buying in self.inventory:
                                self.inventory[buying] += 1
                                self.wallet -= price_dictionary[buying]
                            else:
                                self.inventory[buying] = 1
                                self.wallet -= price_dictionary[buying]
            else:
                print("That is not available for purchase.")

    # This method determines how far into the bag quest
    # the player is, and gives the stranger the appropriate
    # response depending on how far they are
    def side_quest_bag(self):
        if self.bag_quest_completed == 1:
            print("'Go North of the Spring and get the letter, ")
            print("then take it West of the North-East Town.'")
            input("Press Enter")
        elif self.bag_quest_completed == 2:
            print("'Take that letter just West of the North-East")
            print("Town and leave it there!'")
            input("Press Enter")
        elif self.bag_quest_completed == 3:
            print(f"'Go get your prize, {self.name}. It's at the peak of")
            print("the river on the West shore side.'")
            input("Press Enter")
        else:
            print('"Well you look like a guy who would want to run')
            print('an errand for me. What do you say?"')
            chosen = False
            while not chosen:
                choice = input("'Y' or 'N'").lower()
                if choice == "y":
                    print('"Great! I need you to go just North of the magic')
                    print('Spring and pick up a letter for me, and then take')
                    print('it just West of the North-East Town, got it?')
                    print('Come back to me if you need a reminder."')
                    input("Press Enter")
                    self.bag_quest_completed = 1
                    break
                if choice == "n":
                    print('"Suit yourself, come back anytime you want."')
                    input("Press Enter")
                    break
                else:
                    print("That was not a valid term")

    # This is the main-quest of the game. Depending on players progress, it
    # gives the appropriate text.
    def town_cemetery(self):
        if self.main_quest_completed == 0:
            print("You see an old woman, standing in front of a \
crypt adorned with")
            print("the engraving of a medallion. The name on the \
medallion is too worn to read.")
            print("You walk up to her and she says")
            print('"Well hello dear, what brings you to this cemetery?')
            print('If it is adventure you are looking for, might I suggest')
            print('visiting the old Mineshaft across the river? If you do, ')
            print('make sure to check out the Northernmost cave."')
            input("Press Enter")
            self.main_quest_completed = 1
        elif self.main_quest_completed == 1:
            print("The old woman looks at you, and says")
            print('"You should visit the mineshaft like I told you and \
then the northern cave."')
            input("Press Enter")
        elif self.main_quest_completed == 2 or self.main_quest_completed == 3:
            print(self.main_quest_completed)
            print("'Good job! With that useful tool you'll be able to swim")
            print("underwater. Now I remember there being another useful \
tool somewhere")
            print("in the straight of the river, but my memory is not as \
good as")
            print("it once was. good luck to you though! Come back once \
you have found it.")
            input("Press Enter")
            self.main_quest_completed = 3
        elif self.main_quest_completed == 4 or self.main_quest_completed == 5:
            print("The woman is gone, but you notice there is writing on \
the crypt")
            print("It reads:")
            time.sleep(3)
            print("RUN")
            time.sleep(.75)
            print("RUN")
            time.sleep(.75)
            print("AGAIN")
            time.sleep(.75)
            print("GO NOW")
            time.sleep(.75)
            print("FROM THE SOUTHERN TOWN")
            time.sleep(.75)
            print("RUN EAST")
            time.sleep(.75)
            print("KEEP RUNNING!")
            time.sleep(2)
            self.main_quest_completed = 5
        elif self.main_quest_completed == 6:
            print("The crypt is open revealing a staircase leading \
down into darkness.")
            print("You can feel an evil presence deep inside.")
            print("Do you want to go inside? If you do, you cannot leave.")
            done_asking = False
            while not done_asking:
                enter_crypt = input("'Y' or 'N'").lower()
                if enter_crypt == 'y':
                    self.crypt()
                    if self.won:
                        return None
                elif enter_crypt == 'n':
                    print("Better judgement leads the way.")
                    input("Press Enter")
                    break
                else:
                    print("That is not a valid entry.")

    # This method checks every turn if the player is currently at an
    # important spot on the map. If they are, and if they have made
    # enough progress, something will happen.
    def check_important_location(self):
        if self.y_position == 3 and self.x_position == 5:
            print("You found a shield! This will help block monster attacks!")
            self.add_to_inventory(["shield"])
            self.main_quest_completed = 4

        if self.y_position == 23 and self.x_position == 23 \
                and self.main_quest_completed == 5:
            print("\nHidden in the mist, you come upon a hut. You knock \
on the door and it creaks open.")
            print("Inside is the old woman, humming to herself. She pays \
no attention to you.")
            print("You see a medallion shining brightly above the fireplace \
and walk towards it and pick it up.")
            print(f"'{self.name}' it reads...")
            print("The woman cackles and says")
            print("'Go on and take it, it is yours after all. I'll be \
seeing you soon.'")
            print("You walk out into a clear forest, the mist gone and \
the wind pushing you North.")
            self.medallion = True
            self.mist = False
            self.main_quest_completed = 6
            input("Press Enter")

        if self.y_position == 15 and self.x_position == 23:
            if "sword" not in self.inventory:
                print("\nYou find a sword in the forest clearing.")
                done_asking = False
                while not done_asking:
                    sword_choice = input("Do you wish to take it? 'Y' \
or 'N'").lower()
                    if sword_choice == "y":
                        self.add_to_inventory(["sword"])
                        if "sword" in self.inventory:
                            been_to[self.y_position] = self.x_position
                        break
                    elif sword_choice == 'n':
                        break
                    else:
                        print('That is not a valid entry.')

        if self.y_position == 12 and self.x_position == 2 \
                and self.bag_quest_completed == 1:
            print("\nYou found the strangers letter. Take it West of \
the North-East Town.")
            input("Press Enter")
            self.bag_quest_completed = 2
        if self.y_position == 2 and self.x_position == 17 \
                and self.bag_quest_completed == 2:
            print("\nYou find a note that says to leave the \
letter here. On the other side")
            print("it says to go to the peak of the peninsula \
formed by the river.")
            input("Press Enter")
            self.bag_quest_completed = 3
        if self.y_position == 15 and self.x_position == 8 \
                and self.bag_quest_completed == 3:
            print("\nYou found a bag! Now you can carry up to 20 weight!")
            input("Press Enter")
            self.bag = True
            self.bag_quest_completed = 4

    # This is just some text and it calls the boss fighting function
    def crypt(self):
        print("The air cools as you go deeper and the")
        print("shadows from your lantern dance along the walls.")
        print("As you get closer to the bottom, you hear faint whispers")
        print(f"saying '{self.name}'. A strong wind blows the lantern out")
        print("and you feel the pressure of the darkness enclose on you.")
        print("You continue on, feeling your way down the steps until you")
        print("finally reach smooth ground.")
        input("Press Enter")
        print(f"'How many times are you going to do this, {self.name}?'")
        print("Candles surrounding the room ignite suddenly, leaving \
an eerie light")
        print("cascading on the floor. The old woman stands in the \
middle of the room.")
        print("You watch as her body contorts and grows. In just a few \
seconds a horrifying")
        print("beast stands where she was. It looks like a grotesque \
mash of every monster")
        print("You've encountered so far.")
        print("'Let's get this over with' the beast growls.")
        input("Press Enter")
        boss_fight(self)


# This function is called if the player presses 'h' on the moving stage
# Depending on their choice, it gives them some tips about aspects
# of the game.
def help_needed():
    print("Would you like to see a list of board symbols (s), items (i), \
or monsters (m)?")
    print("'s', 'i', or 'm'.")
    while True:
        try:
            if keyboard.is_pressed("s"):
                time.sleep(.5)
                print("")
                print("'&': This is your character")
                print("'#': This is a road, you are free from monsters \
on these. Roads")
                print("can only be placed on ',' spaces.")
                print("'T': This is a Town. All of them are the same \
and will")
                print("serve the same function as any other.")
                print("'A': These are Abandoned houses. They contain \
food and sometimes tools.")
                print("'H': This is your house. Coming here restores \
all health and hunger.")
                print("'M': This is the old Mineshaft.")
                print("'L': These are looted places. You get nothing \
more from them.")
                print("'S': This is the magic Spring. It heals all wounds.")
                print("'B': This is just a Bridge. It offers safe passage \
across Rivers.")
                print("',': This is a field. Basic monsters can spawn here.")
                print("'C': This is a Cave. Every time you enter, three \
halls are randomly")
                print("assigned as a 'monster lair', 'treasure room', and \
'exit'. Choose carefully!")
                print("'R': This is a River. Monsters and treasure can be \
found only if you")
                print("have the correct gear to go under water.")
                print("'F': This is the Forest. Certain monsters spawn \
here, and you cannot")
                print("see where you are going while inside.")
                print("")
                input("Press Enter to continue")
                break
            elif keyboard.is_pressed("i"):
                time.sleep(.5)
                print("")
                print("'food': Increases hunger by 10. If hunger is above \
10, it increases")
                print("health by one every turn. Weighs 1.")
                print("'potion': This will raise your health back to 10 \
after dying. Very useful!")
                print("Weighs 2")
                print("'lantern': Allows access into Caves. Weighs 0")
                print("'snorkel': Allows access underwater. Weighs 0")
                print("'shield': Gives the ability for the player to \
block enemy attacks. Weighs 5")
                print("'dagger': Deals 2 damage. Weighs 2")
                print("'Sword': Deals 5 damage. Weighs 4")
                print("")
                input("Press Enter to Continue")
                break
            elif keyboard.is_pressed("m"):
                time.sleep(.5)
                print("")
                print("'Field Monster': Your basic enemy, can't do \
anything special.")
                print("'Cave Monster': Can make you bleed, raising \
their damage every turn.")
                print("'River Monster': Can poison you, dealing \
additional damage when you attack.")
                print("'Forest Monster': Can dodge your attacks \
while still dealing damage.")
                print("")
                input("Press Enter to Continue")
                break
        except:
            print("That was not a valid option.")
            break


# This function takes in the player and map as parameters and creates the map
# based off of player movement.


def movement(user, world_map) -> str:
    # This prints out the current positon of the player
    world_map[user.y_position][user.x_position] = "&"

    # This makes the map so long as the player is not in the forest and
    # they do not have the medallion.
    if not user.mist:
        make_map(map)

    # This while loop is used to display current health and hunger, and prompt
    # for action.
    moving = True
    while moving:
        print(f"Your health is {user.health}")
        print(f"Your hunger is {user.hunger}")
        if user.hunger == 0:
            print("You are starving!")
        print("'w', 'a', 's', 'd' to move. 'e' to eat. 'c' to check \
inventory. 'h' for help.")

        # This while loop continuously checks if a certain key is
        # pressed, and if so, will break. It will only continue if
        # the player presses a valid button.
        while True:
            try:
                if keyboard.is_pressed("h"):
                    time.sleep(.5)
                    print("\n")
                    help_needed()
                    break
                if keyboard.is_pressed("e"):
                    time.sleep(.5)
                    user.eating = True
                    user.hunger_value()
                    moving = False
                    break
                elif keyboard.is_pressed("c"):
                    print('\n')
                    if user.inventory != {}:
                        for item in user.inventory:
                            print(item)
                            print(user.inventory[item])
                        print(f"You have {user.wallet} gold")
                        input("Press Enter")
                    else:
                        print("You have no items.")
                        input("Press Enter")
                    moving = False
                    break
                elif keyboard.is_pressed("w"):
                    time.sleep(.5)
                    if user.y_position - 1 > -1:
                        user.y_position -= 1
                        moving = False
                        user.hunger_value()
                    else:
                        print("You can't go off the map!")
                        input("Press Enter")
                    break
                elif keyboard.is_pressed("s"):
                    time.sleep(.5)
                    if user.y_position + 1 < 25:
                        user.y_position += 1
                        moving = False
                        user.hunger_value()
                    else:
                        print("You can't go off the map!")
                        input("Press Enter")
                    break
                elif keyboard.is_pressed("a"):
                    time.sleep(.5)
                    if user.x_position - 1 > -1:
                        user.x_position -= 1
                        moving = False
                        user.hunger_value()
                    else:
                        print("You can't go off the map!")
                        input("Press Enter")
                    break
                elif keyboard.is_pressed("d"):
                    time.sleep(.5)
                    if user.x_position + 1 < 25:
                        user.x_position += 1
                        moving = False
                        user.hunger_value()

                    else:
                        print("You can't go off the map!")
                        input("Press Enter")
                    break
            except:
                break


        # going to go is used in the check_structure method.
        going_to_go = world_map[user.y_position][user.x_position]

        # This makes sure that the middle of the map stays as the 'H' icon
        if world_map[12][12] != "H":
            world_map[user.previous_y_position][user.previous_x_position]\
                = "H"
        # This places a road where the player was last turn.
        else:
            world_map[user.previous_y_position][user.previous_x_position]\
                = "#"

        world_map[user.y_position][user.x_position] = "&"
        user.previous_x_position = user.x_position
        user.previous_y_position = user.y_position
        return going_to_go


# This function is like the combat function, but made specifically
# for the boss. Since the boss can have all special abilities, this
# function has to account for that.
def boss_fight(player):
    boss = Boss()
    start_time = time.time()
    player.check_health()
    print(f"Your health is {player.health}")
    print(f"The beasts health is {boss.health}")
    time.sleep(1)

    dead = False
    while not dead:
        player.check_health()
        boss.check_health()

        if player.dead and boss.dead:
            print("You died, but you killed the boss too!")
            break
        elif player.dead:
            print("You failed your quest...")
            break
        elif boss.dead:
            print("You Won!")
            player.won = True
            break

        if ((time.time() - start_time) // 1) % 3 == 0:
            if random.randint(1, 5) == 1 and player.shield:
                print("You blocked the attack!")
            else:
                player.health -= boss.attack

                if boss.check_bleed():
                    boss.attack += 1
                    print("You are bleeding! Boss damage grows now!")

                if player.health < 0:
                    player.health = 0
                print(f"You got hit! Your health is now {player.health}.")

        if ((time.time() - start_time) // 1) % 2 == 0:
            if boss.check_dodge():
                print("It dodged your attack!")
            else:
                # Once the boss is at or below 10 health,
                # it takes half as much damage, rounded down,
                # with a minimum of one damage.
                if boss.check_defend():
                    print("It raised its defense! Attacks do less \
damage now!")
                    boss.health -= player.attack // 2
                    if player.attack // 2 == 0:
                        boss.health -= 1
                else:
                    boss.health -= player.attack

                if boss.health < 0:
                    boss.health = 0
                print(f"You struck! The beast has {boss.health} \
health left!")

            if boss.check_poison():
                player.health -= 2
                print("You took additional poison damage!")
                if player.health < 0:
                    player.health = 0
                print(f"Your health is now {player.health}")

        time.sleep(1)


# This is the end of the game and it sort of wraps up the story.
def victory_sequence():
    time.sleep(2)
    print("As soon as you deliver the final blow, the tomb \
starts to rumble.")
    print("You run up the stairs as fast as you can, but the \
tunnels collapse on you.")
    print("You feel yourself get hit by a piece of rubble \
and watch as everything")
    print("goes dark around you.")
    time.sleep(8)
    input("Press Enter")
    print("\n"*50)
    print("You wake up, head throbbing, the wind pushing you North...")
    time.sleep(3)
    print("")
    print("Thank you for playing my game.")


# This lists out basic knowledge of the game for the player, then
# when prompted, starts the opening sequence of the game.
def instructions():
    print("In this game, you (the '&' symbol) move freely around a board.")
    print("A list of what the symbols mean are available, but if you want")
    print("to figure them out on your own, you can. You will use 'w', 'a', ")
    print("'s', and 'd' to move up, left, down, and right, respectively. You")
    print("may also press 'e', 'c', or 'h' to eat, check inventory, \
or get help, respectively.")
    print("Keep your hunger and health up! Enemies have a chance to spawn")
    print("with every move and will be automatically fought. Make sure to")
    print("press the 'Enter' key after typing in a word. You can carry a \
max weight of 10.")
    print("If you die, you respawn with only key items, but all progress")
    print("saved. If you ever get stuck, visiting the cemetery in the Town")
    print("is a good idea. Most single letter actions do not need \
to be entered (Except 'y' or 'n')")
    print("It takes a second or two for the action to go through, so")
    print("be patient. If you press the enter key a lot with no \
purpose, it stays with the ")
    print("game so anytime you need to press Enter, it will do")
    print("it automaically and skip over the text. Be wary of this.")
    print("Most importantly, good luck!")
    input("Press Enter to continue.")
    print("\n"*50)
    print("You wake up, head throbbing, the wind pushing you North...")
    time.sleep(2)
    input("Press Enter")


# This is long for a main function, but broken down it doesn't do too much.
def main():
    # Just lists instructions and asks for a username
    instructions()
    user = Player()
    user.ask_name()

    # This while loop restores the map, so it isn't just a bunch of commas.
    # This first one is for when the player sees the map for the first time,
    # and the one in the next while loop is to make sure roads are not
    # placed on important structures.
    done_playing = False
    while not done_playing:
        restore_map()
        # This is the actual gameplay loop. If the user is not dead, it
        # asks for movement, sees if the player holds an important item,
        # checks if they are at a special location, and then checks
        # if they are at a structure of some kind. The structure has
        # to be last since that method is what calls the combat function.
        # It then checks if the player won the game or if they are inside
        # of the mist.
        dead = False
        while not dead:
            restore_map()
            user.check_health()
            if user.dead:
                break
            going = movement(user, map)
            user.check_important_item()
            user.check_important_location()
            user.check_structure(going)
            if user.won:
                victory_sequence()
                return None
            if user.mist:
                print("\nThere is a thick mist that blocks all sight...")
        # If the player ever breaks out of this loop, it is because
        # they are dead. If so, they are asked if they would like to try
        # again and if so their stats are reset. Otherwise the program ends.
        print("\n"*50)
        print("You failed...")
        time.sleep(2)


        print("Would you like to try again?")
        done_asking = False
        while not done_asking:
            again = input("'Y' or 'N'").lower()
            if again == "y":
                user.health = 20
                user.hunger = 20
                user.dead = False
                user.y_position = 12
                user.x_position = 12
                user.previous_x_position = 12
                user.previous_y_position = 12
                # Players do not lose items necessary for game progression.
                # The player does not actually need the shield, they just
                # need to find it, so that is not included and that is
                # why it has weight.
                if "lantern" in user.inventory:
                    if "snorkel" in user.inventory:
                        user.inventory = {"lantern": 1, "snorkel": 1}
                    else:
                        user.inventory = {"lantern": 1}
                else:
                    user.inventory = {}
                break
            elif again == "n":
                print("Thank you for playing!")
                return None
            else:
                print("That is not a valid entry.")


# This one line executes the entire game.
main()

# https://stackoverflow.com/questions/24072790/detect-key-press-in-python
# This was the website I used to learn how to run code if the player
# pressed a certain button.
# I got inspiration for the map and some gameplay from the game
# "A Dark Room" Developed by Doublespeak Games and Amir Rajan
# and Designed by Michael Townsend.
