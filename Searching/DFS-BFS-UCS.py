def UnInformedSearch(method_name, problem_file_name):
    # driver code
    graph = {}

    # Add a vertex to the dictionary
    def add_vertex(v, props):
        if v in props['graph']:
            return
        else:
            props['graph'][v] = []

    # Add an edge between vertex v1 and v2 with edge weight e
    def add_edge(props, v1, v2, e):
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
            props['graph'][v1].append(temp)


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

    dresult = []
    result = []
    bresult = []
    dfsvisited = set()
    count = 0

    d = 0

    def dfs(graph, node, props):

        if node not in props['dfsvisited']:
            if (CheckAndAddAsResultdfs(node, props)):
                props['dfsvisited'].add(node)
            for index in reversed(range(len(props['graph'][node]))):
                dfs(props['graph'], props['graph'][node][index][0], props)

    def CheckAndAddAsResultdfs(node, props):
        if (node == 'S'):
            props['dresult'].append(node)
            return 1
        elif (node == 'F'):
            if (props['count'] == props['minCustomerNo']):
                props['dresult'].append(node)
                props['count'] += 1
                return 1
        else:
            if (props['count'] < props['minCustomerNo']):
                props['dresult'].append(node)
                props['count'] += 1
                return 1
            elif (props['count'] >= props['minCustomerNo']):
                return 1
        return 0

    def CheckAndAddAsResult(node, props):
        if (node == 'S'):
            props['bresult'].append(node)
            return 1
        elif (node == 'F'):
            if (props['count'] == props['minCustomerNo']):
                props['bresult'].append(node)
                props['count'] += 1
                return 1
        else:
            if (props['count'] < props['minCustomerNo']):
                props['bresult'].append(node)
                props['count'] += 1
                return 1
            elif (props['count'] >= props['minCustomerNo']):
                return 1
        return 0

    def ProcessResultList(rlist, props):

        res = []
        for n in rlist:
            for i in props['nodes']:
                if (n == i.type):
                    res.append(list(i.coordinate))
                    break
        return res

    visited = []
    queue = []

    def bfs(graph, node, props):  # function for BFS
        props['visited'].append(node)
        props['bresult'].append(node)
        props['queue'].append(node)

        while props['queue']:  # Creating loop to visit each node
            m = props['queue'].pop(0)

            for neighbour in props['graph'][m]:
                if neighbour[0] not in props['visited']:
                    if (CheckAndAddAsResult(neighbour[0], props)):
                        props['visited'].append(neighbour[0])
                        props['queue'].append(neighbour[0])


    opened = []
    closed = []
    ucsgraph = {}
    number_of_steps = 0

    def recursiveCalculatePaths(node):
        resultList = []
        for p in node.parent:
            myp = p[node.parentIndex]

            tempList = [node.type]
            while myp is not None:
                tempList.append(myp)
                myp = myp.parent[myp.parentIndex]

    def paths(node):
        if not node.parent:
            return [[node.type]]  # one path: only contains self.value
        mypaths = []
        parents = node.getParents()
        for parent in parents:
            s = paths(parent)
            for path in s:
                mypaths.append([node.type] + path)
        return mypaths

    def calculatePath(node):
        path = [node.type]
        node = node.parent
        while True:
            path.append(node.type)
            if node.parent == None:
                break
            node = node.parent
        path.reverse()
        return path

    def calculateDistance(parent, child):  # Node parent, Node child
        global graph
        for neighbor in graph[parent.type]:
            if neighbor[0] == child.type:  # child should come from global
                distance = parent.value + neighbor[1]
                if distance < child.value:
                    child.parent = parent
                    return distance

                return child.value

    def InClosed(node):
        for n in closed:
            if n.type == node.type:
                return True
        return False

    def InOpened(node):
        for n in opened:
            if n.type == node.type:
                return True
        return False

    def getFromOpened(type):
        """for n in reversed(range(len(opened))):
            if opened[n].type == type:
                return opened[n]"""
        for n in opened:
            if n.type == type:
                return n
        return None

    def getFromClosed(type):
        for n in closed:
            if n.type == type:
                return n
        return None

    def getMinFromOpened():
        global opened
        temp = Node()
        selected = min(opened)
        if selected.type == 'F':
            temp = selected
            opened.remove(selected)
            selected = min(opened)
            opened.append(temp)
        return selected



    def extendImplicitNode(node, props):
        res = []
        for neighbour in props['graph'][node.type]:
            if neighbour[0] == 'S':
                continue
            newNode = Node(neighbour[0], 0)
            newNode.addParentAncestors(node)  ## it is problematic
            newNode.value = neighbour[1]
            res.append(newNode)
        return res

    def search(graph, start, props):
        nodes = props['nodes']
        resPaths = []
        startNode = [n for n in nodes if n.type == start][0]
        startNode.value = 0
        props['opened'].append(startNode)

        while True:
            if len(props['opened']) == 0:
                return resPaths

            selected_node = min(props['opened'])
            props['opened'].remove(selected_node)

            if selected_node.parent is not None and len(selected_node.parent) == props['minCustomerNo'] + 2:
                if selected_node.parent[-1] == 'F' and selected_node.parent not in resPaths:
                    resPaths.append(selected_node.parent)

            if selected_node.type == 'F' and selected_node.parent is not None:
                if len(selected_node.parent) == props['minCustomerNo'] + 1 and selected_node.parent not in resPaths:
                    selected_node.parent.append('F')
                    resPaths.append(selected_node.parent)
                    continue

            if selected_node.parent is not None and len(selected_node.parent) >= props['minCustomerNo'] + 2:
                continue

            new_nodes = extendImplicitNode(selected_node, props)

            for new_node in new_nodes:
                if new_node.type == 'F':
                    if selected_node.parent is not None and len(selected_node.parent) >= props['minCustomerNo']:
                        props['opened'].append(new_node)
                elif selected_node.parent is None or new_node.type not in selected_node.parent:
                    if selected_node.parent is None:
                        props['opened'].append(new_node)
                    elif selected_node.parent is not None and selected_node.parent[-1] != 'F':
                        props['opened'].append(new_node)
        return resPaths


    minCustomerNo = 0
    numberOfCustomers = 0
    nodes = []

    def has_duplicates(x):
        for idx, item in enumerate(x):
            if item in x[(idx + 1):]:
                return True
        return False

    def calculateCoorDistances(lis):
        dist = 0
        for i in range(len(lis) - 1):
            dist += CalculateDistanceBetweenCoords(lis[i], lis[i + 1])
        return dist

    def minFromPairList(pairs):
        mini = (pairs[0])
        for p in pairs:
            if p[0] < mini[0]:
                mini = p
        return mini

    def prdif(ress, props):
        res = ress
        lasts = []
        for r in range(len(res)):
            if len(res[r]) - 2 == props["minCustomerNo"] and not has_duplicates(res[r]):
                coordList = ProcessResultList(res[r][::-1], props)
                x = (calculateCoorDistances(coordList), r)
                lasts.append(x)
        minPath = minFromPairList(lasts)
        return ((ProcessResultList(res[minPath[1]][::-1], props)))

    def createGraph(problem_file_name, props):

        f = open(problem_file_name, "r")
        content = f.read()
        json = content.split(",", 1)
        min = int(json[0][-1])  # 2 basamaklı sayılar için
        props['minCustomerNo'] = min
        json[1] = json[1].replace(']', '[').split("[")[1].replace("'", "").replace(" ", "")
        map = json[1].split(",")
        size = len(map[0])
        for i in range(size):
            for j in range(size):
                if (map[i][j] == 'C'):
                    props['nodes'].append(Node('C', (i, j)))
                    props['numberOfCustomers'] += 1
                if (map[i][j] == 'F'):
                    props['nodes'].append(Node('F', (i, j)))
                if (map[i][j] == 'S'):
                    props['nodes'].append(Node('S', (i, j)))

        if (props['numberOfCustomers'] < props['minCustomerNo']):
            return None

        counter = 0
        labels = []
        for i in range(len(props['nodes'])):
            if (props['nodes'][i].type == 'C'):
                label = "C" + str(counter)
                props['nodes'][i].type = label
                counter += 1
            else:
                label = props['nodes'][i].type
            labels.append(label)
            add_vertex(label, props)
        for i in range(len(props['nodes'])):
            for h in range(len(props['nodes'])):
                if h == i:
                    continue
                add_edge(props, labels[i], labels[h], CalculateDistanceBetweenCoords(props['nodes'][i].coordinate, props['nodes'][h].coordinate))

    lastGraphName = ""


    def UnInformedSearch1(method_name, problem_file_name, props):


        props['lastGraphName'] = problem_file_name
        createGraph(problem_file_name, props)

        if (props['numberOfCustomers'] < props['minCustomerNo']):
            return None

        if method_name == "DFS":
            dfs(graph, 'S', props)
            return ProcessResultList(props['dresult'], props)
        elif method_name == "BFS":
            bfs(graph, 'S', props)
            return ProcessResultList(props['bresult'], props)
        elif method_name == "UCS":
            result = search('graph', 'S', props)
            return prdif(result, props)[::-1]

        return ProcessResultList(result)

    def CalculateDistanceBetweenCoords(coor1, coor2):
        return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])

    props = {
        'minCustomerNo': minCustomerNo,
        'nodes': nodes,
        'graph': graph,
        'numberOfCustomers': numberOfCustomers,
        'lastGraphName': lastGraphName,
        'opened': opened,
        'closed': closed,
        'dfsvisited': dfsvisited,
        'count': count,
        'dresult': dresult,
        'bresult': bresult,
        'visited': visited,
        'queue': queue
    }

    return UnInformedSearch1(method_name, problem_file_name, props)

print(UnInformedSearch("BFS", "sample1.txt"))