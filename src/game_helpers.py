import random, math
from maneuver import follow_path
from a_star import A_star
from sound import play_airstrike
from search_and_games import find_path

speed_boost_chance = 0.0
call_airstrike_prob = 0.2
EMP_locations = []

def good_droid_turn(droid, G, warriors):
    print("Good droid at {} attempting its turn".format(droid.get_location()))
    if not (droid.get_is_alive()):
        print("GOOD AGENT IS DESTROYED!")
        # TODO: droid falls over
        return end_turn_and_print(G, False, warriors)

    goals = find_good_droid_goals(G, droid.get_location())
    path = None

    for goal in goals:
        droid_in_goal = False
        for w in warriors:
            if goal == w.get_location():
                droid_in_goal = True
                break
        if not droid_in_goal:
            print('good droid attempted goal: ' + str(goal))

            ## UPDATE DROID POSITION
            path = find_path(droid.get_location(), goal, G)
            if path:
                break

    if not path:
        print("NO PATH FOR GOOD DROID") ##GAME SHOULD NOT END IF 2 GOOD DROIDS
        return end_turn_and_print(G, False, warriors)

    path = get_path(droid, path)
    
    if not droid.debug:
        follow_path(droid, path)

    ## UPDATE GRID STATE
    #v1 = path[0]
    #v2 = path[-1]
    #G[v1[0]][v1[1]] = False
    #G[v2[0]][v2[1]] = True
    #agent_pos = path[1]
    update_grid_state(G, path)
    check_for_EMP(droid)

    ## POST UPDATE ACTIONS
    droid_location = droid.get_location()
    if droid_location[0] > len(G) - 2:
    #if droid in goal:
        print("YOU WON")
        if not droid.debug:
            droid.droid_client.animate(3, 0) # chirping Sound
        # TODO: headspin
        return end_turn_and_print(G, True, warriors)
    else:
        dist, bad_droid = get_nearest_opponent(droid.get_location(), droid, warriors)
        if 1 < dist < 2:
            if droid.EMPs > 0:
                launch_EMP(droid, bad_droid)

    return end_turn_and_print(G, False, warriors)

def launch_EMP(droid, bad_guy):
    print('Launching EMP')
    bad_guy.set_is_active(False)
    print('bad guy now inactive')
    if not bad_guy.debug:
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
    
    print("Attempting to hit good droid at {}".format(agent_to_attack.get_location()))
    play_airstrike()

    if random.random() <= prob_airstrike_hit:
        if not agent_to_attack.debug:
            agent_to_attack.droid_client.animate(14, 0) ##fall over and die
        agent_to_attack.set_is_alive(False)
        good_living_agents.remove(agent_to_attack)
        print("AIRSTRIKE HIT")
        if len(good_living_agents) == 0:
            if not bad_agents[0].debug:
                bad_agents[0].droid_client.animate(3,0)
                bad_agents[1].droid_client.animate(3,0)
            return True ##this means the airstrike killed last living good agent
    else:
        print("AIRSTRIKE MISS")
        if not agent_to_attack.debug:
            agent_to_attack.droid_client.animate(7, 0) ##airstrike missed target
    return False

def bad_droid_turn(droid, G, warriors):
    print("Bad droid at {} attempting its turn".format(droid.get_location()))
    # Skip Droid's Turn
    if not droid.get_is_active():
        print('droid is inactive')
        droid.set_is_active(True)
        return end_turn_and_print(G, False, warriors)

    if random.random() <= call_airstrike_prob:
        print('Bad droid at {} called air strike'.format(droid.get_location()))
        if call_airstrike(warriors):
            return end_turn_and_print(G, True, warriors) ## this means the airstrike killed the last living good_agent

    ## UPDATE DROID POSITION
    dist, closest_droid = get_nearest_opponent(droid.get_location(), droid, warriors)
    # TODO: UPDATE LOGIC FOR SETTING DROID GOAL

    bad_droid_goal = find_bad_droid_goal(G, closest_droid.get_location())

    path = find_path(droid.get_location(), bad_droid_goal, G)

    print('path is:' + str(path))
    path = get_path(droid, path)
    if not path:
        print("NO PATH FOR BAD DROID")  ##GAME SHOULD NOT END IF WE HAVE 2 BAD DROIDS
        return end_turn_and_print(G, False, warriors)
    
    if not droid.debug:
        follow_path(droid, path)

    ## UPDATE GRID STATE
    #v1 = path[0]
    #v2 = path[-1]
    #G[v1[0]][v1[1]] = False
    #G[v2[0]][v2[1]] = True
    #enemy_pos = path[1]
    update_grid_state(G, path)

    # TODO: POST UPDATE ACTIONS
    return end_turn_and_print(G, False, warriors)

def got_speed_boost():
    return (random.random() < speed_boost_chance)

# Get nearest opponent of the agent
def get_nearest_opponent(location, agent, warriors):
    d_min = math.inf
    opponent = None
    for w in warriors:
        if w.get_is_good() is not agent.get_is_good() and w.get_is_alive():
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

def find_good_droid_goals(G, location):
    
    goals_and_distance = []
    #goal_distance = 1000000
    x = len(G)-1 #Good droids are always trying to get to the far side of the grid
    #goal = (x, 0)

    for y in range(len(G[-1])):
        cell_distance = compute_distance(location, (x, y))
        #if cell_distance < goal_distance:
            #goal_distance = cell_distance
            #goal = (x, y)
        goals_and_distance.append(((x,y),cell_distance))

    goals_and_distance.sort(key=lambda x: x[1])

    goals = [x[0] for x in goals_and_distance]

    return goals

def update_grid_state(G, path):
    v1 = path[0]
    v2 = path[-1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True

def generate_EMP_locations(G):
    grid_cell_per_EMP = 20
    grid_size = sum(len(row) for row in G)
    num_EMPs_to_place = int(grid_size/grid_cell_per_EMP)

    i = 0
    while i < num_EMPs_to_place:
        x = random.choice(range(1, len(G)-1))
        y = random.choice(range(len(G[0])))

        if not G[x][y] and (x,y) not in EMP_locations:
            i += 1
            EMP_locations.append((x,y))

def check_for_EMP(droid):
    found_EMP = False
    for EMP in EMP_locations:
        if EMP == droid.get_location():
            print("Droid found an EMP on the battlefield!")
            droid.EMPs += 1
            found_EMP = True
            break

    if found_EMP:
        EMP_locations.remove(droid.get_location())


def end_turn_and_print(G, game_over, warriors):
    print('  ', end = '')
    for y in range(len(G[0])):
        print('{} '.format(y), end = '')

    print()
    for row in range(len(G)):
        print ('{} '.format(row), end = '')
        for col in range(len(G[0])):
            printed = False
            for warrior in warriors:
                if warrior.get_location() == (row, col):
                    printed = True
                    if warrior.get_is_good():
                        print('G ', end = '')
                    else:
                        print('B ', end = '')
                    break

            if not printed:
                for EMP in EMP_locations:
                    if EMP == (row, col):
                        print('E ', end = '')
                        printed = True
                        break
            if not printed:
                if G[row][col]:
                    print('X ', end = '')
                else:
                    print('. ', end = '')
        print()

    return game_over



