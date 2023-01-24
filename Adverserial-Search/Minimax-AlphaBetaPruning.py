MIN_TURN = False
MAX_TURN = True


class Node:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.parent = None
        self.processedNodeNumber = 0

    def __str__(self):
        return str([tuple(self.state), self.processedNodeNumber])


def createGraph(gameList):
    graph = {}
    for pile in gameList:
        graph[pile] = []

    for i in range(len(gameList)):
        value = gameList[i]
        for j in range(value):
            newState = gameList[:]
            newState[i] = j
            node = Node(newState)
            graph[value].append(node)

    return graph


def checkIfLeaf(gameList):
    for pile in gameList:
        if pile != 0:
            return False
    return True


def createTree(gameList, parent):
    root = Node(gameList)
    root.parent = parent

    if checkIfLeaf(gameList):
        return root

    for pile in range(len(root.state)):
        for i in range(root.state[pile]):
            newState = root.state[:]
            newState[pile] = i
            root.children.append(createTree(newState, root))

    return root


def nextKeyInGraph(graph, key):
    res = None
    temp = iter(graph)
    for tkey in temp:
        if tkey == key:
            res = next(temp, None)
    return res


def minimax(node, processedNodeSum, isMax):
    if len(node.children) == 0: # if leaf node
        processedNodeSum += 1
        if isMax:
            return node, 1, processedNodeSum
        return node, -1, processedNodeSum

    if isMax:
        values = []
        for child in node.children:
            values.append(minimax(child, processedNodeSum, MIN_TURN))
        maxVal = (Node(None), -1)
        tempSum = 0
        for val in values: # Find max loop
            tempSum += val[2] # Sum processedNodeCount of each child
            if val[1] > maxVal[1]:
                maxVal = val
        node.processedNodeNumber = processedNodeSum + tempSum
        return maxVal[0], maxVal[1], processedNodeSum+1+tempSum
    else:
        values = []
        for child in node.children:
            values.append(minimax(child, processedNodeSum, MAX_TURN))
        minVal = (Node(None), 2)
        tempSum = 0
        for val in values: # Find min loop
            tempSum += val[2]
            if val[1] < minVal[1]:
                minVal = val
        node.processedNodeNumber = processedNodeSum+tempSum
        return minVal[0], minVal[1], processedNodeSum+1+tempSum


def alphabeta(node, processedNodeSum, isMax, alpha, beta):
    if len(node.children) == 0:
        processedNodeSum += 1
        if isMax:
            return node, 1, processedNodeSum
        return node, -1, processedNodeSum

    if isMax:
        bestValue = float('-inf')
        values = []
        for child in node.children:
            value = alphabeta(child, processedNodeSum, MIN_TURN, alpha, beta)
            values.append(value)
            value = value[1]
            bestValue = max(bestValue, value)
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break
        maxVal = (Node(None), -1)
        tempSum = 0
        for val in values:
            tempSum +=val[2]
            if val[1] > maxVal[1]:
                maxVal = val
        node.processedNodeNumber = processedNodeSum + tempSum
        return maxVal[0], maxVal[1], processedNodeSum+1+tempSum
    else:
        bestValue = float('inf')
        values = []
        for child in node.children:
            value = alphabeta(child, processedNodeSum, MAX_TURN, alpha, beta)
            values.append(value)
            value = value[1]
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            if beta <= alpha:
                break
        minVal = (Node(None), 2)
        tempSum = 0
        for val in values:
            tempSum += val[2]
            if val[1] < minVal[1]:
                minVal = val
        node.processedNodeNumber = processedNodeSum+tempSum
        return minVal[0], minVal[1], processedNodeSum+1+tempSum


def findSolutionParent(node):
    if node.parent.parent is None:
        return node

    return findSolutionParent(node.parent)


def SolveGame(method_name, problem_file_name, player_type):
    # Tree Initialization
    f = open(problem_file_name, "r")
    content = f.read()
    json = content[1:-1].split(',')
    initialGame = [eval(i) for i in json]  # Convert Elements to Integer

    tree = createTree(initialGame, None)

    # Algorithms
    isMax = (player_type == "MAX")
    if method_name == "Minimax":
        result = minimax(tree, 0, isMax)
        resultNode = result[0] # minimax returns a triple (state, resultValue, processedNodeCount)
        return findSolutionParent(resultNode) # Find the solution node from leaf node parents
    elif method_name == "AlphaBeta":
        result = alphabeta(tree, 0, isMax, float('-inf'), float('inf'))
        resultNode = result[0]
        return findSolutionParent(resultNode)
    return
