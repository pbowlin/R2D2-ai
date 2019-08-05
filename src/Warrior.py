
############################################################
# Warrior Class for Guerilla Project
############################################################
from client import DroidClient
import collections

# create a class for each droid on the board
# this class takes in a DroidClient from client.py as an object
class Warrior(object):

    def __init__(self, droid_id, location, goodness_boolean):
        self.ID = droid_id
        self.weapons_held = collections.Counter()
        self.current_location = location

        # Is this droid good or evil? True refers to good droid, False refers to bad droid
        self.is_good = goodness_boolean

        # Is this droid alive? True refers to droid is alive. False refers to droid is dead.
            # ONLY GOOD DROIDS CAN DIE
        self.is_alive = True

        # Is this droid active? True refers to active droid. False refers to droid that has been stunned.
            # ONLY BAD DROIDS CAN BE STUNNED
        self.is_active = True

        # CODERPAD SECTION
        # droid_client = DroidClient()
        # droid_client.scan()
        # droid_client.connect_to_droid(droid_id)
        self.droid_client = None#droid_client

    def set_location(self, location):
        self.current_location = location

    def get_location(self):
        return self.current_location

    def add_weapon(self, weaponString):
        self.weapons_held[weaponString] += 1

    def use_weapon(self, weaponString):
        if self.weapons_held[weaponString] > 0:
            self.weapons_held[weaponString] -= 1
        else:
            print("Weapon is unavailable")

    def get_is_good(self):
        return self.is_good

    def set_is_alive(self, alive_boolean):
        self.is_alive = alive_boolean

    def get_is_alive(self):
        return self.is_alive

    def set_is_active(self, active_boolean):
        self.is_active = active_boolean

    def get_is_active(self):
        return self.is_active

############################################################
# END OF WARRIOR CLASS FOR GUERILLA PROJECT
############################################################
