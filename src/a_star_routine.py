import sys
import time
from client import DroidClient
from a_star import A_star
import maneuver
from search_and_games import find_path


G = [[False, False, False, False, False],
     [False, False, True, False, True],
     [False, True, False, False, False],
     [False, False, False, True, False],
     [True, False, False, False, False],
     [False, False, True, False, False],
     [True, False, False, False, False],
     [False, False, False, False, False]]


# connect to Sphero
droid = DroidClient()
droid.scan()
droid.connect_to_droid('D2-6F8D')
# droid.connect_to_R2D2()

enemy = DroidClient()
enemy.scan()
enemy.connect_to_droid('Q5-8CC0')




# get course, find path
#G = courses.grid_1
agent_pos = (0, 0)
enemy_pos = (7, 2)
goal = (7, 4)

G[agent_pos[0]][agent_pos[1]] = True
G[enemy_pos[0]][enemy_pos[1]] = True

#path = A_star(G, start, goal)


# ☑ =start node, ☒ =goal node
# ☐ ══☐   ☐ ══☐
# ║   ║   ║   ║
# ☐   ☐ ══☐   ☐
# ║   ║   ║   ║
# ☐ ══☐   ☐ ══☐
# ║       ║   ║
# ☑   ☐ ══☐   ☒



# enemy1_bound = (5, 6)
# enemy2 = (4, 4)
# enemy2_bound = (3, 4)
speed = 0x88
while True:


    #  AGENT
    path = find_path(agent_pos, goal, G)
    maneuver.follow_path(droid, path[0:2])

    print(path)

    v1 = path[0]
    v2 = path[1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True
    agent_pos = path[1]

    print(G)

    # BAD DROID 1
    path = find_path(enemy_pos, agent_pos, G)
    print(path)
    maneuver.follow_path(enemy, path[0:2])


    v1 = path[0]
    v2 = path[1]
    G[v1[0]][v1[1]] = False
    G[v2[0]][v2[1]] = True
    enemy_pos = path[1]

    print(G)


    # BAD DROID 2
    # enem = find_path(enemy2, goal, G)
    # path =  path[0:2]
    # maneuver.follow_path(bad_droid_2, [enemy3, dest3], speed, scale_dist = 1)
    # enemy2 = dest2
