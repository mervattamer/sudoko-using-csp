def is_valid(grid, row, col, val):
    for i in range(10):
        if((grid[row][i] == val) or 
           (grid[i][col] == val) or 
           (grid[(3*(row/3) +(i/3))][(3*(col/3))+(i%3)] == val)):
            
            return False
    return True


def main():
    grid_string = """
    5 3 0 0 7 0 0 0 0
    6 0 0 1 9 5 0 0 0
    0 9 8 0 0 0 0 6 0
    8 0 0 0 6 0 0 0 3
    4 0 0 8 0 3 0 0 1
    7 0 0 0 2 0 0 0 6
    0 6 0 0 0 0 2 8 0
    0 0 0 4 1 9 0 0 5
    0 0 0 0 8 0 0 7 9
    """

    #csp representation
    n_cells = 81
    variables = [cell for cell in range(n_cells)]  #initialise variables
    domain = {v: [i for i in range(1,10)] for v in variables}

    csp = {
        "variables": variables,
        "domain": domain,
        #"neighbors": neighbors
    }

    #parse string to array
    grid_array = [[int(num) for num in row.split()] for row in grid_string.strip().split("\n")]

    for i in range(n_cells):
        row = i // 9
        col = i % 9
        cell_val = grid_array[row][col]

        #early detection of invalid boards
        if cell_val != 0:
            if cell_val < 0 or cell_val >9:
                print("invalid board")
            elif is_valid(grid_array, cell_val, i):
                csp.get("domain")[i] = [cell_val]
            else:
                print("invalid board")
        




