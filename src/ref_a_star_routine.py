import sys
import time
from collections import defaultdict
# Custom Imports
from Warrior import Warrior
from game_helpers import good_droid_turn, bad_droid_turn, initialize_game_start_parameters
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
            droid_start = (int(line[1]),int(line[2]))
            droid_morality = True

            if line[3] == 'Bad':
                droid_morality = False
            droid = Warrior(droid_name, droid_start, droid_morality, debug_mode)
            droid_list.append(droid)

        return droid_list

def sort_arguments(args):
    print(args)
    print('done args')
    ## Graph Construction
    G = load_gameboard(args.gameboard)

    ## Set Up Agents
    droid_list = load_droids(args.droids, args.debug)

    #Finalize game board with droid locations
    for droid in droid_list:
        droid_start = droid.get_location()
        G[droid_start[0]][droid_start[1]] = True

    initialize_game_start_parameters(G, args.speed_boost_chance, args.airstrike_probabilities, args.debug)

    return G, droid_list

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('gameboard', help='Filepath of the file specifying the game board grid.')
    parser.add_argument('droids', help="""Filepath of the file specifying the droids playing in the game. Each line in the 
        file should pertain to 1 droid in the game and contain 4 values seperated by spaces: droid name, start row, start column, and droid morality. 
        ex: D2-0709 0 0 Good""")
    parser.add_argument('-d','--debug', help='Turn on debug mode. The game will not connect to the droids.', action = "store_true")
    parser.add_argument('-t','--turn_order', help='Specify the turn order of the droids. Defaults to the order they are presented in droid_list.')
    parser.add_argument('-sb','--speed_boost_chance', help='Specify the probability with which the droids will receive a speed boost at the start of their turn (Default = 0.25)', type=float, default=0.25)
    parser.add_argument('-as','--airstrike_probabilities', help='Specify the probability with which the bad droids will call in an airstrike at the start of their turn (Default = 0.20) and the probability with which an airstrike will hit a good droid (Default = 0.25).', nargs=2, type=float, default=[0.2,0.25])
    args = parser.parse_args()

    G, droid_list = sort_arguments(args)


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
