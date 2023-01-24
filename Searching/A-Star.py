class Node:
    def __init__(self, type, coordinate, value=0, parent=None):
        self.type = type
        self.coordinate = coordinate
        self.value = value
        self.parent = parent
        self.parentIndex = 0
        self.visitedNumber = 0

    def __str__(self):
        return f"{self.type}  ({self.coordinate})"

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.value > other.value

    def getCurrentParent(self):
        if type(self.parent) != list:
            return self.parent
        return self.parent[self.parentIndex]

    def getParents(self):
        if type(self.parent) != list:
            if self.parent is None:
                return self.parent
            return [self.parent]
        return self.parent

    def addParent(self, newParent):
        if type(newParent) != list:
            if type(self.parent) != list:
                if self.parent is None:
                    self.parent = [newParent]
                    return
                self.parent = [self.parent, newParent]
                return
            self.parent.append(newParent)
            return
        if type(self.parent) != list:
            if self.parent is None:
                self.parent = newParent
                return
            self.parent = [self.parent] + newParent
            return
        self.parent = self.parent + newParent
        return

    def addParentAncestors(self, newParent):
        if newParent.parent is None:
            self.parent = [newParent.type]
        else:
            self.parent = newParent.parent + [newParent.type]

    def hasSameParent(self, nodetype):
        if type(self.parent) != list:
            return self.parent.type == nodetype
        for p in self.parent:
            if p.type == nodetype:
                return True
        return False


class NodeAStar: # Created to not spend time on overloading constructors in one class
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __str__(self):
        return f"({self.position})"

    def __eq__(self, other):
        return self.position == other.position


# Add a vertex to the dictionary
def add_vertex(v, graph):
    if v in graph:
        return
    else:
        graph[v] = []


def add_edge(props, v1, v2, e, graph):
    # Check if vertex v1 is a valid vertex
    if v1 not in props['graph']:
        return
        print("Vertex ", v1, " does not exist.")
    # Check if vertex v2 is a valid vertex
    elif v2 not in props['graph']:
        return
        print("Vertex ", v2, " does not exist.")
    else:
        # Since this code is not restricted to a directed or
        # an undirected graph, an edge between v1 v2 does not
        # imply that an edge exists between v2 and v1
        temp = [v2, e]
        graph[v1].append(temp)


def findFromGraph(coordinates, graph):
    for a in graph:
        if a[1] == coordinates:
            return Node(a[0], a[1])
    return None


def findFromGraphKey(key, graph):
    for a in graph:
        if a[0] == key:
            return Node(a[0], a[1])
    return None


def createGraph(problem_file_name):
    graph = {}
    f = open(problem_file_name, "r")
    content = f.read()
    edgeLength = content.split("\n").__len__()
    content = content.replace("\n", "\t")
    grid = content.split("\t")
    currentLine = 0
    nodes = []
    dotcounter = 0
    while currentLine < edgeLength:
        for x in range(edgeLength):
            index = (currentLine * edgeLength) + x
            if not grid[index] == '#':
                if grid[index] == '.':
                    add_vertex(('D' + str(dotcounter), (x, currentLine)), graph)
                    dotcounter += 1
                else:
                    add_vertex((grid[index], (x, currentLine)), graph)
        currentLine += 1
    for n in graph:
        x = n[1][0]
        y = n[1][1]
        neighbourCoordList = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        neighbours = []
        for coord in neighbourCoordList:
            neighbour = findFromGraph(coord, graph)
            if neighbour is not None:
                neighbours.append(neighbour)
        graph[n] = neighbours
    return graph


def findStartPoint(graph):
    for node in graph:
        if node[0] == 'S':
            return Node('S', node[1])


def findEndPoint(graph):
    for node in graph:
        if node[0] == 'E':
            return Node('E', node[1])


def extendImplicitNode(node, graph):
    res = []
    key = (node.type, node.coordinate)
    for neighbour in graph[key]:
        if neighbour.type == 'S':
            continue
        newNode = Node(neighbour.type, neighbour.coordinate)
        newNode.addParentAncestors(node)  ## it is problematic
        # newNode.value = neighbour[1]
        res.append(newNode)
    return res


def ucs(graph):
    startNode = findStartPoint(graph)
    endNode = findEndPoint(graph)
    resultPaths = []
    opened = []

    opened.append(startNode)
    while True:
        if opened.__len__() == 0:
            return resultPaths

        selectedNode = min(opened)  # should be selected from left
        opened.remove(selectedNode)
        if selectedNode.parent is not None:
            if selectedNode.parent[-1] == endNode and selectedNode.parent not in resultPaths:
                resultPaths.append(selectedNode.parent)

        if selectedNode.type == 'E' and selectedNode.parent is not None:
            selectedNode.parent.append(selectedNode.type)
            resultPaths.append(selectedNode.parent)
            continue

        newNodes = extendImplicitNode(selectedNode, graph)
        for newNode in newNodes:
            if selectedNode.parent is not None:
                if newNode.type not in selectedNode.parent:
                    opened.append(newNode)
            else:  # selectednode is the starting point
                opened.append(newNode)
    return resultPaths


def ConvertResultPath(path, graph):
    res = []
    for key in reversed(path):
        node = findFromGraphKey(key, graph)
        res.append(node.coordinate)
    return res



def astar(maze, start, end):


    start_node = NodeAStar(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = NodeAStar(None, end)
    end_node.g = end_node.h = end_node.f = 0


    open_list = []
    closed_list = []


    open_list.append(start_node)


    while len(open_list) > 0:


        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index


        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path

        # Generate children
        children = []
        for new_position in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # Adjacent squares


            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[1]][node_position[0]] == '#' or maze[node_position[1]][node_position[0]] == 'S':
                continue


            new_node = NodeAStar(current_node, node_position)


            children.append(new_node)


        for child in children:


            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = int(maze[child.position[1]][child.position[0]])
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


def createGraphHeuristic(problem_file_name):
    f = open(problem_file_name, "r")
    content = f.read()
    edgeLength = content.split("\n").__len__()
    content = content.replace("\n", "\t")
    grid = content.split("\t")
    currentLine = 0
    maze = []
    while currentLine < edgeLength:
        loopList = []
        for x in range(edgeLength):
            index = (currentLine * edgeLength) + x
            if grid[index] == 'E':
                loopList.append('0')
            else:
                loopList.append(grid[index])
        maze.append(loopList)
        currentLine += 1
    return maze


def findCoord(maze, value):
    edgeLength = len(maze)
    for y in range(edgeLength):
        for x in range(edgeLength):
            if maze[y][x] == value:
                return (x, y)


def astarsearch(problem_file_name):
    maze = createGraphHeuristic(problem_file_name)
    start = findCoord(maze, 'S')
    end = findCoord(maze, '0')  # Replaced E with 0

    path = astar(maze, start, end)
    return path


def InformedSearch(method_name, problem_file_name):
    if method_name == 'UCS':
        graph = createGraph(problem_file_name)
        result = ucs(graph)
        return ConvertResultPath(result[0], graph)
    elif method_name == 'AStar':
        return astarsearch(problem_file_name)
