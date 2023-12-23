from collections import deque
import copy

global solved_csp
global csp 

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

        if possible_vals.get(variable)[0] in n_domain:
            csp_fc.get("domain").get(n).remove(possible_vals.get(variable)[0])

            if not n_domain:
                return False, csp_fc
    return True, csp_fc

            
def backtrack_ac3(possible_vals, csp):
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

            forward_checked, csp_fc = forwad_check(csp, unassigned_variable, possible_vals)
            if forward_checked:
                backtrack_sol = backtrack_ac3(possible_vals, csp)
                if backtrack_sol:
                    return True
            
            possible_vals.get(unassigned_variable).remove(v) #remove value from soln if forward check failed
    return False
        


            



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
    neighbors = {v: cell_neighbours(v) for v in variables}
    possible_vals = {v: [] for v in variables}
    csp = {
        "variables": variables,
        "domain": domain,
        "neighbors": neighbors
    }
    
    #parse string to array
    grid_array = [[int(num) for num in row.split()] for row in grid_string.strip().split("\n")]

    for i in range(n_cells):
        row = i // 9
        col = i % 9
        cell_val = grid_array[row][col]
        grid_array[row][col] = 0   #to avoid considering the cell value when validating

        #early detection of invalid boards
        if cell_val != 0:
            if cell_val < 0 or cell_val >9:
                print("invalid board")
                break
            if is_valid(grid_array, row, col ,cell_val):
                csp.get("domain")[i] = [cell_val]
                
            else:
                print("invalid board")
                csp["domain"] = {var: [] for var in variables}
                break
        
        grid_array[row][col] = cell_val  #return board to its initial form after validation

    
    #for i in range(n_cells):
        
        domain_i = csp.get("domain").get(i)

        if len(domain_i) == 1:  #append the values 
            possible_vals.get(i).append(domain_i[0])
        #####
            

    
    if is_arc_consistent(csp):
        backtrack_ac3(possible_vals, csp)
    

    #print output
        
    soln = ""

    for cell in csp.get("variables"):
        soln += str(possible_vals.get(cell)[0])

        if (cell + 1) % 9 == 0:
            if cell != 0 and cell != 80:
                soln += "\n"
        else:
            soln += " "
        
    print(soln)
main()