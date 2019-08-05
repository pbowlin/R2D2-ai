import random, math
from maneuver import follow_path
from a_star import A_star

from search_and_games import find_path

speed_boost_chance = 0.0

def good_droid_turn(droid, G, warriors, goal):
    if not (droid.get_is_alive()):
        print("GOOD AGENT LOST!")
        # TODO: droid falls over
        return True # Game Over

    ## UPDATE DROID POSITION
    path = find_path(droid.get_location(), goal, G)
    path = get_path(droid, path)
    if not path:
        print("NO PATH FOR GOOD DROID")
        return True # Game Over
    follow_path(droid, path)

    ## UPDATE GRID STATE
    v1 = path[0]
    v2 = path[-1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True
    agent_pos = path[1]

    ## POST UPDATE ACTIONS
    if droid in goal:
        print("YOU WON")
        agent_droid.animate(5) # chirping Sound
        # TODO: headspin
        return True
    else:
        dist, bad_droid = get_nearest_opponent(droid.get_location(), droid, warriors)
        if 1 < dist < 2:
            bad_droid.set_is_active(False)
            # TODO: headspin
    return False

def bad_droid_turn(droid, G, warriors):

    # Skip Droid's Turn
    if not droid.get_is_active():
        droid.set_is_active(True)
        return False

    ## UPDATE DROID POSITION
    dist, closest_droid = get_nearest_opponent(droid.get_location(), droid, warriors)
    # TODO: UPDATE LOGIC FOR SETTING DROID GOAL

    bad_droid_goal = find_bad_droid_goal(G, closest_droid.get_location())

    path = find_path(droid.get_location(), bad_droid_goal, G)
    path = get_path(droid, path)
    if not path:
        print("NO PATH FOR BAD DROID")
        return True  # Game Over
    follow_path(droid, path)

    ## UPDATE GRID STATE
    v1 = path[0]
    v2 = path[-1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True
    enemy_pos = path[1]

    # TODO: POST UPDATE ACTIONS
    return False

# TODO:
def launch_EMP(droid, bad_guy):
    bad_guy.set_is_active(False)
    droid.use_weapon("EMP")

def got_speed_boost():
    return (random.random() < speed_boost_chance)

# Get nearest opponent of the agent
def get_nearest_opponent(location, agent, warriors):
    d_min = math.inf
    opponent = None
    for w in warriors:
        if w.get_is_good() is not agent.get_is_good():
            dist = compute_distance(location, w.get_location())
            if dist < d_min:
                d_min = dist
                opponent = w

    return d_min, opponent

# Get varying path length depending on whether you get a speedboost or not
def get_path(droid, path):

    if path is None:
        return False
    if got_speed_boost() and len(path) > 2:
        path = path[0:3]
        droid.set_location(path[2])
    elif len(path) > 1:
        path = path[0:2]
        droid.set_location(path[1])
    else:
        path = False
    return path

# Compute eucledian distance between two points
def compute_distance(location1, location2):
    x_1, y_1 = location1
    x_2, y_2 = location2
    d_x, d_y = (x_2 - x_1), (y_2 - y_1)
    return math.sqrt(d_x**2 + d_y**2)

def find_bad_droid_goal(G, goal):
    while True:
        goal = (goal[0] + 1, goal[1])
        if G[goal[0]][goal[1]] == False:
            return goal


