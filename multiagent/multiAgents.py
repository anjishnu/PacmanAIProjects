# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        


        minGhostDistance = 100000
        minFoodDistance = 10000


        for foodPos in newFood.asList():
            minFoodDistance =  min(minFoodDistance,util.manhattanDistance(newPos,foodPos))
            
        
        
        for GhostState in newGhostStates:
            minDistance =  min(minGhostDistance, util.manhattanDistance(newPos, GhostState.getPosition()))

        if (successorGameState.getNumFood()==0):
            return 10000

        # 1200+ average, 0 fails, 10 trials
        #return (currentGameState.getNumFood()-successorGameState.getNumFood())*150 - 10*minFoodDistance - 50/(minDistance+0.0001) + successorGameState.getScore()

        return (currentGameState.getNumFood()-successorGameState.getNumFood())*150 - 10*minFoodDistance - 50/(minDistance+0.0001) + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        
        #print "number of agents",gameState.getNumAgents()

        #print("final action",self.getActionOfDepth (gameState, self.depth))
        return self.getActionOfDepth (gameState, self.depth)[0]


    def getActionOfDepth(self, gameState, depth):
         #print ("pacman active, depth is", depth, 'gameState is',gameState)

         if(gameState.isWin()==True or gameState.isLose()==True):
            return self.evaluationFunction(gameState)

                 
         pacmanActions=gameState.getLegalActions(0)
         #print "pacman legal actions",pacmanActions
         pacmanStates = [gameState.generateSuccessor(0, action) for action in pacmanActions]
         #print "pacmanStates", pacmanStates
         ActionResults= [self.ghostAction(State, gameState.getNumAgents()-1,depth) for State in pacmanStates]


         #print("pacman choices",ActionResults)
         index = ActionResults.index(max(ActionResults))

         #print pacmanActions [index], min(ActionResults)
         
         return pacmanActions[index], ActionResults[index]

    def ghostAction(self,gameState, maxGhostNum, depth, curGhostNum=1):

        #print("ghost number",curGhostNum,"depth", depth, "is active")

        if(gameState.isWin()==True or gameState.isLose()==True):
            return self.evaluationFunction(gameState)

        ghostActions = gameState.getLegalActions(curGhostNum)
        #print "ghostActions", ghostActions
        #print ("max ghost", maxGhostNum, "currentGhost", curGhostNum, ghostActions, "depth", depth)
        ghostStates = [gameState.generateSuccessor(curGhostNum,action) for action in ghostActions]
        #print "ghostStates", ghostStates
        
        if (curGhostNum==maxGhostNum):
            if (depth==1):
                values = [self.evaluationFunction(state) for state in ghostStates]
                #print "values", values
                index = values.index(min(values))
            else:
                values = [self.getActionOfDepth(state, depth-1) for state in ghostStates]
                #print ("values2",values)
                temp = []
                for itr in values:
                    if type(itr) == tuple:
                        #print "itr",itr
                        temp = temp + [itr[1]]
                    else:
                        temp = temp + [itr]
                values = temp
                #print("reformed values", values)
                #print "min is",(min(values))
                index = values.index(min(values))
            #print("Discovered node:",values[index])
            #print ("ghost",curGhostNum, "choices", values, "depth", 1)
            return values[index]

        else:
            #print ("Nextghostactivating")
            values = [self.ghostAction(state, maxGhostNum, depth, curGhostNum+1) for state in ghostStates]
            #print ("ghost",curGhostNum, "choices", values)
            return min(values)

                    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
  
        alpha = -10000000
        beta = 10000000
        

        def maxAction(gameState, alpha,beta,depth):
            #for PACMAN
            Val = -1000000
            actionToTake = None
            
            if(gameState.isWin()==True or gameState.isLose()==True):
                return self.evaluationFunction(gameState)

            pacmanActions=gameState.getLegalActions(0)
            
            for action in pacmanActions:
                 tempState = gameState.generateSuccessor(0,action)
                 #print "states generated", tempState.state, alpha, beta
                 tval = minAction(tempState,alpha,beta,depth)
                 if (tval>Val):
                     Val = tval
                     if tval>alpha:
                         alpha = tval
                     actionToTake = action
                 if (Val> beta):
                     break
             
            return Val, actionToTake


        def minAction(gameState, alpha, beta, depth, curGhostNum=1):
            #for ghosts
            if(gameState.isWin()==True or gameState.isLose()==True):
                return self.evaluationFunction(gameState)

            Val = 100000
            ghostActions = gameState.getLegalActions(curGhostNum)
            if (curGhostNum == gameState.getNumAgents()-1):
                if (depth==1):     
                    for action in ghostActions:
                        tempState = gameState.generateSuccessor(curGhostNum,action)
                        tval = self.evaluationFunction(tempState)
                        if (tval<Val):
                            Val = tval
                            if tval<beta:
                                beta = tval
                        if (Val<alpha):
                            break
                    return Val
                else:
                    for action in ghostActions:
                        tempState = gameState.generateSuccessor(curGhostNum,action)
                        tval = maxAction(tempState, alpha, beta, depth-1)
                        if type(tval)==tuple:
                            tval = tval[0]
                        if (tval<Val):
                            Val = tval
                            if tval<beta:
                                beta = tval
                        if (Val<alpha):
                            break
                    return Val
            else:
                for action in ghostActions:
                        tempState = gameState.generateSuccessor(curGhostNum,action)
                        tval = minAction(tempState, alpha, beta, depth, curGhostNum+1)
                        if (tval<Val):
                            Val = tval
                            if tval<beta:
                                beta = tval
                        if (Val<alpha):
                            break
                return Val
        return maxAction(gameState,alpha,beta,self.depth)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def mean (self,lst):
	sum = 0
	for element in lst:
		sum = sum+element
	return sum/len(lst)
    
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.getActionOfDepth (gameState, self.depth)[0]


    def getActionOfDepth(self, gameState, depth):
         if(gameState.isWin()==True or gameState.isLose()==True):
            return self.evaluationFunction(gameState)

         pacmanActions=gameState.getLegalActions(0)
         pacmanStates = [gameState.generateSuccessor(0, action) for action in pacmanActions]

         ActionResults= [self.ghostAction(State, gameState.getNumAgents()-1,depth) for State in pacmanStates]
         index = ActionResults.index(max(ActionResults))

         return pacmanActions[index], ActionResults[index]

    def ghostAction(self,gameState, maxGhostNum, depth, curGhostNum=1):

        if(gameState.isWin()==True or gameState.isLose()==True):
            return self.evaluationFunction(gameState)

        ghostActions = gameState.getLegalActions(curGhostNum)
        ghostStates = [gameState.generateSuccessor(curGhostNum,action) for action in ghostActions]
        
        if (curGhostNum==maxGhostNum):
            if (depth==1):
                values = [self.evaluationFunction(state) for state in ghostStates]
                
            else:
                values = [self.getActionOfDepth(state, depth-1) for state in ghostStates]
                temp = []
                for itr in values:
                    if type(itr) == tuple:
                        temp = temp + [itr[1]]
                    else:
                        temp = temp + [itr]
                values = temp
            return self.mean(values)

        else:
            values = [self.ghostAction(state, maxGhostNum, depth, curGhostNum+1) for state in ghostStates]
            return self.mean(values)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    minGhostDistance = 100000
    minFoodDistance = 100000
    #print dir(currentGameState)
    sumScaredTimes= 0
    for scaredTimes in newScaredTimes:
        sumScaredTimes= sumScaredTimes +scaredTimes
    
    for foodPos in newFood.asList():
        minFoodDistance =  min(minFoodDistance,util.manhattanDistance(newPos,foodPos))
                  
    for GhostState in newGhostStates:
        minDistance =  min(minGhostDistance, util.manhattanDistance(newPos, GhostState.getPosition()))

    if (successorGameState.getNumFood()==0):
        return 10000

    
    def winning():
        if currentGameState.isWin():
            return 1000000
            moves = currentGameState.getLegalPacmanActions()
            for move in moves:
                if currentGameState.generatePacmanSuccessor(move).isWin():
                    return 500000
        else:
            return 0
    x= (-successorGameState.getNumFood())*250 - 25*minFoodDistance - 1/(minDistance+0.00001) + successorGameState.getScore() + sumScaredTimes + winning()

    
    return x


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

