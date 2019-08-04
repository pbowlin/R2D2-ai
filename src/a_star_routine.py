import sys
import time
from graph import Graph
from collections import defaultdict

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

obstacles = defaultdict(bool)
obstacle_edges = [
    ((0,0), (0,1)), ((1,0), (1,1)),
    ((1,1), (1,2)), ((2,1), (2,2)), ((3,1), (3,2)), ((4,1), (4,2)),
    ((1,3), (2,3)), ((1,4), (2,4)), ((1,5), (2,5)),
    ((3,5), (4,5)), ((3,6), (4,6)), ((3,7), (4,7))
]
for edges in obstacle_edges:
    obstacles[edges] = True


good_agent = "D2-0709"
bad_agents = ["D2-4D79", "D2-6F8D"]

G = Graph(
    obstacles = obstacles,
    agent_positions = {
        good_agent : (0,0),
        bad_agents[0] : (1,6), # horizontal
        bad_agents[1] : (0,3)  # veritcal
    },
    debug=False
)

goal = (4, 7)
print("Game start!")
G.print()

while True:
    if(G.agent_positions[good_agent] == goal):
        break

    # GOOD AGENT
    path_good_agent = G.get_agent_move(good_agent,
        strategy = "A_star",
        min_bound = G.get_agent_position(good_agent),
        max_bound = goal)
    G.move_agent(good_agent, path_good_agent)
    G.print()

    # BAD AGENTS
    path_bad_agent_0 = G.get_agent_move(bad_agents[0],
        strategy = "horizontal",
        min_bound = (1,6),
        max_bound = (3,6))
    G.move_agent(bad_agents[0], path_bad_agent_0)
    G.print()

    path_bad_agent_1 = G.get_agent_move(bad_agents[1],
        strategy = "vertical",
        min_bound = (0,3),
        max_bound = (0,7))
    G.move_agent(bad_agents[1], path_bad_agent_1)
    G.print()

