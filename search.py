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

    """
    if start is goal state, return
    if not, add start and its total cost to PQ
    check if its successors are goal states
    if not, add successors to fringePQ

    While fringePQ is not empty
        pop off the first node (each node is (state, full path))
        check goal state of all successors, 
        add all of them to PQ: item, Priority,
        item = (action, path), Priority = cost
    """
    
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    path = []
    if problem.isGoalState(startState):
        return path
    startSuccessors = problem.getSuccessors(startState)
    explored = Set([startState])
    for eachS in startSuccessors:
        if problem.isGoalState(eachS[0]):
            return eachS[1]
        node = (eachS[0], eachS[1]) #state, action
        #print "eachS 193 is: %s"%(eachS,)-->  eachS 193 is: ((33, 16), 'West', 1)
        #print "node 194 is:%s"%(node,) -->  node 194 is:((33, 16), 'West')
        tempPath = []
        tempPath.append(node[1])
        #print "tempPath is: %s"%(tempPath,)
        totalCost = problem.getCostOfActions(tempPath)
        #print "total cost: %d"%(totalCost)
        fringe.push(node, totalCost)

    while not fringe.isEmpty():
        newNode = fringe.pop()
        # print "newNode:%s"%(newNode,) -->  newNode:((34, 15), 'South')
        allSuccessors = problem.getSuccessors(newNode[0])
        explored.add(newNode[0])
        for each in allSuccessors:
            if problem.isGoalState(each[0]):
                return each[1]
            else:
                if each[0] not in explored:
                    tempNode = (each[0], each[1])
                    tempPath = []
                    tempPath.append(each[1])
                    tempPath.append(node[1])
                    print "tempPath is: %s"%(tempPath,)
                    # print "tempNode is: %s, %s"%(tempNode[0], tempNode[1])
                    totalCost = problem.getCostOfActions(tempPath)
                    print "total cost: %d"%(totalCost)
                    fringe.push(tempNode, totalCost) #make sure no explored node is pushed
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
