# Simple quintris program! v0.2
# D. Crandall, Sept 2021
# Used some functions from QuintrisGame.py file

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import random
from math import inf as infinity
import copy

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        # return random.choice("mnbh") * random.randint(1, 10)

        initial_board = quintris.get_board()
        depth = len(self.empty_cells(initial_board))

        # Call expectiminimax to get the nex move
        (score, moves) = self.expectiminimax(initial_board, depth,1,{},{})
        return moves

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)
            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))
            moves = self.get_moves(quintris)

            for i in range(len(moves)):
                if(moves[i]=='b'):
                    quintris.left()
                elif(moves[i]=='m'):
                    quintris.right()
                elif(moves[i]=='h'):
                    quintris.hflip()
                elif(moves[i]=='n'):
                    quintris.rotate()


    # Expectiminimax to get maximum score
    def expectiminimax(self,board, depth, player,state_dict,heur_dict):

        score = 0
        if(str(board) not in state_dict):

            # If depth (empty cells on board)<367 use the heuristic to get the score
            if(depth < 367):
                current_col = quintris.col
                piece = quintris.get_piece()[0]
                col= quintris.get_piece()[2]

                board_copy= copy.deepcopy(quintris.get_board())

                # Cache heuristics for a board config
                if(str(board_copy) not in heur_dict):
                    (score,move) = self.compute_heuristic(board_copy,piece,col)
                    heur_dict[str(board_copy)] = (score,move)
                else:
                    return heur_dict[str(board_copy)]

                # Cache score for a board
                state_dict[str(board)] = (score,move)
                return score,move
            else:

                piece= quintris.get_piece()[0]
                col= quintris.get_piece()[2]

                # If maximizing player return max score of successors
                if(player==0):
                    max = -infinity
                    successors_list = self.successors(board,piece,col)
                    next_move =''

                    for succ in successors_list:
                        score,move = self.expectiminimax(succ[0], len(self.empty_cells(succ[0])),1,state_dict,heur_dict)
                        if score>max:
                            max = score
                            next_move = move
                        state_dict[str(board)] = (score,move)
                    state_dict[str(board)] = (max,next_move)
                    return max,''

                # If minimizing player return avg score of successors
                elif(player==1):
                    avg = 0
                    next_move=''
                    max = -infinity
                    successors_list = self.successors(board,piece,col)
                    for succ in successors_list:
                        score,move = self.expectiminimax(succ[0],len(self.empty_cells(succ[0])),0,state_dict,heur_dict)
                        avg+=score*0.1667

                        next_move=move
                        state_dict[str(succ)] = (score,move)
                    state_dict[str(board)] = ((float(avg)),'')
                    return (float(avg)),next_move
        else:
               return state_dict[str(board)][0],state_dict[str(board)][1]

    def successors(self, board,piece,col):

        # List to store successors
        successor_list = []

        # List of bottom empty positions
        bottom_unfilled_col_indices = []

        # Get the coordinates of bottommost empty columns
        # Taking into account all blockers at the bottom
        for i in range(len(board[0])):
            flag=0
            for j in range(len(board)):
                if(board[j][i]=='x'):
                    bottom_unfilled_col_indices.append((j,i))
                    flag=1
                    break
            if(flag!=1):
                bottom_unfilled_col_indices.append((quintris.BOARD_HEIGHT,i))

        # Get all piece orientations possible i.e rotate, horizontal flip
        piece_orientations = self.get_all_piece_orientations()

        for i in range(len(piece_orientations)):

            piece = piece_orientations[i][0]
            move = piece_orientations[i][1]

            piece_height = len(piece)

            piece_width = 0
            for block in piece:
                if(piece_width<len(block)):
                    piece_width = len(block)

            # At every empty bottom position check if piece placement is valid
            for pos in bottom_unfilled_col_indices:

                # If placement valid
                if pos[1]+piece_width<=quintris.BOARD_WIDTH and pos[0]-piece_height>=1 and not QuintrisGame.check_collision(board,quintris.state[1],piece,pos[0]-piece_height,pos[1]):

                    # Place piece
                    new_board = QuintrisGame.place_piece(board, quintris.state[1], piece,pos[0]-piece_height-1 ,pos[1])

                    # If new best position in same column
                    if pos[1]==col:
                        successor_list.append((new_board[0],move))

                    # If new best position to the left move left
                    elif pos[1]<col:
                        move_left=''
                        for i in range(col-pos[1]):
                            move_left+="b"
                        move_next = move+move_left
                        successor_list.append((new_board[0], move_next))

                    # If new best position to the right move right
                    elif pos[1]>col:
                        move_left=''
                        for i in range(pos[1]-col):
                            move_left+="m"
                        move_next = move+move_left
                        successor_list.append((new_board[0], move_next))

        return successor_list

    # Code to compute heuristic by taking into account all successors
    def compute_heuristic(self, board, piece, col):

        # For each successor calculate score by considering height, holes bumpiness, no_of_row_clears etc.
        succ = self.successors(board, piece, col)
        height,bumpiness,holes, wells,bases,edges, no_of_clears = self.compute_parameters(board,piece,col)
        best_move = ''
        best_score = -infinity

        for i in range(len(succ)):
             score =  3.6*height[i] - 2.2*holes[i] + 1.5*wells[i] + 7*no_of_clears[i] + 0.2*edges[i] + 0.06*bumpiness[i] + 4.2*bases[i]
             if(score>best_score):
                best_score = score
                best_move = succ[i][1]

        return best_score,best_move

    # Code to compute heuristic by taking into account all successors and their successors
    def compute_heuristic_depth2(self, board, piece, col):
        succ = self.successors(board, piece,col)
        height,bumpiness,holes, wells,bases,edges, row_clears = self.compute_parameters(board,piece,col)
        best_move = ''
        best_score = -infinity
        for i in range(len(succ)):
            piece1 = quintris.get_next_piece()
            avg = 0
            for col1 in range(0,quintris.BOARD_WIDTH):
                succ_next = self.successors(succ[i][0], quintris.get_next_piece(), col1)
                height_next,bumpiness_next,holes_next, wells_next,bases_next,edges_next, row_clears_next = self.compute_parameters(succ[i][0],piece,col)

                for j in range(len(succ_next)):
                    score = 5.5*height_next[j]-5*holes_next[j]+ 13*row_clears_next[j]+2*bumpiness_next[j]+3*edges_next[j]+3*wells_next[j]+bases_next[j]*7
                    avg+=score*0.1667

                score = (8*height[i]-4.79*holes[i]+10*row_clears[i]+2*bumpiness[i]+3*edges[i]+7*bases[i]+3*wells[i])*avg
                if(score>best_score):
                    best_score = score
                    best_move = succ[i][1]

        return best_score,best_move

    # Rotate and flip the piece to get all possible orientations along with the associated moves
    def get_all_piece_orientations(self):
        # List to store orientations

        piece_orientations=[]
        piece = quintris.get_piece()[0]
        piece_orientations.append((piece,""))
        new_piece = piece

        # Rotations
        for i in range(1,4):
            move = ''
            for j in range(i):
                move+='n'
            new_piece = quintris.rotate_piece(new_piece,90)
            piece_orientations.append((new_piece,move))

        # Horizontal flip
        hflip_new_piece = quintris.hflip_piece(piece)
        piece_orientations.append((hflip_new_piece,"h"))

        # Rotations after horizontal flip
        for i in range(1,4):
            move = 'h'
            for j in range(i):
                move+='n'
            hflip_new_piece = quintris.rotate_piece( hflip_new_piece,90)
            piece_orientations.append(( hflip_new_piece,move))

        return piece_orientations


    def compute_parameters(self,board,piece, col):

        # Code to compute difference in aggregate min height of current state and its successors
        succs= self.successors(board, piece, col)
        current_height= 0
        min_height = infinity
        for row in board:
             if 'x' in row:
                aggregate_height = board.index(row)
                if(aggregate_height<min_height):
                    min_height = aggregate_height
        if(min_height==infinity):
            current_height = 0
        else:
            current_height = min_height

        height=[]
        min_height = infinity
        for succ in succs:
            aggregate_height = 0
            min_height = infinity
            for row in succ[0]:
                 if 'x' in row:
                    aggregate_height = succ[0].index(row)
                    if(aggregate_height<min_height):
                        min_height = aggregate_height
            if(min_height==infinity):
                height.append(-current_height)
            else:
                height.append(min_height-current_height)

        # Code to compute difference in number of holes of current state and its successors
        holes_count = []
        wells_count = []

        board_holes_count = 0
        board_wells_count = 0

        for j in range(0, quintris.BOARD_WIDTH):
            i= quintris.BOARD_HEIGHT-1
            while(i>0):
                index = i-1
                if(board[i][j]==' '):
                    while(index>0 and board[index][j]!='x'):
                        index-=1
                    if(index==0):
                        board_wells_count+=1
                        break
                    else:
                        board_holes_count+=i-index
                i=index

        for succ in succs:
            holes=0
            wells = 0
            for j in (range(0, quintris.BOARD_WIDTH)):
                i= quintris.BOARD_HEIGHT-1
                while(i>0):
                    index = i-1
                    if(succ[0][i][j]==' '):
                        while(index>0 and succ[0][index][j]!='x'):
                            index-=1
                        if(index==0):
                            wells+=1
                            break
                        else:
                            holes+=i-index
                    i=index
            holes_count.append(holes-board_holes_count)
            wells_count.append(wells-board_wells_count)

        # Code to compute number of row clears in successors
        complete_lines=0
        clear_list=[]
        for succ in succs:
            for i in range(0, quintris.BOARD_HEIGHT):

                 if(succ[0][i]=='xxxxxxxxxxxxxxx'):
                     complete_lines+=1
            clear_list.append(complete_lines)

        count_board = 0
        for i in range(len(board[0])):
           if(board[0][i]=='x'):
               count_board+=1
           if(board[0][i]==' ' and (board[quintris.BOARD_HEIGHT-2][i]=='x' or  board[quintris.BOARD_HEIGHT-1][i]=='x')):
               count_board+=1


        # Code to compute the base difference
        base_counts = []

        for succ in succs:
            count_base = 0
            for i in range(len(succ[0][0])):
                if(succ[0][0][i]=='x'):
                    count_base+=1
                if(succ[0][0][i]==' ' and (succ[0][quintris.BOARD_HEIGHT-2][i]=='x' or  succ[0][quintris.BOARD_HEIGHT-1][i]=='x')):
                    count_base+=1
            base_counts.append(count_base-count_board)

        count_board = 0
        for i in range(len(board)):

            if(board[i][0]=='x'):
                count_board+=1
            if(board[i][14]=='x'):
                count_board+=1

        # Code to compute the edge difference
        edge_counts = []
        for succ in succs:
            count_edge = 0
            for i in range(len(succ[0][0])):
                if(succ[0][i][0]=='x'):
                    count_edge+=1
                if(succ[0][i][14]=='x'):
                    count_edge+=1
            edge_counts.append(count_edge-count_board)

        # Code to compute difference in bumpiness of current state and it successors
        self_bumpiness = self.bumpiness_state(board)
        bumpiness_list = []
        for succ in succs:
            bumpiness_list.append(self_bumpiness-self.bumpiness_state(succ[0]))
        return height,bumpiness_list,holes_count, wells_count,base_counts,edge_counts, clear_list

    #Code to compute number of empty cells
    def empty_cells(self,board):
        cells = []
        for x in range(0,len(board)):
            for y in range(0,len(board[0])):
                 if(board[x][y]!='x'):
                    cells.append([x, y])
        return cells

    # Code to compute bumpiness(sum of absolute difference in adjacent heights) of given state
    def bumpiness_state(self,board):
        bumpiness = 0

        col_height = []
        for i in range(0, quintris.BOARD_WIDTH):
            for j in (range(0,quintris.BOARD_HEIGHT)):
                if(board[j][i]=='x'):
                    col_height.append(j)
                    break

        for i in range(1,len(col_height)):
            bumpiness+= abs(col_height[i]-col_height[i-1])
        return bumpiness

# Evaluation function for single state (This did not give good results)
def evaluation_fn(board):
    board_holes_count = 0
    board_wells_count = 0

    # Holes and wells count
    for j in range(0, quintris.BOARD_WIDTH):
        i= quintris.BOARD_HEIGHT-1
        while(i>0):
            index = i-1
            if(board[i][j]==' '):
                while(index>0 and board[index][j]!='x'):
                    index-=1
                if(index==0):
                    board_wells_count+=1
                    break
                else:
                    board_holes_count+=i-index
            i=index

    complete_lines = 0

    # Row clears
    for i in range(0, quintris.BOARD_HEIGHT):
        if(board[i]=='xxxxxxxxxxxxxxx'):
            complete_lines+=1


    # Code to compute bumpiness
    bumpiness = 0

    col_height = []
    for i in range(0, quintris.BOARD_WIDTH):
        for j in (range(0,quintris.BOARD_HEIGHT)):
            if(board[j][i]=='x'):
                col_height.append(j)
                break

    for i in range(1,len(col_height)):
        bumpiness+= abs(col_height[i]-col_height[i-1])
    return bumpiness


    current_height= 0
    min_height = infinity
    for row in board:
         if 'x' in row:
            aggregate_height = board.index(row)
            if(aggregate_height<min_height):
                min_height = aggregate_height
    if(min_height==infinity):
        current_height = 0
    else:
        current_height = min_height

    return -50*current_height + 100*complete_lines - 30*board_holes_count - 60*bumpiness -10*board_wells_count

###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)