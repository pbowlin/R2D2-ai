import sys
import time
import random

from client import DroidClient
import courses
from a_star import A_star
import maneuver
import warriors


game_over = False

# def check_for_bad_guys(self):
#     for warrior in warriors:
#         if not warrior.get_is_good():
#             dist_to_bad_guy = compute_distance(self.get_location(), warrior.get_location())
#             if 1 < dist_to_bad_guy < 2:
#                 self.launch_EMP(warrior)
#                 return None


def launch_EMP(self, bad_guy):
    bad_guy.set_is_active(False)
    self.use_weapon("EMP")


def got_speed_boost():
    return random.random() < 0.2

def get_path(droid, path):

     if path is None:
        return False


    if got_speed_boost():
        path = path[0:3]
        droid.set_location = path[2]
    else:
        path = path[0:2]
        droid.set_location = path[1]

    return path

def compute_distance(location1, location2):
    x_1, y_1 = location1
    x_2, y_2 = location2
    d_x, d_y = (x_2 - x_1), (y_2 - y_1)
    return math.sqrt(d_x**2 + d_y**2)

def get_nearest_opponent(location, warriors):

    d_min = math.inf
    opponent = None
    for w in warriors:
        if w.get_is_good():
            dist = compute_distance(location, w.get_location())
                if dist < d_min:
                    d_min = dist
                    opponent = w

    return d_min, opponent


# TODO: JULIA
def good_droid_turn(droid, w, G, victory_state, warriors):

    if not (droid.get_is_alive()):
        print("YOU LOST")
        # droid falls over
        game_over = True

    path = A_star(G, droid.get_location, victory_state)

    path = get_path(droid, path)
    maneuver.follow_path(droid, path, speed = 0x88, scale_dist = 1)

    if droid in victory_staes:
        print("YOU WON")
        # chirping Sound
        agent_droid.animate(5)
        # headspin

    else:

        dist, bad_droid = get_nearest_opponent(droid.get_location(), warriors)
        if 1 < dist < 2:
            bad_droid.set_is_active(False)
            # headspin

    return True


# TODO: PETER
def bad_droid_turn(droid, warriors, G):
    if not droid.get_is_active():
        droid.set_is_active(True)
        return

    dist, closest_droid = get_nearest_opponent(droid.get_location(), warriors)
    path = a_star(G, droid.get_location(), closest_droid.get_location())

    #TODO: update graph

    if len(path) > 1:
        if got_speed_boost():
            path = path[0:3]
        else:
            path = path[0:2]
    # path = get_path(droid, path)




# get course, find path
G = courses.football_field

victory_state = (7, 2)

good_droid1 = Warrior('Q5-8CC0', (0, 0), True)
good_droid2 = Warrior('Q5-8CC0', (0, 4), True)

bad_droid1 = Warrior('D2-0709', (6, 0), False)
bad_droid2 = Warrior('Q5-8CC0', (6, 4), False)

warriors = [good_droid1, good_droid2, bad_droid1, bad_droid2]

# enemy_droid = HorizontalBadAgent('D2-0709', position = (3, 3),
#     min_bound = (0, 3), max_bound = (3, 3))

agent_start = (0, 0)
agent_goal = (0, 7)

while not game_over:

    for warrior in warriors:
        if warrior.get_is_good():
            good_droid_turn(warrior, G, victory_state, warriors)
        else:
            bad_droid_turn(warrior, warriors):
