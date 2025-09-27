# Name this file to assignment1.py when you submit
import pandas as pd
from queue import PriorityQueue

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  # filepath is the path to a CSV file containing a grid 
  enviroment = pd.read_csv(filepath, header=None).values.tolist()
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
        
  def calculateHeuristic(x, y):
    (r1, c1) = x, y
    (r2, c2) = locationOfGoal
    return abs(r1 - r2) + abs(c1 - c2)
  
  edgeWeight = 1
  solution = False
  num_states_explored = 0

  frontier = PriorityQueue()
  explored = []

  x,y = locationOfStart
  treasures = 0
  explorationNode = {"location":(x,y,treasures), 
                     "parent": None, 
                     "pathCost":0,
                     "treasures": 0
                    }

  #f(n) = g(n) + h(n)
  f_start = explorationNode["pathCost"] + calculateHeuristic(*locationOfStart)
  frontier.put(0, explorationNode)

  while (not solution):
    currentNode = frontier.get()
    if (currentNode['location'] == locationOfGoal and currentNode['treasures'] >= 5):
      solution = True
      break

    x,y,curTreasures = currentNode['location']
    g = edgeWeight + calculateHeuristic(x, y)

    for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
      newX, newY = x + dx, y + dy
      # do we need to check anything like the if the neighbor is possibly a wall?
      if !(0 <= newX < len(environment[0]) and 0 <= newY < len(enviroment)):
        continue
      elif (newX,newY) in walls:
        continue

      if (newX,newY) != locationOfGoal or (newX,newY) != locationOfStart:
        newTreasure = curTreasures + enviroment[newY][newX]
      else
        newTreasure = curTreasures

      explorationNode = {"location": (newX, newY, newTreasures),
                         "parent":currentNode, 
                         "pathCost":(currentNode["pathCost"]+edgeWeight),
                         "treasures": newTreasure
                        }
      
      #### Need a Valid Sytax For this ####
      if any(location['location'] == explorationNode["location"] for (g,location) in frontier):
        if explorationNode['pathCost'] < location['pathCost']:
          #  Update the priority queue
        continue
      
      if explorationNode in explored:
        continue
      
      frontier.put((g, explorationNode))
    
    explored.append(currentNode)
    
    num_states_explored += 1


  optimal_path = []
  optimal_path_cost = currentNode["pathCost"]

  # Follows The Parents Backwards to Find Optimal_Path 
  while (currentNode['location'] != None):
    optimal_path.append(currentNode['location'])
    currentNode = currentNode['parent']#getParent

  # Maybe need to reverse optimal_path


  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored






pathfinding("./Examples/Examples/Example0/grid.txt")