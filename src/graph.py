from itertools import product
from collections import defaultdict
from client import DroidClient
from a_star import A_star
import math
import random

class Graph:
    def __init__(self, obstacles, agent_positions = {}, row = 8, col = 5, debug=False):
        self.row = row
        self.col = col
        self.debug = debug # If true, robots don't actually move
        self.V = list(product(range(self.row), range(self.col)))

        #dDictionary of { vertiex : set(vertices) }
        self.neighborhood = defaultdict(set)

        # list of agent names
        self.agent_names = agent_positions.keys()

        # dictionary of { droid_name : (vertex_x, vertex_y) }
        self.agent_positions = agent_positions

        # dictionaryu of { droid_name : DroidClient }
        self.agent_droidclient = dict()

        # Create grid
        offsets = ((1,0), (0,1), (-1, 0), (0, -1))
        E = []
        for u_x in range(self.col):
            for u_y in range(self.row):
                for offset_row, offset_col in offsets:
                    v_x, v_y = (u_x + offset_row, u_y + offset_col)
                    # Check if both vertices are within grid bounds AND
                    # if either direction u-> or v->u have been intialized as obstacles
                    if (0 <= u_x < self.col and 0 <= u_y < self.row and
                        0 <= v_x < self.col and 0 <= v_y < self.row and
                        not (obstacles[(u_x, u_y), (v_x, v_y)] or \
                            obstacles[(v_x, v_y), (u_x, u_y)])):
                        E.append(
                            ((u_x, u_y), (v_x, v_y))
                        )

        # Update neighborhood. This is used to check for obstacles and updated for changes
        for (u,v) in E:
            self.neighborhood[u].add(v)
            self.neighborhood[v].add(u) # assumes undirected graph

        # # Update the neighborhood based on agents
        # for agent_name in self.agent_names:
        #     self.update_neighbors(None, self.get_agent_position(agent_name))

    # Agent methods
    def get_agents(self):
        """Return all agent by name"""
        return self.agent_names

    def get_agent_position(self, agent_name):
        """Return the agent's position by name"""
        return self.agent_positions[agent_name]

    def get_agent_droidclient(self, agent_name):
        """Return droid client for the agent"""
        return self.agent_droidclient[agent_name]

    def update_agent_position(self, agent_name, new_pos):
        self.agent_positions[agent_name] = new_pos
        return None

    # Grid State methods
    def is_edge_blocked(self, u, v):
        """
        Returns true if the edge between vertices u and v is
        blocked. Edge blocked status is always bi-drectional: u -> v and v -> u
        No agent should be able to cross if the edge
        is blocked, from either directions u -> v or v -> u.
        """
        return (v not in self.get_neighbors(u)) or \
            (u not in self.get_neighbors(v))

    def get_neighbors(self, u):
        """
        Return set of vertices ((x1,y1), (x2,y2), ...)
        that any agent can travel to from u
        """
        return self.neighborhood[u]

    def update_neighbors(self, v_to_free, v_to_block):
        """Block & unblock the specified edges bewteen verticies.
        v_to_free: *allow* all of it's *current* neighbors to v
        v_to_bloc: *block* all of it's *current* neighbors to v
        """
        # TODO: ??

        # neighbors_to_block = list() if v_to_block is None else list(self.get_neighbors(v_to_block))
        # neighbors_to_free = list() if v_to_free is None else list(self.get_neighbors(v_to_free))

        # # add new obstacles
        # for neighbor in neighbors_to_block:
        #     self.neighborhood[neighbor].remove(v_to_block)
        #     self.neighborhood[v_to_block].remove(neighbor)

        # # delete old obstacles and recover as new_edge
        # for neighbor in neighbors_to_free:
        #     self.neighborhood[neighbor].add(v_to_free)
        #     self.neighborhood[v_to_free].add(neighbor)

    def dist_between(self, u, v):
        """Distance between vertices."""
        if v not in self.get_neighbors(u):
            return None
        return 1 # assumes unweighted graph

    def move_agent(self, agent_name, path):
        """Move agent_name by path of size 2"""
        print("move {0}: {1}".format(agent_name, path))

        x, y = path[0]
        new_x, new_y = path[1]

        # Update grid states
        # Update agent's position
        self.update_agent_position(agent_name, (new_x, new_y))

        # Update grid so that old position (x,y) is now available for move into
        # while new position is not available into
        self.update_neighbors((x,y), (new_x, new_y))

        # Physically move robot
        if not self.debug:
            self.follow_path(
                droid_client = self.get_agent_droidclient(agent_name),
                path = [(x,y), (new_x, new_y)]
            )


    def print(self):
        """Print game grid to terminal. For debugging / terminal game play"""
        position_agent = {position: agent for agent, position in self.agent_positions.items()}

        neighbor_width = "        "
        obstacle_width = " ------ "
        bottom = [obstacle_width] * self.col

        print("#" * self.col * 8)
        print(" " + "".join(bottom))
        for y in range(self.row-1, -1, -1):
            bottom = []
            for x in range(self.col):
                cell = str((x,y)) #+ " " # extra space to line up with droid name
                if (x,y) in position_agent:
                    cell = position_agent[(x,y)]
                    cell = cell.replace("-", "")

                bottom_border = obstacle_width
                left_border = "|" + (" " if x == 0 else "")
                right_border = (" " if x == (self.col - 1) else "") + "|"
                for valid_neighbor in self.get_neighbors((x,y)):
                    if (valid_neighbor[0] == (x - 1)):
                        left_border = " "
                    elif (valid_neighbor[0] == (x + 1)):
                        right_border = " "
                    elif (not y == 0 and valid_neighbor[1] == (y - 1)):
                        bottom_border = neighbor_width
                bottom.append(bottom_border)
                print("{0}{1}{2}".format(
                    left_border, cell, right_border
                ), end = "")
            print("")
            print("|" + "".join(bottom) + "|")

        # End printing grid. Print final line
        print("#" * self.col * 8)
