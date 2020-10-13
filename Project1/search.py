# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    # Frontier as stack: initialize frontier with initial state (node, actions)
    frontier = util.Stack()                      
    frontier.push((problem.getStartState(), [])) 

    # Explored set to be empty
    explored = set()                             

    while True:
        # If the frontier is empty then return
        if frontier.isEmpty():
            return []

        # Choose a leaf node and remove it from the frontier
        node, actions = frontier.pop()

        # If the node contains a goal state then return the corresponding solution
        if problem.isGoalState(node):
            return actions

        # Add the state of the node to the explored set
        explored.add(node)                        

        # Expand the chosen node, adding the resulting nodes to the frontier # 
        # only if their state is not in the the explored set                 #
        successors = problem.getSuccessors(node)
        for nextNode, direction, stepCost in successors:
            if nextNode not in explored:
                frontier.push((nextNode, actions + [direction]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    # Frontier as FIFO Queue: initialize frontier with initial state (node, actions)
    frontier = util.Queue()                      
    frontier.push((problem.getStartState(), []))

    # Explored list to be empty
    explored = []                             

    while True:
        # If the frontier is empty then return
        if frontier.isEmpty():
            return []

        # Choose a leaf node and remove it from the frontier
        node, actions = frontier.pop()

        # If the node contains a goal state then return the corresponding solution
        if problem.isGoalState(node):
            return actions

        if node not in explored:
            # Add the state of the node to the explored set
            explored.append(node)

            # Expand the chosen node, adding the resulting nodes to the frontier # 
            # only if their state is not in the the explored set                 #
            successors = problem.getSuccessors(node)
            for nextNode, direction, stepCost in successors:
                if nextNode not in explored:
                    frontier.push((nextNode, actions + [direction]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Frontier as Priority Queue: initialize frontier with initial state (node, actions)
    frontier = util.PriorityQueue()                 
    frontier.push((problem.getStartState(), []), 0)

    # Explored set to be empty
    explored = set()                                

    while True:
        # If the frontier is empty then return
        if frontier.isEmpty():
            return []

        # Choose a leaf node and remove it from the frontier
        node, actions = frontier.pop()

        # If the node contains a goal state then return the corresponding solution
        if problem.isGoalState(node):
            return actions
        
        if node not in explored:
            # Add the state of the node to the explored set
            explored.add(node)

            # Expand the chosen node, adding the resulting nodes to the frontier # 
            # only if their state is not in the the explored set                 #
            successors = problem.getSuccessors(node)
            for nextNode, direction, stepCost in successors:
                if nextNode not in explored:
                    frontier.update((nextNode, actions + [direction]), problem.getCostOfActions(actions + [direction]))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    startNode = problem.getStartState()

    # frontier as Priority Queue: initialize frontier with initial state (node, actions)
    frontier = util.PriorityQueue()                               
    frontier.push((startNode, []), heuristic(startNode, problem))

    # Explored list to be empty
    explored = []                                              

    while True:
        # If the frontier is empty then return
        if frontier.isEmpty():
            return []

        # Choose a leaf node and remove it from the frontier
        node, actions = frontier.pop()

        # If the node contains a goal state then return the corresponding solution
        if problem.isGoalState(node):
            return actions

        if node not in explored:
            # Add the state of the node to the explored set
            explored.append(node)

            # Expand the chosen node, adding the resulting nodes to the frontier # 
            # only if their state is not in the the explored set                 #
            successors = problem.getSuccessors(node)
            for nextNode, direction, stepCost in successors:
                if nextNode not in explored:
                    evalFn = problem.getCostOfActions(actions + [direction]) + heuristic(nextNode, problem)
                    frontier.update((nextNode, actions + [direction]), evalFn)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
