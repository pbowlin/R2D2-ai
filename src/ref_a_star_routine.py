import sys
import time
from collections import defaultdict
# Custom Imports
from Warrior import Warrior
from game_helpers import good_droid_turn, bad_droid_turn, generate_EMP_locations


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



    ## Set Up Agents
    '''
    agent1_pos = (0, 0)
    agent2_pos= (0, 4)


    enemy_pos = (7, 4)
    enemy2_pos = (7, 0)
    '''
    agent1_pos = (0, 2)
    agent2_pos= (4, 2)


    enemy_pos = (6, 2)
    enemy2_pos = (7, 2)
    


    # if True, robots don't move
    debug_mode = True

    good_agent1 = Warrior("D2-84FA", agent1_pos, True, debug_mode)
    good_agent2 = Warrior("D2-0709", agent2_pos, True, debug_mode)

    bad_agent1 = Warrior("D2-6F8D", enemy_pos, False, debug_mode)
    bad_agent2 = Warrior("Q5-A9B7", enemy2_pos, False, debug_mode)


    agents = [good_agent1, bad_agent1, good_agent2, bad_agent2]

    G[agent1_pos[0]][agent1_pos[1]] = True
    G[agent2_pos[0]][agent2_pos[1]] = True
    G[enemy_pos[0]][enemy_pos[1]] = True
    G[enemy2_pos[0]][enemy2_pos[1]] = True

    generate_EMP_locations(G)


    print("Game start!")

    while True:

        for agent in agents:
            if game_over:
                print("----- ENDING GAME -------")
                return

            if agent.get_is_good():
                print()
                print('Trying good droid turn')
                game_over = good_droid_turn(agent, G, agents)
                #print_graph(G)
            else:
                print()
                print('Trying bad droid turn')
                game_over = bad_droid_turn(agent, G, agents)
                #print_graph(G)


if __name__ == '__main__':
    main()
