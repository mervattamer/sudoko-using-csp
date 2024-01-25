# Sudoku Solver

## 1. Game Description

Sudoku Solver is a logic-based number-placement game that challenges players to fill a 9x9 grid with digits from 1 to 9. The objective is to complete the grid so that each row, each column, and each of the nine 3x3 subgrids contains all of the digits from 1 to 9 without repetition.

## 2. Implementation

### 2.1 Game GUI

- **Mode 1:** Full game with GUI demonstrating the AI agent solving the game.
  
- **Mode 2:** Game with GUI allowing users to input a board representation, then the agent solves it.

### 2.2 Algorithms

- **Backtracking:** Used to validate input (check if the puzzle is solvable) and to generate a random puzzle by filling random places.

### 2.3 Arc Consistency

- **Arc Consistency for Solution:**
  - Represent Sudoku as a CSP (Constraint Satisfaction Problem).
  - **Variables:** Each cell in the Sudoku grid is a variable.
  - **Domains:** The domain of each variable represents the possible numbers (1 to 9) that can be placed in the cell.
  - **Constraints:** Sudoku rules – no number can be repeated in a row, column, or 3x3 subgrid.
  - **Define Arcs:** An arc in Sudoku represents a binary constraint between two variables (cells). Arc consistency is applied to all pairs of connected variables.
  - **Initial Domain Reduction:** Before applying arc consistency, initialize the domains based on the initial puzzle.
    - For pre-filled cells, remove all other values from their domain.
    - For empty cells, initialize their domain to [1, 2, 3, 4, 5, 6, 7, 8, 9].
  - **Apply Arc Consistency:** Iteratively enforce arc consistency on all arcs until no further changes can be made.
    - For each arc (Xi, Xj): Revise - check if there is a consistent value in the domain of Xj for each value in the domain of Xi. If inconsistent, remove the inconsistent value from the domain of Xi. Repeat for all arcs.
  - **Update Sudoku Grid:** After applying arc consistency, update the Sudoku grid based on the reduced domains.
    - For each cell with a singleton domain, assign that value to the cell.
  - **Repeat:** Continue the process of enforcing arc consistency and updating the Sudoku grid until no more changes can be made and the board is filled.

## How to Run

1. **Compile the Code:**
   ```bash
   gcc sudoku_solver.c -o merv_gui
   ```

2. **Run the Executable:**
   ```bash
   ./sudoku_solver
   ```

3. **Follow the On-screen Instructions in GUI Mode.**

---

Feel free to customize this template based on any additional information or details specific to your project.
