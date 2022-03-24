#
# raichu.py : Play the game of Raichu
#
# Authors:   Primary: Jacob Striebel    (jstrieb)
#          Secondary: Aishwarya Budhkar (abudhkar)
#                     Shubhavi Arya     (aryas)
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import math

def get_row_col(offset, N):
  
  r = math.floor(offset/N)
  c = offset - (r*N)
  
  return r, c


def reflect_board(N, board):
  
  reflected_board = ''
  
  for r in range(N):
    for c in range(N):
      square = board[(N-1-r)*N + c]
      reflected_square = None
      if 'w'==square:
        reflected_square = 'b'
      elif 'W'==square:
        reflected_square = 'B'
      elif '@'==square:
        reflected_square = '$'
      elif 'b'==square:
        reflected_square = 'w'
      elif 'B'==square:
        reflected_square = 'W'
      elif '$'==square:
        reflected_square = '@'
      elif '.'==square:
        reflected_square = '.'
      else:
        assert False
      reflected_board += reflected_square
      
  return reflected_board


def actions(N, board, player):
  
  N_save      = N
  board_save  = board
  player_save = player
  legal_moves = set()
  
  if 'w'==player:
    
    for i in range(N*N):
      i_save = i
      r, c = get_row_col(i, N)
      
      if 'w'==board[i]:
        
        r0 = r+1
        c0 = c-1
        i0 = r0*N + c0
        if r0 < N and c0 >= 0 and '.'==board[i0]:
          rslt_piece = 'w'
          if N-1==r0:
            rslt_piece = '@'
          legal_moves.add( board[:i] + '.' + board[i+1:i0] + rslt_piece + board[i0+1:] )
        del r0
        del c0
        del i0
        
        r1 = r+1
        c1 = c+1
        i1 = r1*N + c1
        if r1 < N and c1 < N and '.'==board[i1]:
          rslt_piece = 'w'
          if N-1==r1:
            rslt_piece = '@'
          legal_moves.add( board[:i] + '.' + board[i+1:i1] + rslt_piece + board[i1+1:] )
        del r1
        del c1
        del i1
        
        r2a = r+1
        c2a = c-1
        i2a = r2a*N + c2a
        r2b = r+2
        c2b = c-2
        i2b = r2b*N + c2b
        if r2b < N and c2b >= 0 and 'b'==board[i2a] and '.'==board[i2b]:
          rslt_piece = 'w'
          if N-1 == r2b:
            rslt_piece = '@'
          legal_moves.add( board[:i] + '.' + board[i+1:i2a] + '.' + board[i2a+1:i2b] + rslt_piece + board[i2b+1:] )
        del r2a
        del c2a
        del i2a
        del r2b
        del c2b
        del i2b
        
        r3a = r+1
        c3a = c+1
        i3a = r3a*N + c3a
        r3b = r+2
        c3b = c+2
        i3b = r3b*N + c3b
        if r3b < N and c3b < N and 'b'==board[i3a] and '.'==board[i3b]:
          rslt_piece = 'w'
          if N-1==r3b:
            rslt_piece = '@'
          legal_moves.add( board[:i] + '.' + board[i+1:i3a] + '.' + board[i3a+1:i3b] + rslt_piece + board[i3b+1:] )
        del r3a
        del c3a
        del i3a
        del r3b
        del c3b
        del i3b
        
      elif 'W'==board[i]:
        
        def add_board(new_board, board='empty', i=-99, i1a=-99):
          if len(new_board)!=N*N:
            print('error: a generated board has the wrong number of board squares ', len(new_board))
            print(new_board)
            print(board)
            print('i=', i)
            print('i1a=', i1a)
            assert False
          legal_moves.add(new_board)
        
        # West
        
        r0a = r
        c0a = c-1
        i0a = r0a*N + c0a
        r0b = r
        c0b = c-2
        i0b = r0b*N + c0b
        r0c = r
        c0c = c-3
        i0c = r0c*N + c0c
        
        if c0a >= 0 and '.'==board[i0a]:
          add_board( board[:i0a] + 'W.' + board[i+1:] )
        
        if c0b >= 0 and '.'==board[i0a] and '.'==board[i0b]:
          add_board( board[:i0b] + 'W..' + board[i+1:] )
        
        if c0b >= 0 and board[i0a] in 'bB' and '.'==board[i0b]:
          add_board( board[:i0b] + 'W..' + board[i+1:] )
        
        if c0c >= 0 and board[i0a] in 'bB' and '.'==board[i0b] and '.'==board[i0c]:
         add_board( board[:i0c] + 'W...' + board[i+1:] )
        
        if c0c >= 0 and '.'==board[i0a] and board[i0b] in 'bB' and '.'==board[i0c]:
          add_board( board[:i0c] + 'W...' + board[i+1:] )
        
        del r0a
        del c0a
        del i0a
        del r0b
        del c0b
        del i0b
        del r0c
        del c0c
        del i0c
        
        
        # East
        
        r1a = r
        c1a = c+1
        i1a = r1a*N + c1a
        r1b = r
        c1b = c+2
        i1b = r1b*N + c1b
        r1c = r
        c1c = c+3
        i1c = r1c*N + c1c
        
        if c1a < N and '.'==board[i1a]:
          add_board( board[:i] + '.W' + board[i1a+1:], board, i, i1a )
        
        if c1b < N and '.'==board[i1a] and '.'==board[i1b]:
          add_board( board[:i] + '..W' + board[i1b+1:] )
        
        if c1b < N and board[i1a] in 'bB' and '.'==board[i1b]:
          add_board( board[:i] + '..W' + board[i1b+1:] )
        
        if c1c < N and board[i1a] in 'bB' and '.'==board[i1b] and '.'==board[i1c]:
          add_board( board[:i] + '...W' + board[i1c+1:] )
        
        if c1c < N and '.'==board[i1a] and board[i1b] in 'bB' and '.'==board[i1c]:
          add_board( board[:i] + '...W' + board[i1c+1:] )
        
        del r1a
        del c1a
        del i1a
        del r1b
        del c1b
        del i1b
        del r1c
        del c1c
        del i1c
        
        
        # South
        
        r2a = r+1
        c2a = c
        i2a = r2a*N + c2a
        r2b = r+2
        c2b = c
        i2b = r2b*N + c2b
        r2c = r+3
        c2c = c
        i2c = r2c*N + c2c
        
        if r2a < N and '.'==board[i2a]:
          rslt_piece = 'W'
          if N-1==r2a:
            rslt_piece = '@'
          add_board( board[:i] + '.' + board[i+1:i2a] + rslt_piece + board[i2a+1:] )
        
        if r2b < N and '.'==board[i2a] and '.'==board[i2b]:
          rslt_piece = 'W'
          if N-1==r2b:
            rslt_piece = '@'
          add_board( board[:i] + '.' + board[i+1:i2b] + rslt_piece + board[i2b+1:] )
        
        if r2b < N and board[i2a] in 'bB' and '.'==board[i2b]:
          rslt_piece = 'W'
          if N-1==r2b:
            rslt_piece = '@'
          add_board( board[:i] + '.' + board[i+1:i2a] + '.' + board[i2a+1:i2b] + rslt_piece + board[i2b+1:] )
        
        if r2c < N and board[i2a] in 'bB' and '.'==board[i2b] and '.'==board[i2c]:
          rslt_piece = 'W'
          if N-1==r2c:
            rslt_piece = '@'
          add_board( board[:i] + '.' + board[i+1:i2a] + '.' + board[i2a+1:i2c] + rslt_piece + board[i2c+1:] )
        
        if r2c < N and '.'==board[i2a] and board[i2b] in 'bB' and '.'==board[i2c]:
          rslt_piece = 'W'
          if N-1==r2c:
            rslt_piece = '@'
          add_board( board[:i] + '.' + board[i+1:i2b] + '.' + board[i2b+1:i2c] + rslt_piece + board[i2c+1:] )
        
        del r2a
        del c2a
        del i2a
        del r2b
        del c2b
        del i2b
        del r2c
        del c2c
        del i2c
        
      elif '@'==board[i]:
        
        # North
        r0a = r
        c0a = c
        i0a = -1
        while (r0a := r0a-1) >= 0:
          i0a = r0a*N + c0a
          if '.'==board[i0a]:
            legal_moves.add( board[:i0a] + '@' + board[i0a+1:i] + '.' + board[i+1:] )
          elif board[i0a] in 'wW@':
            break
          elif board[i0a] in 'bB$':
            r0b = r0a
            c0b = c0a
            i0b = -1
            while (r0b := r0b-1) >= 0:
              i0b = r0b*N + c0b
              if '.'==board[i0b]:
                legal_moves.add( board[:i0b] + '@' + board[i0b+1:i0a] + '.' + board[i0a+1:i] + '.' + board[i+1:] )
              elif board[i0b] in 'wW@bB$':
                break
              else:
                assert False
            del r0b
            del c0b
            del i0b
            break
          else:
            assert False
        del r0a
        del c0a
        del i0a
        
        # Northeast
        r1a = r
        c1a = c
        i1a = -1
        while (r1a := r1a-1) >= 0 and (c1a := c1a+1) < N:
          i1a = r1a*N + c1a
          if '.'==board[i1a]:
            legal_moves.add( board[:i1a] + '@' + board[i1a+1:i] + '.' + board[i+1:] )
          elif board[i1a] in 'wW@':
            break
          elif board[i1a] in 'bB$':
            r1b = r1a
            c1b = c1a
            i1b = -1
            while (r1b := r1b-1) >= 0 and (c1b := c1b+1) < N:
              i1b = r1b*N + c1b
              if '.'==board[i1b]:
                legal_moves.add( board[:i1b] + '@' + board[i1b+1:i1a] + '.' + board[i1a+1:i] + '.' + board[i+1:] )
              elif board[i1b] in 'wW@bB$':
                break
              else:
                assert False
            del r1b
            del c1b
            del i1b
            break
          else:
            assert False
        del r1a
        del c1a
        del i1a
        
        # East
        r2a = r
        c2a = c
        i2a = -1
        while (c2a := c2a+1) < N:
          i2a = r2a*N + c2a
          if '.'==board[i2a]:
            legal_moves.add( board[:i] + '.' + board[i+1:i2a] + '@' + board[i2a+1:] )
          elif board[i2a] in 'wW@':
            break
          elif board[i2a] in 'bB$':
            r2b = r2a
            c2b = c2a
            i2b = -1
            while (c2b := c2b+1) < N:
              i2b = r2b*N + c2b
              if '.'==board[i2b]:
                legal_moves.add( board[:i] + '.' + board[i+1:i2a] + '.' + board[i2a+1:i2b] + '@' + board[i2b+1:] )
              elif board[i2b] in 'wW@bB$':
                break
              else:
                assert False
            del r2b
            del c2b
            del i2b
            break
          else:
            assert False
        del r2a
        del c2a
        del i2a
        
        # Southeast
        r3a = r
        c3a = c
        i3a = -1
        while (r3a := r3a+1) < N and (c3a := c3a+1) < N:
          i3a = r3a*N + c3a
          if '.'==board[i3a]:
            legal_moves.add( board[:i] + '.' + board[i+1:i3a] + '@' + board[i3a+1:] )
          elif board[i3a] in 'wW@':
            break
          elif board[i3a] in 'bB$':
            r3b = r3a
            c3b = c3a
            i3b = -1
            while (r3b := r3b+1) < N and (c3b := c3b+1) < N:
              i3b = r3b*N + c3b
              if '.'==board[i3b]:
                legal_moves.add( board[:i] + '.' + board[i+1:i3a] + '.' + board[i3a+1:i3b] + '@' + board[i3b+1:] )
              elif board[i3b] in 'wW@bB$':
                break
              else:
                assert False
            del r3b
            del c3b
            del i3b
            break
          else:
            assert False
        del r3a
        del c3a
        del i3a
        
        # South
        r4a = r
        c4a = c
        i4a = -1
        while (r4a := r4a+1) < N:
          i4a = r4a*N + c4a
          if '.'==board[i4a]:
            legal_moves.add( board[:i] + '.' + board[i+1:i4a] + '@' + board[i4a+1:] )
          elif board[i4a] in 'wW@':
            break
          elif board[i4a] in 'bB$':
            r4b = r4a
            c4b = c4a
            i4b = -1
            while (r4b := r4b+1) < N:
              i4b = r4b*N + c4b
              if '.'==board[i4b]:
                legal_moves.add( board[:i] + '.' + board[i+1:i4a] + '.' + board[i4a+1:i4b] + '@' + board[i4b+1:] )
              elif board[i4b] in 'wW@bB$':
                break
              else:
                assert False
            del r4b
            del c4b
            del i4b
            break
          else:
            assert False
        del r4a
        del c4a
        del i4a
        
        # Southwest
        r5a = r
        c5a = c
        i5a = -1
        while (r5a := r5a+1) < N and (c5a := c5a-1) >= 0:
          i5a = r5a*N + c5a
          if '.'==board[i5a]:
            legal_moves.add( board[:i] + '.' + board[i+1:i5a] + '@' + board[i5a+1:] )
          elif board[i5a] in 'wW@':
            break
          elif board[i5a] in 'bB$':
            r5b = r5a
            c5b = c5a
            i5b = -1
            while (r5b := r5b+1) < N and (c5b := c5b-1) >= 0:
              i5b = r5b*N + c5b
              if '.'==board[i5b]:
                legal_moves.add( board[:i] + '.' + board[i+1:i5a] + '.' + board[i5a+1:i5b] + '@' + board[i5b+1:] )
              elif board[i5b] in 'wW@bB$':
                break
              else:
                assert False
            del r5b
            del c5b
            del i5b
            break
          else:
            assert False
        del r5a
        del c5a
        del i5a
        
        # West
        r6a = r
        c6a = c
        i6a = -1
        while (c6a := c6a-1) >= 0:
          i6a = r6a*N + c6a
          if '.'==board[i6a]:
            legal_moves.add( board[:i6a] + '@' + board[i6a+1:i] + '.' + board[i+1:] )
          elif board[i6a] in 'wW@':
            break
          elif board[i6a] in 'bB$':
            r6b = r6a
            c6b = c6a
            i6b = -1
            while (c6b := c6b-1) >= 0:
              i6b = r6b*N + c6b
              if '.'==board[i6b]:
                legal_moves.add( board[:i6b] + '@' + board[i6b+1:i6a] + '.' + board[i6a+1:i] + '.' + board[i+1:] )
              elif board[i6b] in 'wW@bB$':
                break
              else:
                assert False
            del r6b
            del c6b
            del i6b
            break
          else:
            assert False
        del r6a
        del c6a
        del i6a
        
        # Northwest
        r7a = r
        c7a = c
        i7a = -1
        while (r7a := r7a-1) >= 0 and (c7a := c7a-1) >= 0:
          i7a = r7a*N + c7a
          if '.'==board[i7a]:
            legal_moves.add( board[:i7a] + '@' + board[i7a+1:i] + '.' + board[i+1:] )
          elif board[i7a] in 'wW@':
            break
          elif board[i7a] in 'bB$':
            r7b = r7a
            c7b = c7a
            i7b = -1
            while (r7b := r7b-1) >= 0 and (c7b := c7b-1) >= 0:
              i7b = r7b*N + c7b
              if '.'==board[i7b]:
                legal_moves.add( board[:i7b] + '@' + board[i7b+1:i7a] + '.' + board[i7a+1:i] + '.' + board[i+1:] )
              elif board[i7b] in 'wW@bB$':
                break
              else:
                assert False
            del r7b
            del c7b
            del i7b
            break
          else:
            assert False
        del r7a
        del c7a
        del i7a
        
      elif board[i] in ".bB$":
        pass
      else:
        assert False
      
      assert i==i_save
      assert N==N_save
      assert get_row_col(i, N)==(r, c)
      
  elif 'b'==player:
    
    reflected_board = reflect_board(N, board)
    reflected_legal_moves = actions(N, reflected_board, 'w')
    for reflected_move in reflected_legal_moves:
      legal_moves.add( reflect_board(N, reflected_move) )
    
  else:
    assert False
  
  assert N==N_save
  assert board==board_save
  assert player==player_save
  
  for move in legal_moves:
    #assert len(move)==N*N
    if len(move)!=N*N:
      print('error: a generated move has the wrong number of board squares: ', len(move))
      print(move)
      assert False
  
  return legal_moves


PICHU_VALUE   =  1  # A Pichu can only capture other Pichus; basically useless
PIKACHU_VALUE =  4
RAICHU_VALUE  = 16
def evaluate_board(N, board, player):
  white_score = 0
  black_score = 0
  for r in range(N):
    for c in range(N):
      square = board[r*N + c]
      if 'w'==square:
        white_score += PICHU_VALUE
      elif 'W'==square:
        white_score += PIKACHU_VALUE
      elif '@'==square:
        white_score += RAICHU_VALUE
      elif 'b'==square:
        black_score += PICHU_VALUE
      elif 'B'==square:
        black_score += PIKACHU_VALUE
      elif '$'==square:
        black_score += RAICHU_VALUE
      elif '.'==square:
        pass
      else:
        assert False
  if 0==black_score:
    white_score = 9999
  if 0==white_score:
    black_score = 9999
  return (0==white_score if 'w'==player else 0==black_score,
          0==black_score if 'w'==player else 0==white_score,
          white_score - black_score if 'w'==player else black_score - white_score)


def max_value(N, board, max_player, min_player, current_depth, depth_limit):
  assert current_depth<=depth_limit
  # Terminal tests
  no_max_pieces, no_min_pieces, score_for_max = evaluate_board(N, board, max_player)
  assert False==no_min_pieces # Min just moved, he couldn't have moved no piece.
  if True==no_max_pieces:
    assert -9999==score_for_max
    return score_for_max
  legal_moves = actions(N, board, max_player)
  if 0==len(legal_moves):
    return 0 # Stalemate
  if current_depth==depth_limit:
    return score_for_max
  # Find the maximum min value
  move__score = dict()
  for move in legal_moves:
    assert move not in move__score
    move__score[move] = min_value(N, board, max_player, min_player, current_depth+1, depth_limit)
  best_move_score = -10000
  best_move = None
  for move in legal_moves:
    assert move in move__score
    score = move__score[move]
    if score > best_move_score:
      best_move_score = score
      best_move = move
  return best_move_score


def min_value(N, board, max_player, min_player, current_depth, depth_limit):
  assert current_depth<=depth_limit
  # Terminal tests
  no_max_pieces, no_min_pieces, score_for_max = evaluate_board(N, board, max_player)
  assert False==no_max_pieces # Max just moved, he couldn't have moved no piece.
  if True==no_min_pieces:
    assert 9999==score_for_max
    return score_for_max
  legal_moves = actions(N, board, min_player)
  if 0==len(legal_moves):
    return 0 # Stalemate
  if current_depth==depth_limit:
    return score_for_max
  # Find the minimum max value
  move__score = dict()
  for move in legal_moves:
    assert move not in move__score
    move__score[move] = max_value(N, board, max_player, min_player, current_depth+1, depth_limit)
  best_move_score = 10000
  best_move = None
  for move in legal_moves:
    assert move in move__score
    score = move__score[move]
    if score < best_move_score:
      best_move_score = score
      best_move = move
  return best_move_score


def minimax_decision(N, board, player):
  legal_moves = actions(N, board, player)
  assert len(legal_moves) > 0
  depth = 0
  while True:
    depth += 2
    move__score = dict()
    for move in legal_moves:
      assert move not in move__score
      move__score[move] = min_value(N, move, player, 'b' if 'w'==player else 'w', 0, depth)
    best_move_score = -10000
    best_move = None
    for move in legal_moves:
      assert move in move__score
      score = move__score[move]
      if score > best_move_score:
        best_move_score = score
        best_move = move
    if 9999==best_move_score:
      print('A guaranteed victory has been found at or before depth ', depth, ': next move:')
      print(best_move)
      break
    elif -9999==best_move_score:
      print('We are guaranteed to lose at or before depth ', depth, ' if our opponent plays optimally: random legal move:')
      print(best_move)
    else:
      print('Best move at depth ', depth, ':')
      print(best_move)


def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
    
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")
    
    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")
    
    first_row = board[:N]
    if 'b' in first_row or 'B' in first_row:
        raise Exception("input error: there is a black piece in the first row that is not a Raichu")
    
    last_row  = board[-N:]
    if 'w' in last_row or 'W' in last_row:
        raise Exception("input error: there is a white piece in the last row that is not a Raichu")
    
    no_white_pieces, no_black_pieces, _ = evaluate_board(N, board, 'w')
    
    if True==no_white_pieces:
        raise Exception("input error: the input board has no white pieces")
    
    if True==no_black_pieces:
        raise Exception("input error: the input board has no black pieces")
    
    legal_moves = actions(N, board, player)
    
    if 0==len(legal_moves):
        raise Exception("input error: you are asking a player to move who has no legal move")
    
    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    
    minimax_decision(N, board, player)
    
