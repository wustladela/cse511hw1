# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor state to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    from sets import Set
    from game import Directions
    fringe = util.Stack()
    start = problem.getStartState()
    explored = Set([start])
    inFringe = Set([])
    path = []
    if problem.isGoalState(start):
        return path
    startSucc = problem.getSuccessors(start)
    for ssucc in startSucc:
        node = (ssucc[0], ssucc[1])
        fringe.push(node)
        inFringe.add(ssucc[0])
    while not fringe.isEmpty():
        leaf = fringe.pop()
        inFringe.remove(leaf[0])
        path = []
        if type(leaf[1]) == str:
            path = [leaf[1],]
        else:
            path = leaf[1]
        explored.add(leaf[0])
        if problem.isGoalState(leaf[0]):
            return path
        else:
            possMoves = problem.getSuccessors(leaf[0])
            for succ in possMoves:
                if succ[0] not in explored and succ[0] not in inFringe:
                    tempPath = list(path)
                    tempPath.append(succ[1])
                    node = (succ[0],tempPath)
                    fringe.push(node)
                    inFringe.add(succ[0])

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    from sets import Set
    from game import Directions
    fringe = util.Queue()
    start = problem.getStartState()
    explored = Set([start])
    path = []
    inFringe = Set([])
    if problem.isGoalState(start):
        return path
    startSucc = problem.getSuccessors(start)
    for ssucc in startSucc:
        node = (ssucc[0], ssucc[1])
        fringe.push(node)
        inFringe.add(ssucc[0])
    while not fringe.isEmpty():
        leaf = fringe.pop()
        inFringe.remove(leaf[0])
        path = []
        if type(leaf[1]) == str:
            path = [leaf[1],]
        else:
            path = leaf[1]
        explored.add(leaf[0])
        if problem.isGoalState(leaf[0]):
            return path
        else:
            possMoves = problem.getSuccessors(leaf[0])
            for succ in possMoves:
                if succ[0] not in explored and succ[0] not in inFringe:
                    tempPath = list(path)
                    tempPath.append(succ[1])
                    node = (succ[0],tempPath)
                    fringe.push(node)
                    inFringe.add(succ[0])
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least *total* cost first. "
    "*** YOUR CODE HERE ***"
    from sets import Set
    from game import Directions

    fringe = util.PriorityQueue()
    goalPQ = util.PriorityQueue()#solutions

    start = problem.getStartState()
    path = []
    ans = []
    counter = 0;
    ansNode = []
    inFringe = Set([])#closed set, meaning visited, to make sure the fringe has only unique nodes.
    if problem.isGoalState(start):
        return path

    startSucc = problem.getSuccessors(start)
    explored = [start]#expanded
    for ssucc in startSucc:
        node = (ssucc[0], ssucc[1])
        tempPath = list(path)
        tempPath.append(ssucc[1])
        totalCost = problem.getCostOfActions(tempPath)
        if node[0] not in inFringe and node[0] not in explored:
            fringe.push(node, totalCost)
            inFringe.add(ssucc[0])
    while not fringe.isEmpty():
        leaf = fringe.pop()
        inFringe.remove(leaf[0])
        path = []
        # set path to be total path so far
        if type(leaf[1]) == str:
            path = [leaf[1],]
        else:
            path = leaf[1]

        print "cost of leaf:"
        tempCost = problem.getCostOfActions(path)
        print tempCost
        print "----"
        minCost = 99968719479864
        if problem.isGoalState(leaf[0]):
            #return leaf[1]
            thisMinCost = problem.getCostOfActions(leaf[1])
            if thisMinCost < minCost:
                minCost = thisMinCost
            goalNode = (leaf[0], leaf[1])
            goalCost = problem.getCostOfActions(leaf[1])
            goalPQ.push(goalNode, goalCost)
        else:
            # check if we need to expand this leaf node
            leafCost = problem.getCostOfActions(path)
            if leaf[0] not in explored and leafCost < minCost:
                possMoves = problem.getSuccessors(leaf[0])
                explored.append(leaf[0])
                counter = counter+1
                for succ in possMoves:
                    if succ[0] not in explored and succ[0] not in inFringe:
                        tempPath = list(path)
                        tempPath.append(succ[1])
                        totalCost = problem.getCostOfActions(tempPath)
                        print "totalCost after tempPath:"
                        print totalCost
                        print "----"
                        if totalCost < minCost:
                            node = (succ[0],tempPath)
                            fringe.push(node, totalCost)
                            inFringe.add(succ[0])
    if not goalPQ.isEmpty():
        ansNode = goalPQ.pop()
        ans = ansNode[1]
    return ans
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    from sets import Set
    from game import Directions

    fringe = util.PriorityQueue()
    goalPQ = util.PriorityQueue()
    start = problem.getStartState()
    path = []
    ans = []
    ansNode = []
    inFringe = Set([])#closed set, meaning visited, to make sure the fringe has only unique nodes.
    if problem.isGoalState(start):
        return path

    startSucc = problem.getSuccessors(start)
    explored = Set([start])
    for ssucc in startSucc:
        node = (ssucc[0], ssucc[1])
        tempPath = list(path)
        tempPath.append(ssucc[1])
        totalCost = problem.getCostOfActions(tempPath)+nullHeuristic(ssucc[0])
        if node[0] not in inFringe:
            fringe.push(node, totalCost)
            inFringe.add(ssucc[0])
        #fringe: state, path, cost
        #loop through the priority queue
    while not fringe.isEmpty():
        # if len(inFringe) == 0:
        #     return [] #failure case????
        leaf = fringe.pop()
        inFringe.remove(leaf[0])
        path = []
        # set path to be total path so far
        if type(leaf[1]) == str:
            path = [leaf[1],]
        else:
            path = leaf[1]
        # set a minCost that will be the solution with min Cost for all
        minCost = 968719479864
        if problem.isGoalState(leaf[0]):
            thisMinCost = problem.getCostOfActions(leaf[1])+nullHeuristic(leaf[0])
            if thisMinCost < minCost:
                minCost = thisMinCost
                minNode = (leaf[0], leaf[1])
            goalNode = (leaf[0], leaf[1])
            goalCost = problem.getCostOfActions(leaf[1])+nullHeuristic(leaf[0])
            goalPQ.push(goalNode, goalCost)
        else:
            # check if we need to expand this leaf node.    
            leafCost = problem.getCostOfActions(path)
            if leaf[0] not in explored and leaf[0] not in inFringe and leafCost<minCost:

            #if leaf[0] not in explored:
                possMoves = problem.getSuccessors(leaf[0])
                explored.add(leaf[0])
                for succ in possMoves:
                    if succ[0] not in explored and succ[0] not in inFringe:
                        tempPath = list(path)
                        tempPath.append(succ[1])
                        totalCost = problem.getCostOfActions(tempPath)+nullHeuristic(succ[0])
                        if totalCost < minCost:
                            node = (succ[0],tempPath)
                            fringe.push(node, totalCost)
                            inFringe.add(succ[0]) #inFringe makes sure fringe is unique
    if not goalPQ.isEmpty():
        ansNode = goalPQ.pop()
        ans = ansNode[1]
    return ans
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
