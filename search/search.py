# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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
        successor to the current state, 'action' is the action
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

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    import util
    
    currentState=problem.getStartState()
    stack = util.Stack()
    hashset = {}
    curpath= []
    hashset[currentState]=curpath
    while(problem.isGoalState(currentState) is False):
        templist = problem.getSuccessors(currentState)
        for state in templist:
            try:
                hashset[state[0]]
                hashset[state[0]]= curpath + [state[1]]
            except:
                stack.push(state[0])
                hashset[state[0]]= curpath + [state[1]]
                #print "pushing",state[0]
                #print "path", hashset[state[0]]
                
        currentState= stack.pop()
        #print "popping",currentState
        curpath = hashset[currentState]
    
    return hashset[currentState]
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    import util
    
    currentState=problem.getStartState()
    stack = util.Queue()
    hashset = {}
    curpath= []
    hashset[currentState]=curpath
    while(problem.isGoalState(currentState) is False):
        templist = problem.getSuccessors(currentState)
        #print "list of successors", templist
        for state in templist:
            try:
                hashset[state[0]]
            except:
                stack.push(state[0])
                #print "pushing",state[0]
                hashset[state[0]]= curpath+[state[1]]
                
        currentState= stack.pop()
        curpath = hashset[currentState]
    
    return hashset[currentState]

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    import util
    currentState=problem.getStartState()
    hashmap = {}
    curpath= []
    pathcost = 0
    hashmap[currentState]= [curpath, pathcost]
    def cost(state):
        tempcost = 0
        return hashmap[state][1]
    queue = util.PriorityQueueWithFunction(cost)
    
    while(problem.isGoalState(currentState) is False):
        templist = problem.getSuccessors(currentState)
        for state in templist:
            try:
                hashmap[state[0]]
                if (pathcost + state[2]< hashmap[state[0]][0]):
                   hashmap[state[0]]=[curpath + [state[1]], pathcost + state[2]]
            except:
                
                hashmap[state[0]]= [curpath + [state[1]], pathcost + state[2]]
                queue.push(state[0])
                
        currentState= queue.pop()
        curpath = hashmap[currentState][0]
        pathcost = hashmap[currentState][1]
    
    return hashmap[currentState][0]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    import util
    currentState=problem.getStartState()
    hashmap = {}
    curpath= []
    pathcost = 0
    hashmap[currentState]= [curpath, pathcost]

    def cost(state):
        #print "cost:", hashmap[state][1], "heuristic value:", heuristic(state, problem),"total:",hashmap[state][1]+ heuristic(state, problem)
        return hashmap[state][1]+ heuristic(state, problem)

    queue = util.PriorityQueueWithFunction(cost)
    
    while(problem.isGoalState(currentState) is False):
        templist = problem.getSuccessors(currentState)
        #print templist
        for state in templist:
            try:
                hashmap[state[0]]
                if (pathcost + state[2]< hashmap[state[0]][1]):
                    #print "path optimized state:", state[0], "old cost:", hashmap[state[0]][0], "new cost:",pathcost + state[2]
                    hashmap[state[0]]=[curpath + [state[1]], pathcost + state[2]]
                    queue.push(state[0])
            except:
                
                hashmap[state[0]]= [curpath + [state[1]], pathcost + state[2]]
                queue.push(state[0])
                #print "pushing state", state[0], "with path",curpath + [state[1]],"and cost", pathcost + state[2]
                
        currentState= queue.pop()
        #print "popped",currentState

        curpath = hashmap[currentState][0]
        pathcost = hashmap[currentState][1]
    
    return hashmap[currentState][0]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
