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
        locationOfStart = (element, row)
      elif(enviroment[row][element] == "X"):
        walls.append((element, row))
      elif(enviroment[row][element] == "G"):
        locationOfGoal = (element, row)
      elif(int(enviroment[row][element]) >= 1):
        treasures.append((element, row))

  def calculateHeuristic(x, y):
    (r1, c1) = x, y
    (r2, c2) = locationOfGoal
    return abs(r1 - r2) + abs(c1 - c2)
  
  edgeWeight = 1
  solution = False
  num_states_explored = 0

  frontierNum = 0
  frontier = PriorityQueue()
  frontierList = []
  explored = []

  x,y = locationOfStart
  treasures = 0
  explorationNode = {"location":(x,y,treasures), 
                     "parent": -1, 
                     "pathCost":0,
                     "treasures": 0
                    }

  #f(n) = g(n) + h(n)
  f_start = explorationNode["pathCost"] + calculateHeuristic(x, y)
  frontier.put((0, frontierNum))
  frontierList.append(explorationNode)
  frontierNum += 1

  while (not solution):
    fn, curNodeFrontierLoc = frontier.get()
    currentNode = frontierList[curNodeFrontierLoc]
    goalX, goalY = locationOfGoal
    x,y,curTreasures = currentNode['location'] 
    if ((x, y) == (goalX, goalY) and curTreasures >= 5):
      solution = True
      break

    
    g = edgeWeight + calculateHeuristic(x, y)

    for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
      newX, newY = x + dx, y + dy
      # do we need to check anything like the if the neighbor is possibly a wall?
      if not (0 <= newX < len(enviroment[0]) and 0 <= newY < len(enviroment)):
        continue
      elif (newX,newY) in walls:
        continue

      if (newX,newY) != locationOfGoal and (newX,newY) != locationOfStart:
        newTreasure = curTreasures + int(enviroment[newY][newX])
      else:
        newTreasure = curTreasures

      explorationNode = {"location": (newX, newY, newTreasure),
                         "parent": curNodeFrontierLoc, 
                         "pathCost":(currentNode["pathCost"]+edgeWeight),
                         "treasures": newTreasure
                        }
      
      #### Need a Valid Sytax For this ####
      for location in frontierList:
        if (location['location'] == explorationNode['location']):
          if explorationNode['pathCost'] < location['pathCost']:
            location['pathCost'] = explorationNode['pathCost']
          continue
      
      if any(location['location'] == explorationNode['location'] for location in explored):
        continue
      
      frontier.put((g, frontierNum))
      frontierList.append(explorationNode)
      frontierNum += 1

    explored.append(currentNode)
    num_states_explored += 1
    

  print(currentNode)
  print(num_states_explored)
  w = 0
  for item in frontierList:
    print(str(w) + ": " + str(item))
    w += 1
  optimal_path = []
  optimal_path_cost = currentNode["pathCost"]

  # Follows The Parents Backwards to Find Optimal_Path 
  while (currentNode['parent'] != -1):
    x,y, treasure = currentNode['location']
    optimal_path.append((x,y))
    currentNode = frontierList[currentNode['parent']]#getParent

  x,y, treasure = currentNode['location']
  optimal_path.append((x,y))

  optimal_path.reverse()


  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored






print(pathfinding("./Examples/Examples/Example0/grid.txt"))
print("---------")
print(pathfinding("./Examples/Examples/Example1/grid.txt"))
print("---------")
print(pathfinding("./Examples/Examples/Example2/grid.txt"))
print("---------")
print(pathfinding("./Examples/Examples/Example3/grid.txt"))
print("---------")




















