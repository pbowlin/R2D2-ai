import sys
import time
from collections import defaultdict
# Custom Imports
from Warrior import Warrior
from game_helpers import good_droid_turn, bad_droid_turn, generate_EMP_locations
import argparse
import csv

def load_gameboard(gameboard_file):
    G = []
    with open(gameboard_file) as file:
        reader = csv.reader(file)
        for line in reader:
            G_row = []
            for string in line:
                for char in string:
                    if char == 'X':
                        G_row.append(True)
                    elif char == '.':
                        G_row.append(False)
            G.append(G_row)
        return G

def load_droids(droid_file, debug_mode):
    with open(droid_file) as file:
        reader = csv.reader(file, delimiter=' ')
        droid_list = []
        for line in reader:
            droid_name = line[0]
            droid_start = (int(line[1][1]),int(line[1][3]))
            droid_morality = True

            if line[2] == 'Bad':
                droid_morality = False
            droid = Warrior(droid_name, droid_start, droid_morality, debug_mode)
            droid_list.append(droid)

        return droid_list


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('gameboard', help='Filepath of the file specifying the game board grid.')
    parser.add_argument('droids', help="""Filepath of the file specifying the droids playing in the game. Each line in the 
        file should pertain to 1 droid in the game and contain 3 values seperated by spaces: droid name, starting position, and droid morality. 
        ex: D2-0709 (0,0) Good, Q5-8CC0 (7,4) Bad""")
    parser.add_argument('-d','--debug', help='Turn on debug mode. The game will not connect to the droids.', action = "store_true")
    parser.add_argument('-t','--turn_order', help='Specify the turn order of the droids. Defaults to the order they are presented in droid_list.')
    parser.add_argument('-sb','--speed_boost_chance', help='Specify the probability with which the droids will receive a speed boost at the start of their turn. Default = 0.25.')
    parser.add_argument('-as','--airstrike_chance', help='Specify the probability with which the bad droids will receive call in an airstrike at the start of their turn. Default = 0.20.')
    args = parser.parse_args()

    ## Graph Construction
    G = load_gameboard(args.gameboard)

    ## Set Up Agents
    droid_list = load_droids(args.droids, args.debug)

    #Finalize game board with droid locations
    for droid in droid_list:
        droid_start = droid.get_location()
        G[droid_start[0]][droid_start[1]] = True

    generate_EMP_locations(G)


    print("Game start!")
    game_over = False

    while True:

        for agent in droid_list:
            if game_over:
                print("----- ENDING GAME -------")
                return

            if agent.get_is_good():
                print()
                print('Trying good droid turn')
                game_over = good_droid_turn(agent, G, droid_list)
                #print_graph(G)
            else:
                print()
                print('Trying bad droid turn')
                game_over = bad_droid_turn(agent, G, droid_list)
                #print_graph(G)


if __name__ == '__main__':
    main()
