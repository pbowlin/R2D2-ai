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
    obstacles = defaultdict(bool)
    obstacle_edges = [
        ((0,0), (0,1)), ((1,0), (1,1)),
        ((1,1), (1,2)), ((2,1), (2,2)), ((3,1), (3,2)), ((4,1), (4,2)),
        ((1,3), (2,3)), ((1,4), (2,4)), ((1,5), (2,5)),
        ((3,5), (4,5)), ((3,6), (4,6)), ((3,7), (4,7))
    ]

    for edges in obstacle_edges:
        obstacles[edges] = True

    ## Set Up Agents

    good_agent = ["D2-0709"]
    bad_agent = [ "D2-6F8D"]

    good_agent1 = Warrior("D2-0709", (0, 0), True)
    # good_agent2 = Warrior('Q5-8CC0', (0, 4), True)

    bad_agent1 = Warrior("D2-6F8D", (6, 0), False)

    warriors = [good_agent1, bad_agent1]
    # bad_agent2 = Warrior("D2-6F8D", (6, 4), False)


    G = Graph(
        obstacles = obstacles,
        agent_positions = {
            good_agent[0] : (0,0),
            # good_agents[1]: (0,4),
            bad_agent[0] : (6,0)
            # bad_agents[1] : (0,3),  # veritcal
        },
        debug=False
    )

    goal = (4, 7)

    print("Game start!")
    G.print()

    while True:

        for warrior in warriors:
            if game_over:
                print("----- ENDING GAME -------")
                return

            if warrior.get_is_good():
                game_over = good_droid_turn(warrior, G, warriors, goal)
                G.print()
            else:
                game_over = bad_droid_turn(warrior, G, warriors)
                G.print()


if __name__ == '__main__':
    main()
