############################################################
# CIS 521: Homework 2
############################################################

student_name = "Peter Bowlin"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import math

############################################################
# Section 1: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self._board = board

    def get_board(self):
        return self._board

    def perform_move(self, row, col):
        if not self._is_valid_square(row, col):
          print('Invalid move - Square is outside the bounds of the board.')
          return
        
        neighbor_offsets = [[0,0],[-1,0],[1,0],[0,-1],[0,1]]

        for x in neighbor_offsets:
          if self._is_valid_square(row+x[0], col+x[1]):
            self._board[row+x[0]][col+x[1]] = not self._board[row+x[0]][col+x[1]]
        
    def _is_valid_square(self,row, col):
        board = self.get_board()
        
        if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
          return False
        return True


    def scramble(self):
        board_coordinates = self._generate_board_coordinates()
        random.shuffle(board_coordinates)

        for x in board_coordinates:
          if random.random() < 0.5:
            self.perform_move(x[0],x[1])

    def is_solved(self):
        board = self.get_board()
        
        for x in board:
          for y in range(len(board[0])): 
            if x[y] == True:
              return False

        return True


    def copy(self):
        board = self.get_board()

        copied_board = [[x for x in i] for i in board]
        return LightsOutPuzzle(copied_board)

    def successors(self):
        board_coordinates = self._generate_board_coordinates()

        for x in board_coordinates:
          new_puzzle = self.copy()
          new_puzzle.perform_move(x[0],x[1])

          yield (x, new_puzzle)


    def find_solution(self):
        solution = []

        if self.is_solved():
          print('The puzzle is already solved!')
          return solution

        root_node = Node(self)
        frontier = [root_node]
        visited_boards = set()

        while len(frontier) != 0:
          current_node = frontier.pop(0)
          current_game = current_node.get_node()
          successors = current_game.successors()
          
          for action, successor in successors:
            if successor.is_solved():
              solution.append(action)
              
              while current_node.get_parent() != None:
                solution.insert(0,current_node.get_action())
                current_node = current_node.get_parent()

              return solution

            board_state = successor._tuplefy_game_board(successor.get_board())

            if board_state not in visited_boards:
              visited_boards.add(board_state)
              new_node = Node(successor, current_node, action, 1)
              frontier.append(new_node)

        return None

    def _generate_board_coordinates(self):
        board = self.get_board()
        rows = len(board)
        cols = len(board[0])
        board_coordinates = [(i,j) for i in range(rows) for j in range(cols)]
        return board_coordinates

    def _tuplefy_game_board(self, board):
        return tuple(tuple(x) for x in board)

def create_puzzle(rows, cols):
    board = [[False for col in range(cols)] for row in range(rows)]
    return LightsOutPuzzle(board)

####################################################################
class Node:
    def __init__(self, node, parent = None, action = None, cost = 0):
        self._node = node
        self._parent = parent
        self._cost = cost
        if parent:
          self._action = action
          self._depth = parent.get_depth() + 1
        else:
          self._depth = 0
        
    def get_node(self):
      return self._node 

    def get_parent(self):
      return self._parent

    def set_parent(self, new_parent):
      self._parent = new_parent

    def adopt_children(self, children):
      self._children = children 

    def get_children(self):
      return self._children

    def get_action(self):
      return self._action

    def get_cost(self):
      return self._cost

    def set_cost(self, new_cost):
      self._cost = new_cost

    def get_depth(self):
      return self._depth
####################################################################

############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):

    print(start)
    print(goal)
    #if _is_obstacle(start, scene) or _is_obstacle(goal, scene):
      #print(start), print(goal)
      #print('Cant have the start or goal positions be on an obstacle.')
      #return None

    solution = []
    frontier = [Node(start, cost = _calculate_SLD(start, goal))]
    visited = set()

    while len(frontier) != 0:
          current_node = frontier.pop(frontier.index(min(frontier, key = lambda x : x.get_cost())))
          visited.add(current_node.get_node())
          
          if current_node.get_node() == goal:
            while current_node != None:
                solution.insert(0,current_node.get_node())
                current_node = current_node.get_parent()

            return solution

          current_node_SLD = _calculate_SLD(current_node.get_node(),goal)      
          neighbors = _get_neighbors(current_node.get_node(), scene, goal)
          
          for neighbor in neighbors:
            if neighbor not in visited:
              SLD = _calculate_SLD(neighbor, goal)
              cost = current_node.get_cost() - current_node_SLD + _calculate_SLD(current_node.get_node(),neighbor) + SLD
              node_matched = False
              
              for node in frontier:
                if node.get_node() == neighbor:
                  node_matched = True
                  if cost < node.get_cost():
                    node.set_cost(cost)
                    node.set_parent(current_node)
                  break
              
              if not node_matched:
                new_node = Node(neighbor, parent = current_node, cost = cost)
                frontier.append(new_node)

    return None

def _is_obstacle(node, scene, goal):
    if node[0] < 0 or node[0] >= len(scene):
      return True

    if node[1] < 0 or node[1] >= len(scene[0]):
      return True 

    if node[0] == goal[0] and node[1] == goal[1]:
        return False

    return scene[node[0]][node[1]]

def _get_neighbors(node, scene, goal):
    neighbors = []
    #neighbor_offsets = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    neighbor_offsets = [[-1,0],[0,-1],[0,1],[1,0]]

    for offset in neighbor_offsets:
      neighbor_node = (node[0] + offset[0], node[1] + offset[1])

      if not _is_obstacle(neighbor_node, scene, goal):
        neighbors.append(neighbor_node)

    return neighbors

def _calculate_SLD(current_node, goal):
    a = (goal[0] - current_node[0])
    b = (goal[1] - current_node[1])

    return (a**2 + b**2)**0.5



############################################################
# Section 3: Dominoes Games
############################################################

def create_dominoes_game(rows, cols):
    pass

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self._board = board
        self._rows = len(board)
        self._cols = len(board[0])

    def get_board(self):
        return self._board

    def reset(self):
        self._board = [[False for col in range(self._cols)] for row in range(self._rows)]

    def is_legal_move(self, row, col, vertical):
        r_offset, c_offset  = self.get_move_offsets(vertical)

        if row < 0 or row + r_offset >= self._rows:
          return False
        if col < 0 or col + c_offset >= self._cols:
          return False
        if self._board[row][col] or self._board[row + r_offset][col + c_offset]:
          return False

        return True

    def legal_moves(self, vertical):
        r_offset, c_offset  = self.get_move_offsets(vertical)

        for row in range(self._rows - r_offset):
          for col in range(self._cols - c_offset):
            if self.is_legal_move(row, col, vertical):
              yield (row, col)


    def perform_move(self, row, col, vertical):
        r_offset, c_offset  = self.get_move_offsets(vertical)

        if self.is_legal_move(row, col, vertical):
          self._board[row][col] = True
          self._board[row + r_offset][col + c_offset] = True
        else:
          print('Illegal move')

    def game_over(self, vertical):
        if not next(self.legal_moves(vertical),False):
          return True
        else:
          return False


    def copy(self):
        board = self.get_board()

        copied_board = [[x for x in i] for i in board]
        return DominoesGame(copied_board)

    def successors(self, vertical):
        legal_moves = list(self.legal_moves(vertical))

        for x in legal_moves:
          successor = self.copy()
          successor.perform_move(x[0],x[1], vertical)

          yield (x, successor)

    def get_random_move(self, vertical):
        legal_moves = list(self.legal_moves(vertical))

        return random.choice(legal_moves)

    def get_best_move(self, vertical, limit):
        v = self._get_max_value(vertical, limit, -math.inf, math.inf)

        return v

    def get_move_offsets(self, vertical):
      if vertical:
        return 1,0
      else:
        return 0,1

    def _get_max_value(self,vertical, limit, alpha, beta):
      recommended_action = None
      leaf_count = 0
      if limit == 0 or self.game_over(vertical):
        return recommended_action, self._calculate_heuristic(vertical), leaf_count + 1
      v = -math.inf

      for action, state in self.successors(vertical):
        result, leaves = state._get_min_value(vertical, limit - 1, alpha, beta)
        leaf_count += leaves
        v = max(v, result)
        if v >= beta:
          return recommended_action, v, leaf_count
        if v > alpha:
          recommended_action = action
          alpha = v
      return recommended_action, v, leaf_count


    def _get_min_value(self, vertical, limit, alpha, beta):
      leaf_count = 0
      if limit == 0 or self.game_over(not vertical):
        return self._calculate_heuristic(vertical), leaf_count + 1
      v = math.inf

      for action, state in self.successors(not vertical):
        r_action, result, leaves = state._get_max_value(vertical, limit - 1, alpha, beta)
        leaf_count += leaves
        v = min(v, result)
        if v <= alpha:
          return v, leaf_count
        beta = min(beta, v)
      return v, leaf_count
     
    def _calculate_heuristic(self, vertical):
      return len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical)))

def create_dominoes_game(rows, cols):
    board = [[False for col in range(cols)] for row in range(rows)]
    return DominoesGame(board)

