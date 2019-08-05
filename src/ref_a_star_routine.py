import sys
import time
from collections import defaultdict
# Custom Imports
from Warrior import Warrior
from game_helpers import good_droid_turn, bad_droid_turn

def print_graph(G):
    for row in G:
        print(row)

# -- Initialize game
# Footbal field: 8 x 5
#
# Each box is a vertex
#
#       ------ ☐ ------
#       ☐══☐══☐══☐══☐══☐
#       ║           ║  ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║           ║  ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║     ║     ║  ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║     ║        ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║     ║        ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║              ║
#       ☐  ☐══☐══☐══☐══☐
#       ║              ║
#       ☐══☐══☐  ☐  ☐  ☐
#       ║
# (0,0) ☐══☐══☐══☐══☐══☐
# --- start ---

def main():
    game_over = False

    ## Graph Construction

    G = [[False, False, False, False, False],
         [False, False, True, False, True],
         [False, True, False, False, False],
         [False, False, False, True, False],
         [False, False, False, False, False],
         [False, False, True, False, False],
         [True, False, False, False, False],
         [False, False, False, False, False]]



    goal = (7, 4)
    #goal = (4, 3)
    ## Set Up Agents
    agent1_pos = (0, 1)
    agent2_pos= (0, 2)


    enemy_pos = (7, 4)
    enemy2_pos = (7, 1)

    good_agent1 = Warrior("D2-84FA", agent1_pos, True)
    good_agent2 = Warrior("D2-0709", agent2_pos, True)

    bad_agent1 = Warrior("D2-6F8D", enemy_pos, False)
    bad_agent2 = Warrior("D2-5A22", enemy2_pos, False)

    agents = [good_agent1, bad_agent1, good_agent2, bad_agent2]

    G[agent1_pos[0]][agent1_pos[1]] = True
    G[agent2_pos[0]][agent2_pos[1]] = True
    G[enemy_pos[0]][enemy_pos[1]] = True
    G[enemy2_pos[0]][enemy2_pos[1]] = True


    print("Game start!")

    while True:

        for agent in agents:
            if game_over:
                print("----- ENDING GAME -------")
                return

            if agent.get_is_good():
                game_over = good_droid_turn(agent, G, agents)
                print_graph(G)
            else:
                print('trying bad droid turn')
                game_over = bad_droid_turn(agent, G, agents)
                print_graph(G)


if __name__ == '__main__':
    main()
