from typing import *
import random

# All classes are very similar to one another with only
# minor differences. They all have a base health and attack, and their own
# chance of dropping gold.All monsters have a method to check if they are
# dead, and their loot drop. All except the Field Monster have special
# abilities and methods to see if they become active or not. The boss
# class is a little different from the others.


# The Field Monster is the most basic and most common enemy. It has no
# special ability and is rather weak.
class FieldMonster:

    def __init__(self):
        self.health = 5
        self.attack = 1
        self.dead = False

    def check_health(self):
        if self.health <= 0:
            self.health = 0
            self.dead = True

    def loot_drop(self):
        if self.health <= 0:
            return random.randint(0, 5)


# The River Monster has the ability to poison the player, which deals
# damage every time the player attacks.
class RiverMonster:
    def __init__(self):
        self.health = 15
        self.attack = 1
        self.poison = False
        self.dead = False

    def check_health(self):
        if self.health <= 0:
            self.health = 0
            self.dead = True

    def check_poison(self):
        if random.randint(1, 100) <= 10:
            self.poison = True
        return self.poison

    def loot_drop(self):
        if self.health <= 0:
            return random.randint(0, 10)


# The Cave Monster can make the player bleed, which just increases the
# monsters damage per attack every turn.
class CaveMonster:
    def __init__(self):
        self.health = 10
        self.attack = 1
        self.bleed = False
        self.dead = False

    def check_health(self):
        if self.health <= 0:
            self.health = 0
            self.dead = True

    def check_bleed(self):
        if random.randint(1, 100) < 10:
            self.bleed = True
        return self.bleed

    def loot_drop(self):
        if self.health <= 0:
            return random.randint(0, 15)


# The Forest Monster has the ability to dodge an attack. Unlike the other two,
# This ability does not stay active the entirety of the fight otherwise
# it would be impossible to hit the monster.
class ForestMonster:
    def __init__(self):
        self.health = 20
        self.attack = 2
        self.dodge = False
        self.dead = False

    def check_health(self):
        if self.health <= 0:
            self.health = 0
            self.dead = True

    def check_dodge(self):
        self.dodge = False
        if random.randint(1, 100) < 15:
            self.dodge = True
        return self.dodge

    def loot_drop(self):
        if self.health <= 0:
            return random.randint(0, 15)


# The boss can have all abilities active at a time or any mix. It
# does not have a loot drop method since the game is over as soon
# as the player beats it.
class Boss:
    def __init__(self):
        self.health = 50
        self.attack = 3
        self.poison = False
        self.bleed = False
        self.dodge = False
        self.defend = False
        self.dead = False

    def check_health(self):
        if self.health <= 0:
            self.health = 0
            self.dead = True

    def check_poison(self):
        if random.randint(1, 100) <= 7:
            self.poison = True
        return self.poison

    def check_bleed(self):
        if random.randint(1, 100) < 7:
            self.bleed = True
        return self.bleed

    def check_dodge(self):
        self.dodge = False
        if random.randint(1, 100) < 12:
            self.dodge = True
        return self.dodge

    def check_defend(self):
        if self.health <= 10:
            self.defend = True
        return self.defend
