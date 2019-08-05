import sys
import time
from graph import Graph
from collections import defaultdict
# Custom Imports
from Warrior import Warrior
from game_helpers import good_droid_turn, bad_droid_turn

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
         [True, False, False, False, False],
         [False, False, True, False, False],
         [True, False, False, False, False],
         [False, False, False, False, False]]



    goal = (7, 4)
    ## Set Up Agents
    agent_pos = (0, 0)
    enemy_pos = (7, 2)
    good_agent1 = Warrior("D2-6F8D", (0, 0), True)
    bad_agent1 = Warrior("Q5-8CC0", (7, 2), False)
    agents = [good_agent1, bad_agent1]

    G[agent_pos[0]][agent_pos[1]] = True
    G[enemy_pos[0]][enemy_pos[1]] = True

    print("Game start!")

    while True:

        for agent in agents:
            if game_over:
                print("----- ENDING GAME -------")
                return

            if agent.get_is_good():
                game_over = good_droid_turn(agent, G, agents, goal)
                print(G)
            else:
                game_over = bad_droid_turn(agent, G, agents)
                print(G)


if __name__ == '__main__':
    main()
