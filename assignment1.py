# Name this file to assignment1.py when you submit
import pandas as pd
from queue import PriorityQueue

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
    # filepath is the path to a CSV file containing a grid 
    environment = pd.read_csv(filepath, header=None).values.tolist()
    walls = []
    treasures = {}  
    locationOfStart = None
    goals = []  

    # Looks through and finds all none-basic squares
    for row in range(len(environment)):
        for col in range(len(environment[row])):
            cell = str(environment[row][col]).strip()
            if cell == "S":
                locationOfStart = (row, col)
            elif cell == "X":
                walls.append((row, col))
            elif cell == "G":
                goals.append((row, col))  
            else:
                val = int(cell)
                if val >= 1:
                    treasures[(row, col)] = val

    if locationOfStart is None or len(goals) == 0: 
        raise ValueError("Missing start or goal location")

    # Heuristic - Euclidean 
    def calculateHeuristic(row, col):
        return min(((row - goalRow)**2 + (col - goalCol)**2)**0.5 for goalRow, goalCol in goals)

    solution = False
    num_states_explored = 0

    frontierNum = 0
    frontier = PriorityQueue()
    frontierList = []
    
    explored = set()
    best_g = {}

    # Initialize starting node
    row, col = locationOfStart
    startNode = {
        "location": (row, col, 0),  
        "parent": -1,
        "pathCost": 0,
        "treasures": 0,
        "collected": set()
    }

    # Add start node to frontier
    #f(n) = g(n) + h(n)
    f_start = startNode["pathCost"] + calculateHeuristic(row, col)
    frontier.put((f_start, frontierNum))
    frontierList.append(startNode)
    best_g[(row, col, 0)] = 0
    frontierNum += 1

    # A* search loop
    while not solution and not frontier.empty():
        fn, curNodeFrontierLoc = frontier.get()
        currentNode = frontierList[curNodeFrontierLoc]

        # Debugging - track frontier pops and node detailss
        # print("Frontier popped:", (fn, curNodeFrontierLoc)) # f(n) value and index of node in frontierList
        # print("Node details:", currentNode) # location (row, col, treasure), path cost, parent index, colelcted treasure cells
        # print()

        row, col, curTreasures = currentNode['location']
        explored.add((row, col, frozenset(currentNode["collected"])))
        num_states_explored += 1

        # Check if goal reached with sufficient treasure
        if (row, col) in goals and curTreasures >= 5:  
            solution = True
            break

        # Explore neighbors (up, right, down, left)    
        for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
            newRow, newCol = row + dr, col + dc

            # Skip out-of-bounds or walls
            if not (0 <= newRow < len(environment) and 0 <= newCol < len(environment[0])):
                continue
            if (newRow, newCol) in walls:
                continue

            # Update treasure collection
            newCollected = set(currentNode["collected"])  
            if (newRow, newCol) in treasures and (newRow, newCol) not in newCollected:
                newTreasure = curTreasures + treasures[(newRow, newCol)]
                newCollected.add((newRow, newCol))
            else:
                newTreasure = curTreasures

            # Create successor node
            successorNode = {
                "location": (newRow, newCol, newTreasure),
                "parent": curNodeFrontierLoc,
                "pathCost": currentNode["pathCost"] + 1,
                "treasures": newTreasure,
                "collected": newCollected
            }

            state_id = (newRow, newCol, newTreasure)
            if state_id in explored:
                continue

            g = successorNode["pathCost"]

            # Skip if we have a better path to this state
            if state_id in best_g and g >= best_g[state_id]:
                continue
            best_g[state_id] = g

            # Add to frontier
            h = calculateHeuristic(newRow, newCol)
            frontier.put((g + h, frontierNum))
            frontierList.append(successorNode )
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
    grid_copy = [row[:] for row in environment]
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
