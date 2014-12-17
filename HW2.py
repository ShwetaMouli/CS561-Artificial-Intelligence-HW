__author__ = 'Shweta'
# read input file
f = open("input.txt", 'r+b')
play_method = int(f.readline().rstrip('\n'))
my_player = f.readline().rstrip()
depth = int(f.readline().rstrip('\n'))
max_depth = depth
range_size = range(8)
directions = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

rows = [1, 2, 3, 4, 5, 6, 7, 8]
columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

tuple_in_dir = lambda tuple1, direction: (tuple1[0]+direction[0], tuple1[1]+direction[1])
tuple_valid = lambda tuple1: (tuple1[0] >= 0 and tuple1[0] < 8 and tuple1[1] >= 0 and tuple1[1] < 8)

if my_player == 'X':
    opponent = 'O'
else:
    opponent = 'X'

#code to create board
n = 1
start_board = []
while n <= 8:
    start_board.append(list(f.readline().rstrip()))
    n += 1

#print play_method, my_player, depth
#print start_board

rows = [1, 2, 3, 4, 5, 6, 7, 8]
columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

board_value = [[99, -8, 8, 6, 6, 8, -8, 99],
              [-8, -24, -4, -3, -3, -4, -24, -8],
              [8, -4, 7, 4, 4, 7, -4, 8],
              [6, -3, 4, 0, 0, 4, -3, 6],
              [6, -3, 4, 0, 0, 4, -3, 6],
              [8, -4, 7, 4, 4, 7, -4, 8],
              [-8, -24, -4, -3, -3, -4, -24, -8],
              [99, -8, 8, 6, 6, 8, -8, 99]]

#print board_value

#deepcopy function
def deepcopy(A):
    rt = []
    for elem in A:
        if isinstance(elem,list):
            rt.append(deepcopy(elem))
        else:
            rt.append(elem)
    return rt

#opponent
def opponent1(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

def evaluate(me, opponent, board):
    my_score, opponent_score = 0, 0
    i, j = 0, 0
    while i < 8:
        j = 0
        while j < 8:
            if board[i][j] == '*':
                pass
            elif board[i][j] == me:
                my_score += board_value[i][j]
            else:
                opponent_score += board_value[i][j]
            j += 1
        i += 1

    return my_score, opponent_score

#print evaluate('X', 'O', start_board)


def generate_moves(board, player):
        if player == 'X':
            opp = 'O'
        else:
            opp = 'X'

        moves = []
        for i in range_size:
            for j in range_size:
                if board[i][j] != '*':
                    continue
                for direction in directions:
                    t = tuple_in_dir((i,j), direction)
                    if (not tuple_valid(t)) or (board[t[0]][t[1]] != opp):
                        continue
                    while board[t[0]][t[1]] == opp:
                        t = tuple_in_dir(t, direction)
                        if not tuple_valid(t):
                            break
                    else:
                        if board[t[0]][t[1]] == player:
                            moves.append((i, j))
                            break

        if not moves: #and not terminal_test():
            moves = [None]

        else:
            i = 0
            while i < len(moves):
                j = i + 1
                while j < len(moves):
                    if moves[i][0]>moves[j][0]:
                        temp = moves[i]
                        moves[i]=moves[j]
                        moves[j]=temp
                    j+=1
                i+=1

            i = 0
            while i < len(moves):
                j = i + 1
                if j < len(moves):
                    while moves[i][0] == moves[j][0]:
                        if moves[i][1]>moves[j][1]:
                            temp = moves[i]
                            moves[i]=moves[j]
                            moves[j]=temp
                        if j < len(moves) - 1:
                            j+=1
                        else:
                            break
                i+=1




        return moves


#print generate_moves(start_board, 'X')


def make_move(board, move, player):
        board_copy = deepcopy(board)
        if move is None:
            return "NoValidMove"

        board_copy[move[0]][move[1]] = player

        if player == 'X':
            opp = 'O'
        else:
            opp = 'X'

        for direction in directions:

            t = tuple_in_dir(move, direction)

            if (not tuple_valid(t)) or (board[t[0]][t[1]] != opp):
                continue

            while board_copy[t[0]][t[1]] == opp:
                t = tuple_in_dir(t, direction)
                if not tuple_valid(t):
                    break

            else:

                if board_copy[t[0]][t[1]] == player:
                    t = tuple_in_dir(move, direction)

                    while board_copy[t[0]][t[1]] == opp:
                        board_copy[t[0]][t[1]] = player
                        t = tuple_in_dir(t, direction)
        #print board_copy

        return evaluate(player, opp, board_copy), board_copy, move

#print make_move(start_board, (2, 3), 'X')

def greedy_search(board, player):
    moves = generate_moves(board, player)
    possible_array = list()
    i = 0
    no_of_moves = len(moves)
    best_eval = 0
    best_move = list()

    board_copy = deepcopy(board)

    while i < no_of_moves:
        board_copy = deepcopy(board)
        possible_array.append([make_move(board_copy, moves[i], player), moves[i]])
        i += 1

    #print possible_array
    if possible_array[0][0] == "NoValidMove":
        return "NoPossibleMove"

    outloop = 0
    inloop = 0

    while outloop < len(possible_array):
        if possible_array[outloop][0][0] > best_eval:
            best_eval = possible_array[outloop][0][0]
        outloop += 1

    best_moves = list()
    outloop = 0
    while outloop < len(possible_array):
        if possible_array[outloop][0][0] == best_eval:
            best_moves.append(possible_array[outloop])
        outloop += 1

    first_row_move = best_moves[0][1][0]
    outloop = 0
    while outloop < len(best_moves):
        if best_moves[outloop][1][0] < first_row_move:
            first_row_move = best_moves[outloop][1][0]
        outloop += 1

    first_row_moves = list()
    outloop = 0
    while outloop < len(best_moves):
        if best_moves[outloop][1][0] == first_row_move:
            first_row_moves.append(best_moves[outloop])
        outloop += 1

    first_col_move_val = first_row_moves[0][1][1]
    first_col_move = first_row_moves[0]
    outloop = 0
    #print first_row_moves[outloop][1][1], outloop, len(best_moves)
    while outloop < len(first_row_moves):
        if first_row_moves[outloop][1][1] < first_col_move_val:
            first_col_move = first_row_moves[outloop]
            first_col_move_val = first_row_moves[outloop][1][1]
        outloop += 1

    #print possible_array
    board_copy = make_move(board_copy, first_col_move[1], player)
    return board_copy

#print greedy_search(start_board, 'O')


log = str()

def minimax_decision(board, depth, player):
    global log
    val = list()
    evalu = list()
    moves = generate_moves(board, player)
    i = 0
    if player == my_player:
        best = -99999
    else:
        best = 99999


    #log = "root,0,-Infinity"

    if moves[0] is not None:
        best_moves = list()
        while i < len(moves):
            b = deepcopy(board)
            mv = make_move(b, moves[i], player)
            b = mv[1]
            if depth == max_depth:
                log += '\n'+"root"+','+str(0)+','+str(best)
            else:
                log += '\n'+"pass"+','+str(max_depth - depth)+','+str(best)

            if player == my_player:
                evalu = minimax_value(b, depth-1, opponent, moves[i])
                val = max(evalu, best)
                #alpha = max(evalu[1], alpha)
                #beta = min(evalu[1], beta)
            else:
                #val.append([minimax_value(b, depth-1, my_player), moves[i]])
                evalu = minimax_value(b, depth-1, my_player, moves[i])
                val = min(evalu, best)
                #alpha = max(evalu[1], alpha)
                #beta = min(evalu[1], beta)

            best = val
            best_moves.append([best, moves[i]])
            #log += '\n'+str(columns[mv[2][1]])+str(rows[mv[2][0]])+','+str(1)+','+str(best) + "," + str(alpha) + "," + str(beta)

            i += 1
        if max_depth - depth == 0:
            log += '\n'+"root"+','+str(0)+','+str(best)
    elif max_depth - depth == 0:
        outcome = evaluate(my_player, opponent, board)
        log += '\n'+"root"+','+str(0)+','+str(best)
        #log += '\n' + "Pass" + ',' + "1,"+ str(best) + "," + str(alpha) + "," + str(beta)
        abd = minimax_decision(board, depth-1, opponent1(player))
        best = abd[0]
        best_moves = abd[1]
        log += '\n'+"pass"+','+str(1)+','+str(best)
        log += '\n'+"root"+','+str(0)+','+str(best)

    else:
        best_moves = None

    #print best_moves
    return best, best_moves

def minimax_value(board, depth, player, move, passv = None):
    global log
    if depth == 0:
        outcome = evaluate(my_player, opponent, board)
        log += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(max_depth)+','+str(outcome[0]-outcome[1])
        return outcome[0] - outcome[1]
    if player == my_player:
        best = -99999
    else:
        best = 99999
    moves = generate_moves(board, player)
    #print moves
    #log += '\n' + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(alpha) + "," + str(beta)
    if passv == None:
        log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best)

    if moves[0] is not None:
        i = 0
        while i < len(moves):

            b = deepcopy(board)
            mv = make_move(b, moves[i], player)
            b = mv[1]
            if player == my_player:
                #best = -10000
                mval = minimax_value(b, depth - 1, opponent, moves[i])
                val = max(mval, best)

                #return max(best, val)
            else:
                #best = 10000
                mval = minimax_value(b, depth - 1, my_player, moves[i])
                val = min(mval, best)


                #beta = min(beta, mval[1])
                #return min(best, val)
            best = val
            #return val
            if passv == None:
                log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best)
            if passv == True:
                log += "\n" + "pass" + ',' + str(max_depth - depth) + ',' + str(best)
                #log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth - 1) + ',' + str(best) + "," + str(alpha) + "," + str(beta)

            #log += "\nPass"

            #log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(val) + "," + str(alpha) + "," + str(beta) + "," + str(movealpha) + "," + str(movebeta)
            i += 1
    else:

        log += "\npass,"+str(max_depth - depth + 1)+","+str(-1*best)
        if player == my_player:
                #best = -10000
            mval = minimax_value(board, depth - 1, opponent, move, True)
            val = max(mval, best)
            log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(val)

                #return max(best, val)
        else:
            #best = 10000
            mval = minimax_value(board, depth - 1, my_player, move, True)
            val = min(mval, best)
            log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(val)
        #log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(movealpha) + "," + str(movebeta)

        best = val
            #return val
        #log += "\n" +"pass"+ ',' + str(max_depth - depth -1) + ',' + str(best) + "," + str(movealpha) + "," + str(movebeta)


            #val = None

    return val


#print minimax_decision(start_board, max_depth, my_player)


log = log.replace("-99999", "-Infinity")
log = log.replace("99999", "Infinity")
#print log





def alphabeta_decision(board, depth, player):
    global log
    val = list()
    evalu = list()
    moves = generate_moves(board, player)
    i = 0
    if player == my_player:
        best = -99999
    else:
        best = 99999

    alpha = -99999
    beta = 99999

    #log = "root,0,-Infinity"

    if moves[0] is not None:
        best_moves = list()
        while i < len(moves):
            b = deepcopy(board)
            mv = make_move(b, moves[i], player)
            b = mv[1]
            if depth == max_depth:
                log += '\n'+"root"+','+str(0)+','+str(best) + "," + str(alpha) + "," + str(beta)
            else:
                log += '\n'+"pass"+','+str(max_depth - depth)+','+str(best) + "," + str(alpha) + "," + str(beta)

            if player == my_player:
                evalu = alphabeta_value(b, depth-1, opponent, alpha, beta, moves[i])
                val = max(evalu[0], best)
                alpha = max(evalu[1], alpha)
                #beta = min(evalu[1], beta)
            else:
                #val.append([minimax_value(b, depth-1, my_player), moves[i]])
                evalu = alphabeta_value(b, depth-1, my_player, alpha, beta, moves[i])
                val = min(evalu[0], best)
                #alpha = max(evalu[1], alpha)
                beta = min(evalu[1], beta)

            best = val
            best_moves.append([best, moves[i]])
            #log += '\n'+str(columns[mv[2][1]])+str(rows[mv[2][0]])+','+str(1)+','+str(best) + "," + str(alpha) + "," + str(beta)

            i += 1
        if max_depth - depth == 0:
            log += '\n'+"root"+','+str(0)+','+str(best) + "," + str(alpha) + "," + str(beta)
    elif max_depth - depth == 0:
        outcome = evaluate(my_player, opponent, board)
        log += '\n'+"root"+','+str(0)+','+str(best) + "," + str(alpha) + "," + str(beta)
        #log += '\n' + "Pass" + ',' + "1,"+ str(best) + "," + str(alpha) + "," + str(beta)
        abd = alphabeta_decision(board, depth-1, opponent1(player))
        best = abd[0]
        best_moves = abd[1]
        log += '\n'+"pass"+','+str(1)+','+str(best) + "," + str(abd[2]) + "," + str(abd[3])
        log += '\n'+"root"+','+str(0)+','+str(best) + "," + str(abd[3]) + "," + str(-1*abd[2])

    else:
        best_moves = None

    #print best_moves
    return best, best_moves, alpha, beta

def alphabeta_value(board, depth, player, alpha, beta, move, passv = None):
    global log
    if depth == 0:
        outcome = evaluate(my_player, opponent, board)
        log += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(max_depth)+','+str(outcome[0]-outcome[1]) + "," + str(alpha) + "," + str(beta)
        return outcome[0] - outcome[1], None, None
    if player == my_player:
        best = -99999
    else:
        best = 99999
    moves = generate_moves(board, player)
    #print moves
    #log += '\n' + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(alpha) + "," + str(beta)
    if passv == None:
        log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(alpha) + "," + str(beta)

    if moves[0] is not None:
        i = 0
        while i < len(moves):
            movebeta = beta
            movealpha = alpha
            if alpha < beta:
                b = deepcopy(board)
                mv = make_move(b, moves[i], player)
                b = mv[1]
                if player == my_player:
                    #best = -10000
                    mval = alphabeta_value(b, depth - 1, opponent, alpha, beta, moves[i])
                    val = max(mval[0], best)
                    if mval[1] == None:
                        alpha = max(alpha, mval[0])
                        #alpha = mval[0]
                    else:
                        alpha = max(alpha, mval[1])

                    #return max(best, val)
                else:
                    #best = 10000
                    mval = alphabeta_value(b, depth - 1, my_player, alpha, beta, moves[i])
                    val = min(mval[0], best)
                    if mval[1] == None:
                        beta = min(beta, mval[0])
                        #beta = mval[0]
                    else:
                        beta = min(beta, mval[1])


                    #beta = min(beta, mval[1])
                    #return min(best, val)
                best = val
                #return val
                if passv == None:
                    log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(movealpha) + "," + str(movebeta)
                if passv == True:
                    log += "\n" + "pass" + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(movealpha) + "," + str(movebeta)
                    #log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth - 1) + ',' + str(best) + "," + str(alpha) + "," + str(beta)

            else:

                val = best
                if player == my_player:
                    return val, alpha, beta
                else:
                    return val, beta, alpha
                #log += "\nPass"

            #log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(val) + "," + str(alpha) + "," + str(beta) + "," + str(movealpha) + "," + str(movebeta)
            i += 1
    else:
        movealpha = alpha
        movebeta = beta
        log += "\npass,"+str(max_depth - depth + 1)+","+str(-1*best)+","+str(alpha)+","+str(beta)
        if player == my_player:
                #best = -10000
            mval = alphabeta_value(board, depth - 1, opponent, alpha, beta, move, True)
            val = max(mval[0], best)
            if mval[1] == None:
                alpha = max(alpha, mval[0])
            else:
                alpha = max(alpha, mval[1])
            printalpha = max(alpha, movealpha)
            printbeta = max(beta, movebeta)
            log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(val) + "," + str(printalpha) + "," + str(printbeta)

                #return max(best, val)
        else:
            #best = 10000
            mval = alphabeta_value(board, depth - 1, my_player, alpha, beta, move, True)
            val = min(mval[0], best)
            if mval[1] == None:
                beta = min(beta, mval[0])
            else:
                beta = min(beta, mval[1])
            printalpha = min(movealpha, alpha)
            printbeta = max(movebeta, beta)

            log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(val) + "," + str(printalpha) + "," + str(printbeta)
        #log += "\n" + str(columns[move[1]]) + str(rows[move[0]]) + ',' + str(max_depth - depth) + ',' + str(best) + "," + str(movealpha) + "," + str(movebeta)


    if player == my_player:
        return val, alpha, beta
    else:
        return val, beta, alpha

#print alphabeta_decision(start_board, max_depth, my_player)

log = log.replace("-99999", "-Infinity")
log = log.replace("99999", "Infinity")

#print log


if play_method == 1:
    output = greedy_search(start_board, my_player)[1]
    if output != 'o':
        next_state = output
    else:
        next_state = start_board
    next_state_str = str()
    i = 0
    while i < len(next_state):
        line = str(next_state[i]).replace('[','')
        line = line.replace(']', '')
        line = line.replace(',','')
        line = line.replace("\'",'')
        line = line.replace(" ",'')
        next_state_str += line+'\n'
        i += 1
    next_state_str = next_state_str.rstrip('\n')
    f = open("output.txt", "w")
    f.write(next_state_str)
    f.close()

if play_method == 2:
    best_moves = minimax_decision(start_board, max_depth, my_player)[1]
    #print best_moves
    if best_moves is not None:
        best_move = best_moves[0]
        i = 0
        while i < len(best_moves):
            if best_moves[i][0] > best_move[0]:
                best_move = best_moves[i]
            i += 1

        minimaxboard = deepcopy(start_board)
        next_state = make_move(minimaxboard, best_move[1], my_player)[1]
        #print minimaxboard
        log = log.replace("-99999", "-Infinity")
        log = log.replace("99999", "Infinity")
        #print log

    else:
        next_state = start_board
        outcome = evaluate(my_player, opponent, start_board)
        log = "\nroot,0,"+str(outcome[0]-outcome[1])


    next_state_str = str()
    i = 0
    while i < len(next_state):
        line = str(next_state[i]).replace('[','')
        line = line.replace(']', '')
        line = line.replace(',','')
        line = line.replace("\'",'')
        line = line.replace(" ",'')
        next_state_str += line+'\n'
        i += 1
    #next_state_str = next_state_str.rstrip('\n')
    f = open("output.txt", "w")
    f.write(next_state_str)
    f.write("Node,Depth,Value"+log)
    #f.write(log)
    f.close()

if play_method == 3:
    best_moves = alphabeta_decision(start_board, max_depth, my_player)[1]
    #print best_moves
    if best_moves is not None:
        best_move = best_moves[0]
        i = 0
        while i < len(best_moves):
            if best_moves[i][0] > best_move[0]:
                best_move = best_moves[i]
            i += 1

        board = deepcopy(start_board)
        next_state = make_move(board, best_move[1], my_player)[1]
        #print minimaxboard
        log = log.replace("-99999", "-Infinity")
        log = log.replace("99999", "Infinity")
        #print log

    else:
        next_state = start_board
        outcome = evaluate(my_player, opponent, start_board)
        log = "\nroot,0,"+str(outcome[0]-outcome[1])+",-Infinity,Infinity"

    next_state_str = str()
    i = 0
    while i < len(next_state):
        line = str(next_state[i]).replace('[','')
        line = line.replace(']', '')
        line = line.replace(',','')
        line = line.replace("\'",'')
        line = line.replace(" ",'')
        next_state_str += line+'\n'
        i += 1
    #next_state_str = next_state_str.rstrip('\n')
    f = open("output.txt", "w")
    f.write(next_state_str)
    f.write("Node,Depth,Value,Alpha,Beta"+log)
    #f.write(log)
    f.close()



