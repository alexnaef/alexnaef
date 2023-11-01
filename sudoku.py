
"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def find_zero(board):
    result = []
    for row in ROW:
        for col in COL:
            if board[row+col] == 0:
                result.append(row+col)
    return result

def current_row(index, board):
    row = index[0]
    temp_set = set()
    for col in COL:
        temp_set.add(board[row + col])
    return temp_set

def current_col(index, board):
    col = index[1]
    temp_set = set()
    for row in ROW:
        temp_set.add(board[row + col])
    return temp_set

def current_block(index, board):
    temp_set = set()
    row = (row_convert(index[0])) // 3 * 3
    col = (int(index[1]) - 1) // 3 * 3
    for i in range(3):
        for j in range(3):
            temp_set.add(board[ROW[row+i]+COL[j+col]])
    return temp_set

def mrv(board, empty):
    values = []
    for index in empty:
        values.append((index, candidates(board, index)))

    def sorting_key(item):
        candidates_len = len(item[1])
        heuristic_value = -heuristic(empty, item[0])
        return (candidates_len, heuristic_value)

    values.sort(key=sorting_key)

    if not values or not values[0][1]:
        return None

    return values[0]

def candidates(board, index):
    rocobo = (current_row(index, board) | 
    (current_col(index, board) | 
    current_block(index, board)))
    
    # Generate the domain by looping through values and filtering
    candidates = []
    for i in range(1, 10):
        if i not in rocobo:
            candidates.append(i)
    return candidates

def heuristic(empty, index):
    """Count the number of neighbors that are also in zero_board."""
    count = 0
    for neighbor in empty:
        if neighbor != index:
            row = neighbor[0] == index[0]
            col = neighbor[1] == index[1]
            block = ((row_convert(index[0])) // 3 == (row_convert(index[0])) // 3 
                            and (int(index[1]) - 1) // 3 == (int(neighbor[1]) - 1) // 3)
            
            if row or col or block:
                count += 1
                
    return count

def row_convert(index):
    dict = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8
    }
    return dict[index]

def backtracking(board):
    empty_spaces = find_zero(board)
    if not empty_spaces:
        return board

    next_index = mrv(board, empty_spaces)
    
    if not next_index:
        return None
    
    index, domains = next_index

    for val in domains:
        board[index] = val
        if backtracking(board):
            return board
        board[index] = 0

    return None


if __name__ == '__main__':
    times = []
    solved_puzzles = 0
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        
        
        start_time = time.time()
        solved_board = backtracking(board)
        end_time = time.time()
        total_time = start_time-end_time
        times.append(total_time)

        if solved_board == True:
            solved_puzzles += 1

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()
            total_time = end_time-start_time
            times.append(total_time)
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
        if times:
            mean_time = statistics.mean(times)
            std_dev_time = statistics.stdev(times)
            min_time = min(times)
            max_time = max(times)

            print(f"Total puzzles solved: {solved_board}/{len(times)}")
            print(f"Mean runtime: {mean_time:.4f} seconds")
            print(f"Standard deviation of runtime: {std_dev_time:.4f} seconds")
            print(f"Minimum runtime: {min_time:.4f} seconds")
            print(f"Maximum runtime: {max_time:.4f} seconds")
        else:
            print("No puzzles were solved.")