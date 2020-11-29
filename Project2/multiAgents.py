# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        "*** YOUR CODE HERE ***"
        ghostsPos = successorGameState.getGhostPositions()

        # Variable eval keeps score to return
        eval = 0
        
        # If successor state is Pacman eating food, increase points
        if ( currentGameState.getNumFood() > successorGameState.getNumFood() ):
            eval += 100

        # If Pacman is not moving, decrease points
        if action == Directions.STOP:
            eval -= 1000
        
        # Find the closest food and substract the distance from eval (multiple with 2 for better results)
        foodDist = []
        for food in newFood.asList():
            foodDist.append(util.manhattanDistance(newPos, food))
        if len(foodDist):
            eval += (-2)*min(foodDist)

        # Find the closest ghost and add the distance to eval
        ghostsDist = []
        for ghost in ghostsPos:
            ghostsDist.append(util.manhattanDistance(newPos, ghost))
        # If the ghost is too close, avoid
        if min(ghostsDist) < 2:
            return float("-inf")
        eval += min(ghostsDist)

        # If pacman's new position is to eat capsule, increase eval
        if newPos in currentGameState.getCapsules():
            eval += 1000
    
        return eval

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # minimax returns a list: [action, evaluation]
        return self.minimax(gameState, 0, 0)[0]

    def minimax(self, state, depth, agentIndex):
        # If agentIndex overcomes number of agents, reset agentIndex and increase depth
        if agentIndex >= state.getNumAgents():
            depth += 1
            agentIndex = 0

        # If cut-off-test is true, call evaluation function
        if depth == self.depth or state.isWin() or state.isLose(): return self.evaluationFunction(state)

        # List of legal actions for agent
        agentActions = state.getLegalActions(agentIndex)
        # Make sure agentActions is not empty
        if not agentActions: return self.evaluationFunction(state)

        # If agent is Pacman (MAX player)
        if agentIndex == 0:
            # Initialize action and maxEval
            [a, maxEval] = [agentActions[0], float("-inf")]
        
            for action in agentActions:
                # Call minimax with generated state and increased agentIndex
                minimaxVal = self.minimax(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)

                if type(minimaxVal) is list: evaluation = minimaxVal[1]
                else: evaluation = minimaxVal

                if evaluation > maxEval:
                    maxEval = evaluation
                    a = action

            return [a, maxEval]

        # If agent is Ghost (MIN player)
        else:
            # Initialize action and minEval
            [a, minEval] = [agentActions[0], float("inf")]

            for action in agentActions:
                # Call minimax with generated state and increased agentIndex
                minimaxVal = self.minimax(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)

                if type(minimaxVal) is list: evaluation = minimaxVal[1]
                else: evaluation = minimaxVal

                if evaluation < minEval:
                    minEval = evaluation
                    a = action

            return [a, minEval]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # alphaBeta returns a list: [action, evaluation]
        return self.alphaBeta(gameState, 0, 0, float("-inf"), float("inf"))[0]
    
    def alphaBeta(self, state, depth, agentIndex, a, b):
        # If agentIndex overcomes number of agents, reset agentIndex and increase depth
        if agentIndex >= state.getNumAgents():
            depth += 1
            agentIndex = 0

        # If cut-off-test is true, call evaluation function
        if depth == self.depth or state.isWin() or state.isLose(): return self.evaluationFunction(state)

        # If agent is Pacman (MAX player), call maxValue function
        elif agentIndex == 0: return self.maxValue(state, depth, agentIndex, a, b)

        # If agent is Ghost (MIN player), call minValue function
        else: return self.minValue(state, depth, agentIndex, a, b)
    
    def maxValue(self, state, depth, agentIndex, a, b):
        # List of legal actions for agent
        agentActions = state.getLegalActions(agentIndex)

        # Make sure agentActions is not empty
        if not agentActions: return self.evaluationFunction(state)

        # Initialize action and maxEval
        [action, maxEval] = [agentActions[0], float("-inf")]
        
        for agentAction in agentActions:
            # Call alphaBeta with generated state and increased agentIndex
            abVal = self.alphaBeta(state.generateSuccessor(agentIndex, agentAction), depth, agentIndex + 1, a, b)

            # Check type of returned value of alphaBeta
            if type(abVal) is list: evaluation = abVal[1]
            else: evaluation = abVal

            if evaluation > maxEval:
                maxEval = evaluation
                action = agentAction
            
            if maxEval > b:
                return [action, maxEval]

            a = max(a, maxEval)

        return [action, maxEval]

    def minValue(self, state, depth, agentIndex, a, b):
        # List of legal actions for ghost
        ghostActions = state.getLegalActions(agentIndex)

        # Make sure ghostActions is not empty
        if not ghostActions: return self.evaluationFunction(state)

        # Initialize action and maxEval
        [action, minEval] = [ghostActions[0], float("inf")]

        for agentAction in ghostActions:
            # Call alphaBeta with generated state and increased agentIndex
            abVal = self.alphaBeta(state.generateSuccessor(agentIndex, agentAction), depth, agentIndex + 1, a, b)

            # Check type of returned value of alphaBeta
            if type(abVal) is list: evaluation = abVal[1]
            else: evaluation = abVal

            if evaluation < minEval:
                minEval = evaluation
                action = agentAction

            if minEval < a:
                return [action, minEval]

            b = min(b, minEval)

        return [action, minEval]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # expectimax returns a list: [action, evaluation]
        return self.expectimax(gameState, 0, 0)[0]
    
    def expectimax(self, state, depth, agentIndex):
        # If agentIndex overcomes number of agents, reset agentIndex and increase depth
        if agentIndex >= state.getNumAgents():
            depth += 1
            agentIndex = 0

        # If cut-off-test is true, call evaluation function
        if depth == self.depth or state.isWin() or state.isLose(): return self.evaluationFunction(state)

        # List of legal actions for agent
        agentActions = state.getLegalActions(agentIndex)
        # Make sure agentActions is not empty
        if not agentActions: return self.evaluationFunction(state)

        # If agent is Pacman (MAX player)
        if agentIndex == 0:
            # Initialize action and maxEval
            [a, maxEval] = [agentActions[0], float("-inf")]
        
            for action in agentActions:
                # Call expectimax with generated state and increased agentIndex
                expectimaxVal = self.expectimax(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)

                if type(expectimaxVal) is list: evaluation = expectimaxVal[1]
                else: evaluation = expectimaxVal

                if evaluation > maxEval:
                    maxEval = evaluation
                    a = action

            return [a, maxEval]

        # If agent is Ghost (MIN player)
        else:
            # Initialize Eval and probability
            Eval = 0
            probability = 1/len(agentActions)

            for action in agentActions:
                # Call expectimax with generated state and increased agentIndex
                expectimaxVal = self.expectimax(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)

                if type(expectimaxVal) is list: evaluation = expectimaxVal[1]
                else: evaluation = expectimaxVal

                Eval += probability*evaluation
                a = action

            return [a, Eval]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: foodscore, ghostscore, scaredTimes
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    # newScaredTimes holds the number of moves that each ghost will remain 
    # scared because of Pacman having eaten a power pellet.
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Check for winning and losing states
    if currentGameState.isLose(): return float("-inf")
    elif currentGameState.isWin(): return float("inf")

    # Initialize eval to current score in the game
    eval = scoreEvaluationFunction(currentGameState)

    # Find the total food distances and add the inverse number to eval
    foodDist = 0
    for food in newFood.asList():
        foodDist += util.manhattanDistance(newPos, food)
    eval += 1.0/foodDist

    # Find the distance of ghost and Pacman
    for ghostState in newGhostStates:
        distance = util.manhattanDistance(newPos, ghostState.getPosition())
        # If ghost is active (is not scared) and it is too close to Pacman (distance < 3),
        # substract the inverse distance to eval
        if not ghostState.scaredTimer and distance < 3:
            eval -= 1.0/distance
        # If ghost is scared and the number of moves that it will remain scared is less than distance,
        # add the inverse distance to eval
        elif ghostState.scaredTimer < distance:
            eval += 1.0/distance
    
    # If Pacman has eaten a power pellet, add 100 points to eval
    if newScaredTimes[0] > 0:
        eval += 100

    return eval

# Abbreviation
better = betterEvaluationFunction
