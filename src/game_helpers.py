import random, math
from maneuver import follow_path
from a_star import A_star
from sound import play_airstrike
from search_and_games import find_path

speed_boost_chance = 0.0
call_airstrike_prob = 0.5

def good_droid_turn(droid, G, warriors):
    if not (droid.get_is_alive()):
        print("GOOD AGENT LOST!")
        # TODO: droid falls over
        return True # Game Over

    goal = find_good_droid_goal(G, droid.get_location())
    print('good droid goal: ' + str(goal))

    ## UPDATE DROID POSITION
    path = find_path(droid.get_location(), goal, G)
    path = get_path(droid, path)
    if not path:
        print("NO PATH FOR GOOD DROID") ##GAME SHOULD NOT END IF 2 GOOD DROIDS 
        return True # Game Over
    
    if not droid.debug:
        follow_path(droid, path)

    ## UPDATE GRID STATE
    v1 = path[0]
    v2 = path[-1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True
    #agent_pos = path[1]

    ## POST UPDATE ACTIONS
    droid_location = droid.get_location()
    if droid_location[0] > len(G) - 2:
    #if droid in goal:
        print("YOU WON")
        droid.droid_client.animate(3, 0) # chirping Sound
        # TODO: headspin
        return True
    else:
        dist, bad_droid = get_nearest_opponent(droid.get_location(), droid, warriors)
        if 1 < dist < 2:
            if droid.EMPs > 0:
                launch_EMP(droid, bad_droid)

    return False

def launch_EMP(droid, bad_guy):
    print('Launching EMP')
    bad_guy.set_is_active(False)
    print('bad guy now inactive')
    bad_guy.droid_client.play_sound(5, 0)
    print('after play sound')

    for i in range(4):
        bad_guy.droid_client.rotate_head(45)
        bad_guy.droid_client.rotate_head(0)
        bad_guy.droid_client.rotate_head(90)
        bad_guy.droid_client.rotate_head(0)
    
    droid.EMPs -= 1

def call_airstrike(agents):
    print("AIRSTRIKE CALLED")
    prob_airstrike_hit = 0.5
    good_living_agents = []
    bad_agents = []
    for agent in agents:
        if agent.get_is_good() and agent.get_is_alive():
            good_living_agents.append(agent)
        elif not agent.get_is_good():
            bad_agents.append(agent)

    if len(good_living_agents) > 1:
        agent_to_attack = good_living_agents[0] if random.random() < .5 else good_living_agents[1]
    else:
        agent_to_attack = good_living_agents[0] 
        prob_airstrike_hit /= 2  
    

    play_airstrike()

    if random.random() <= prob_airstrike_hit:
        agent_to_attack.droid_client.animate(14, 0) ##fall over and die
        agent_to_attack.set_is_alive(False)
        good_living_agents.remove(agent_to_attack)
        print("AIRSTRIKE HIT")
        if len(good_living_agents) == 0:
            bad_agents[0].droid_client.animate(3,0)
            bad_agents[1].droid_client.animate(3,0)
            return True ##this means the airstrike killed last living good agent
    else:
        agent_to_attack.droid_client.animate(7, 0) ##airstrike missed target
    return False

def bad_droid_turn(droid, G, warriors):

    # Skip Droid's Turn
    if not droid.get_is_active():
        print('droid is inactive')
        droid.set_is_active(True)
        return False

    if random.random() <= call_airstrike_prob:
        if call_airstrike(warriors):
            return True ## this means the airstrike killed the last living good_agent

    ## UPDATE DROID POSITION
    dist, closest_droid = get_nearest_opponent(droid.get_location(), droid, warriors)
    # TODO: UPDATE LOGIC FOR SETTING DROID GOAL

    bad_droid_goal = find_bad_droid_goal(G, closest_droid.get_location())

    path = find_path(droid.get_location(), bad_droid_goal, G)

    print('path is:' + str(path))
    path = get_path(droid, path)
    if not path:
        print("NO PATH FOR BAD DROID")  ##GAME SHOULD NOT END IF WE HAVE 2 BAD DROIDS
        return True  # Game Over
    
    if not droid.debug:
        follow_path(droid, path)

    ## UPDATE GRID STATE
    v1 = path[0]
    v2 = path[-1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True
    #enemy_pos = path[1]

    # TODO: POST UPDATE ACTIONS
    return False

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

def find_good_droid_goal(G, location):
    goal_distance = 1000000
    x = len(G)-1
    goal = (x, 0)

    for y in range(len(G[-1])):
        cell_distance = compute_distance(location, (x, y))
        if cell_distance < goal_distance:
            goal_distance = cell_distance
            goal = (x, y)

    return goal





