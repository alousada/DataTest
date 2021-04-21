# installing the necessary packages

import pip
package_names=['pyfiglet'] #packages to install
pip.main(['install'] + package_names + ['--upgrade']) 


import os
import time
import math
import random as rnd
import json
from pyfiglet import Figlet

from abalone.grid import AbaloneGrid
import abalone.config as config

import abalone.ai.AI as ai
import abalone.ai.TT as tt
import abalone.ai.mcts as mcts
from timeit import default_timer as timer

#human movement
def human_black():
    pass

#main code
custom_fig = Figlet(font='big')
print(custom_fig.renderText('Abalone Engine'))
user = input("Check best possible move or hit enter for simulation (AI vs AI): ")

if user != "":
    state = None
    with open(user) as json_file:  
        state = json.load(json_file)
    
    state[True] = state['true']
    del state['true']
    state[False] = state['false']
    del state['false']

    for key in state:
        for idx, block in enumerate(state[key]):
            state[key][idx] = tuple(block)

    # Initialize the grid
    initial_position = config.initialize(state)
    grid = AbaloneGrid(initial_position)
    
    print("Loading state: ", state)
    print("\nState loaded\n")
    print(grid.display)
    
    player = input("\nEnter player to move [w/b]: ")
    if player == "w":
        player = True
    else:
        player = False
    
    print("\nGenerating best move...\n")

    # Find best move
    tt.initialize_keys()
    _, move = tt.pvs(grid, player, -math.inf, math.inf, 5)
    grid.move(move[0], move[1])

    print(grid.display)
    print(move, "\n")
elif user == "":

    looping = True
    while looping:
        
        choose_depth = int(input ("Level of difficulty for AI from 1 to 5?"))

        black_score = 0
        white_score = 0
        iterations = 0
        accum_node_count = 0
        node_count = 0
        depth = choose_depth
        simulations = 1
        tt.table = {}
        rnd.seed(4106)

        # Initialize the grid with the 'mini' opening
        loop_=True
        while loop_:
            init_board = input("Do you want the (M)ini or (S)tandard version of Abalone?")

            if init_board == "M" or init_board == "m":
                init_board="mini"
                loop_=False
            elif init_board == "S" or init_board == "s":
                init_board="standard"
                loop_=False
            else:
                loop_=True

        initial_position = config.initialize(init_board)
        grid = AbaloneGrid(initial_position)

        print("Black will play as Random AI.\n")
        choice = print("Select an algorithm for White:\n(1) MiniMax \n(2) Alpha-Beta")
        alg = input("\nSelect a number: ")
        print("__________________________________________")
        print("\n White: ", white_score, "\t\tBlack: ", black_score)
        print("__________________________________________\n\n")
        print(grid.display)
        print("\n")
        
        for i in range(3,0,-1):
            print("Simulating game in ", i, "...")    
            time.sleep(1)

        ###### GAME START ######
        start = time.time()
        while True:
            ################## Black ####################
            # move
            curr_white = grid.query.marbles(grid.WHITE, True)
            moves = list(grid.moves(grid.BLACK, rnd=True, seed=rnd.seed))
            block, direction = moves[rnd.randint(0, len(moves) - 1)]
            grid.move(block, direction)

            # output
            print("__________________________________________")
            print("\n White: ", white_score, "\t\tBlack: ", black_score)
            print("__________________________________________\n")
            print("Iteration: ", iterations, "\n")
            print(grid.display)
            print("__________________________________________")
            print("\nBlack move: ", (block, direction))
            print("__________________________________________\n\n")
            print(f"Type block var: {type(block)}")
        
            
            # check win
            if grid.query.check_win(grid.BLACK):
                print("Black wins!")
                print("Time taken: ", time.time() - start)
                print("______________________________________\n\n")
                tt.output()
                break

            # update score
            black_score += curr_white - grid.query.marbles(grid.WHITE, True)
            curr_white = grid.query.marbles(grid.WHITE, True)
            ###############################################

            ################## White ####################
            # move
            move = None
            curr_black = grid.query.marbles(grid.BLACK, True)
            if alg == "1":
                _, move = ai.minimax(grid, depth, grid.WHITE)
                accum_node_count += ai.node_count
                node_count = ai.node_count
            elif alg == "2":
                _, move = ai.alphabeta(grid, depth, grid.WHITE, -math.inf, math.inf)
                accum_node_count += ai.node_count
                node_count = ai.node_count
            
            print (f"move zero {type(move[0])}")
            
            print (f"move um {type(move[1])}")

            grid.move(move[0], move[1])
        
            # output
            print("__________________________________________")
            print("\n White: ", white_score, "\t\tBlack: ", black_score)
            print("__________________________________________\n")
            print("Iteration: ", iterations, "\n")
            print(grid.display)
            print("______________________________________")
            print("\nWhite move: ", move, sep="")
            print("[ Nodes visited: ", node_count, "]")
            print("______________________________________\n\n")
            node_count = 0
            ai.node_count = 0
            tt.node_count = 0
            print("\n")
            
            # check win
            if grid.query.check_win(grid.WHITE):
                print("White wins!")
                print("Time taken: ", time.time() - start)
                print("Accumulated Nodes: ", accum_node_count)
                print("______________________________________\n\n")
                tt.output()
                break
            
            # update score
            white_score += curr_black - grid.query.marbles(grid.BLACK, True)
            curr_black = grid.query.marbles(grid.BLACK, True)

            iterations += 1
        ###############################################

