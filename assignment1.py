# Name this file to assignment1.py when you submit
import pandas as pd
from queue import PriorityQueue

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
    # filepath is the path to a CSV file containing a grid 
    enviroment = pd.read_csv(filepath, header=None).values.tolist()
    walls = []
    treasures = {}  
    locationOfStart = None
    locationOfGoal = None

    # Looks through and finds all none-basic squares
    for row in range(len(enviroment)):
        for col in range(len(enviroment[row])):
            cell = str(enviroment[row][col]).strip()
            if cell == "S":
                locationOfStart = (row, col)
            elif cell == "X":
                walls.append((row, col))
            elif cell == "G":
                locationOfGoal = (row, col)
            else:
                val = int(cell)
                if val >= 1:
                    treasures[(row, col)] = val

    if locationOfStart is None or locationOfGoal is None:
        raise ValueError("Missing start or goal location")

    # Heuristic
    def calculateHeuristic(row, col):
        goalRow, goalCol = locationOfGoal
        return abs(row - goalRow) + abs(col - goalCol)

    edgeWeight = 1
    solution = False
    num_states_explored = 0

    frontierNum = 0
    frontier = PriorityQueue()
    frontierList = []
    explored = set()

    row, col = locationOfStart
    explorationNode = {
        "location": (row, col, 0),  
        "parent": -1,
        "pathCost": 0,
        "treasures": 0,
        "collected": set()
    }

    #f(n) = g(n) + h(n)
    f_start = explorationNode["pathCost"] + calculateHeuristic(row, col)
    frontier.put((f_start, frontierNum))
    frontierList.append(explorationNode)
    frontierNum += 1

    while not solution and not frontier.empty():
        fn, curNodeFrontierLoc = frontier.get()
        currentNode = frontierList[curNodeFrontierLoc]

        # Debugging - track frontier pops and node detailss
        print("Frontier popped:", (fn, curNodeFrontierLoc)) # f(n) value and index of node in frontierList
        print("Node details:", currentNode) # location (row, col, treasure), path cost, parent index, colelcted treasure cells
        print()

        goalRow, goalCol = locationOfGoal
        row, col, curTreasures = currentNode['location']
        explored.add((row, col, curTreasures))
        num_states_explored += 1

        if (row, col) == (goalRow, goalCol) and curTreasures >= 5:
            solution = True
            break

        # Check neighbors and skip walls or out-of-bounds cells    
        for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
            newRow, newCol = row + dr, col + dc
            if not (0 <= newRow < len(enviroment) and 0 <= newCol < len(enviroment[0])):
                continue
            if (newRow, newCol) in walls:
                continue

            newCollected = set(currentNode["collected"])  
            if (newRow, newCol) in treasures and (newRow, newCol) not in newCollected:
                newTreasure = curTreasures + treasures[(newRow, newCol)]
                newCollected.add((newRow, newCol))
            else:
                newTreasure = curTreasures

            explorationNode = {
                "location": (newRow, newCol, newTreasure),
                "parent": curNodeFrontierLoc,
                "pathCost": currentNode["pathCost"] + edgeWeight,
                "treasures": newTreasure,
                "collected": newCollected
            }

            state_id = (newRow, newCol, newTreasure)
            if state_id in explored:
                continue

            g = explorationNode["pathCost"]
            h = calculateHeuristic(newRow, newCol)
            frontier.put((g + h, frontierNum))
            frontierList.append(explorationNode)
            frontierNum += 1

    if not solution:
        raise RuntimeError("No valid path found")

    # Reconstruct path
    optimal_path = []
    optimal_path_cost = currentNode["pathCost"]
    while currentNode['parent'] != -1:
        r, c, _ = currentNode['location']
        optimal_path.append((r, c))
        currentNode = frontierList[currentNode['parent']]
    r, c, _ = currentNode['location']
    optimal_path.append((r, c))
    optimal_path.reverse()

    # Visual grid printout
    grid_copy = [row[:] for row in enviroment]
    for (r, c) in optimal_path:
        if grid_copy[r][c] not in ["S", "G"]:
            grid_copy[r][c] = "*"

    print("\nGrid with path:")
    for row in grid_copy:
        print(" ".join(str(cell).rjust(2) for cell in row))
    print("---------")

    return optimal_path, optimal_path_cost, num_states_explored


print(pathfinding("./Examples/Examples/Example0/grid.txt"))
print("---------")
print(pathfinding("./Examples/Examples/Example1/grid.txt"))
print("---------")
print(pathfinding("./Examples/Examples/Example2/grid.txt"))
print("---------")
print(pathfinding("./Examples/Examples/Example3/grid.txt"))
print("---------")

# Debugging - Test Cases

# Test cases - all 4 examples
# if __name__ == "__main__":
#     for i in range(4):
#         result = pathfinding(f"./Examples/Examples/Example{i}/grid.txt")
#         print(f"Example{i} Result:")
#         print("Path:", result[0])
#         print("Cost:", result[1])
#         print("States Explored:", result[2])
#         print("---------")

        
# Test cases - single example
# if __name__ == "__main__":
#     result = pathfinding("./Examples/Examples/Example0/grid.txt")
#     print("Example2 Result:")
#     print("Path:", result[0])
#     print("Cost:", result[1])
#     print("States Explored:", result[2])
#     print("---------")
