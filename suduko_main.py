from collections import deque
import copy
import pygame
import time
#import random_fn
from merv_input_gui import Grid
background_image = pygame.image.load('game_bg.jpg')
global solved_csp
global csp 
global board

space_for_tree = ""

s_tree = ""




def print_grid(csp, possible_vals, s_tree, display_gui):
    soln = s_tree

    
    for cell in csp.get("variables"):
        if (len(possible_vals.get(cell)) != 0):
            soln += str(possible_vals.get(cell)[0])
        else:
            soln += str(0)
        if (cell + 1) % 9 == 0:
            if cell != 0 and cell != 80:
                soln += "\n"
                soln += s_tree
        else:
            soln += " "
    #print(soln)
    if(display_gui):
        soln_array = [[int(num) for num in row.split()] for row in soln.strip().split("\n")]
        board.update_board(soln_array)
    ##win.fill((255,255,255))
        win.blit(background_image, (0, 0))
        board.draw()
        pygame.display.update()
    # time.sleep(0.2)
    
    
        
    


def is_valid(grid, row, col, val):
    for i in range(9):
        if((grid[row][i] == val) or 
           (grid[i][col] == val) or 
           (grid[(3*(row//3) +(i//3))][(3*(col//3))+(i%3)] == val)):
            
            return False
    return True

def cell_neighbours(variable_index):
    row = variable_index//9
    col = variable_index % 9
    neighbors = set()
    for i in range(9):
        neighbors.add(9 * row + i)
        neighbors.add(9*i +col)
        neighbors.add(9* (3*(row//3) +(i//3)) + (3*(col//3)+(i%3)))
    neighbors.remove(variable_index)
    return neighbors


def revise(csp, v , n):
    revised = False
    for d in csp.get("domain").get(v):
        consistent = False
        
        for dn in csp.get("domain").get(n):
            if (d != dn):
                consistent = True
                break
        if (consistent == False):
            csp.get("domain").get(v).remove(d)
            revised = True
    return revised




def is_arc_consistent(csp):
    arcs_queue = deque([])
    for v in csp.get("variables"):
        for n in csp.get("neighbors").get(v):
            arcs_queue.append((v,n))
            #print("added arc \n")
            #print(arcs_queue)

    while(len(arcs_queue) != 0 ):
        v, n = arcs_queue.popleft()
        revised = revise(csp, v, n)
        if revised:
            if (csp.get("domain").get(v) == []):
                return False
            for x in csp.get("neighbors").get(v):
                if x != n:
                    arcs_queue.append((x,v))
    return True

def lcv(variable, csp):
    domain = csp.get("domain").get(variable)
    neighbors = csp.get("neighbors").get(variable)

    def count_constraints(value):
        return sum(1 for neighbor in neighbors if value in csp.get("domain").get(neighbor))

    # Sort the domain based on the count of constraints (least constraining value first)
    sorted_domain = sorted(domain, key=count_constraints)

    return sorted_domain


def forwad_check(csp, variable, possible_vals):
    csp_fc = copy.deepcopy(csp)

    for n in csp_fc.get("neighbors").get(variable):
        n_domain = csp_fc.get("domain").get(n)

        #print("domainn  ")
        ##print(n)
        ##print("\n")
        #print(csp.get("domain").get())
        #time.sleep(5)

        if possible_vals.get(variable)[0] in n_domain:
            csp_fc.get("domain").get(n).remove(possible_vals.get(variable)[0])
            print("removed value to domain from pos")
            print(n)
            print("\n")
            print(csp.get("domain").get(n))
            
            time.sleep(5)

            if not n_domain:
                return False, csp_fc
    return True, csp_fc

            
def backtrack_ac3(possible_vals, csp):
    global space_for_tree
    global s_tree 
    #get unnassigned variable usig MRV
    mrv = 0
    solved = True
    for i, sol_vals in possible_vals.items():
        if len(sol_vals) == 0: #if there is unnassigned soln for any variable
            solved = False
            domain_len = len(csp.get("domain").get(i))
            
            if (mrv==0) or (domain_len <mrv):
                mrv = domain_len
                unassigned_variable = i
    if solved:
        #solved_csp = possible_vals
        return True
    
    #get domain for unassigned variable using lcv
    unassigned_var_domain = lcv(unassigned_variable, csp)

    for v in unassigned_var_domain:
        consistent = True
        for n in csp.get("neighbors").get(unassigned_variable):
            if v in possible_vals.get(n):
                consistent = False
        if consistent:
            possible_vals.get(unassigned_variable).append(v)
            #print("added value to domain \n")
            #print(csp.get("domain").get(unassigned_variable))
            space_for_tree = space_for_tree + "--"
            s_tree= s_tree+ "  "
            #print(space_for_tree + "arc consistent added " + str(v) + " to pos" + str(unassigned_variable)+ "\n" )
            
            print_grid(csp, possible_vals, s_tree, display_gui=False)

            forward_checked, csp_fc = forwad_check(csp, unassigned_variable, possible_vals)
            if forward_checked:
                backtrack_sol = backtrack_ac3(possible_vals, csp)
                if backtrack_sol:
                    return True
            
            possible_vals.get(unassigned_variable).remove(v) #remove value from soln if forward check failed
            #print("removed value from domain \n")
            #print(csp.get("domain").get(unassigned_variable))
            
            space_for_tree= space_for_tree.rstrip(space_for_tree[:-3])
            s_tree = s_tree.rstrip(s_tree[:-3])
            
            #print(space_for_tree + "not arc consistent removed " + str(v) + " from pos" + str(unassigned_variable) + "\n")
            print_grid(csp, possible_vals, s_tree, display_gui=False)
    return False
        


def array_to_string(array):
    result = ""
    for row in array:
        result += " ".join(str(num) for num in row)
        result += "\n"
    return result          



def main( grid_a):
    grid_string = array_to_string(grid_a)

    #csp representation
    n_cells = 81
    variables = [cell for cell in range(n_cells)]  #initialise variables
    domain = {v: [i for i in range(1,10)] for v in variables}
    neighbors = {v: cell_neighbours(v) for v in variables}
    possible_vals = {v: [] for v in variables}
    csp = {
        "variables": variables,
        "domain": domain,
        "neighbors": neighbors
    }
    
    valid_input = True
    #parse string to array
    grid_array = [[int(num) for num in row.split()] for row in grid_string.strip().split("\n")]

    for i in range(n_cells):
        row = i // 9
        col = i % 9
        cell_val = grid_array[row][col]
        grid_array[row][col] = 0   #to avoid considering the cell value when validating


        #could change this to strng validation only if there is time
        #early detection of invalid boards
        if cell_val != 0:
            if cell_val < 0 or cell_val >9:
                print("invalid board")
                valid_input = False
                break
            if is_valid(grid_array, row, col ,cell_val):
                csp.get("domain")[i] = [cell_val]
                
            else:
                print("invalid board")
                csp["domain"] = {var: [] for var in variables}
                valid_input = False
                break
        
        grid_array[row][col] = cell_val  #return board to its initial form after validation


        
        #for i in range(n_cells):
        
        domain_i = csp.get("domain").get(i)

        if len(domain_i) == 1:  #append the values 
            possible_vals.get(i).append(domain_i[0])
            
        #####
    #main_gui(grid_array)       

    if valid_input:
        if is_arc_consistent(csp):
            backtrack_ac3(possible_vals, csp)
        #print output
        print_grid(csp, possible_vals, s_tree , display_gui = True)
        
        
# grid_string = """
#     6 0 9 0 4 0 0 0 1
#     7 1 0 5 0 9 6 0 0
#     0 5 0 0 0 0 0 0 0
#     2 0 7 0 8 0 0 9 0
#     0 0 0 0 6 0 0 2 4
#     0 6 0 9 0 0 0 0 8
#     0 0 8 0 0 0 3 0 0
#     0 0 0 4 0 0 0 0 7
#     0 0 0 0 5 0 0 0 0
#     """    
# grid_a = [[int(num) for num in row.split()] for row in grid_string.strip().split("\n")]



#main(grid_string) 
def main_gui(b):
    #pygame.init()
    pygame.font.init()
    global win
    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku")
    #b = random_fn.random_inp() #grid array
    global board
    board = Grid(b, 9, 9, 540, 540, win)
    #win.fill((255,255,255))
    win.blit(background_image, (0, 0))
    board.draw()
    pygame.display.update()
    
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            start_time = time.time()
            main(b)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"Elapsed Time: {elapsed_time} seconds")
            time.sleep(60)
            break
        break
        
                
        
        
        #redraw_window(win, board)
       
    pygame.quit()


    

# main(grid_a)