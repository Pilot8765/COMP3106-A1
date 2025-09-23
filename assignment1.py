# Name this file to assignment1.py when you submit
import pandas as pd
from queue import PriorityQueue

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  # filepath is the path to a CSV file containing a grid 
  enviroment = pd.read_csv(filepath, header=None).values.tolist()
  locationOfStart = None
  walls = []
  treasures = []

  # Looks through and finds all none-basic squares
  for row in range(len(enviroment)):
    for element in range(len(enviroment[row])):
      if(enviroment[row][element] == "S"):
        locationOfStart = (row, element)
      elif(enviroment[row][element] == "X"):
        walls.append((row, element))
      elif(enviroment[row][element] == "G"):
        locationOfGoal = (row, element)
      elif(int(enviroment[row][element]) >= 1):
        treasures.append((row, element))

  # DO we need to also determine if goal is not present in the grid??
  if locationOfStart is None:
    print("Grid must contain one S")
    return 0
    
  
  heuristic = 1 #Create Function to Calculate
  def heuristic(a,b):
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)
  edgeWeight = 1
  solution = False
  num_states_explored = 0

  frontier = PriorityQueue()
  explored = []

  explorationNode = {"location":locationOfStart, "parent": None, "pathCost":0, "g": heuristic}
  frontier.put(g, explorationNode)

  while (not solution):
    currentNode = frontier.get()
    if (currentNode['location'] == locationOfGoal):
      solution = True
      break
    x,y = currentNode['location']
    #Add Surroundings if not outside Bounds or Wall to Frontier (or already in with lower pathCost)

    explorationNode = {"location":,"parent":currentNode, "pathCost":(currentNode["pathCost"]+edgeWeight)}
    frontier.append(explorationNode)
    

    explored.append(currentNode)
    ++num_states_explored


  optimal_path_cost = currentNode["pathCost"]
  optimal_path.append(currentNode["location"])

  while (currentNode['location'] != None):
    currentNode = currentNode['parent']#getParent
    optimal_path.append(currentNode['location'])


  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored
def PriorityQueue():
  
  

pathfinding("./Examples/Examples/Example0/grid.txt")
