import copy
import random

class BayesNet:
    def __init__(self, children, pt, variables):
        self.children = children
        self.X = ""
        #self.pt = dict(pt)
        self.pt = {}
        for entry in pt:
            if len(pt[entry][1]) == 1:
                value = 0
                for i in pt[entry][1]:
                    value = i
                self.pt[entry] = ([], {(): value})
            else:
                parents = pt[entry][0]
                temp = {}
                l = pt[entry][1]
                for i in l:
                    newkey = i
                    if type(i) is bool:
                        newkey = (i,)
                    temp[newkey] = l[i]
                self.pt[entry] = (parents, temp)

        # self.variables = variables
        self.variables = []
        for entry in children:
            self.variables.append(entry)

    def variable_values(self):
        return [True, False]

    def get_parents(self, X):
        res = []
        for entry in self.children:
            if X in self.children[entry]:
                res.append(entry)
        return res

    def probability(self, Y, y, e):
        # Return the probability of Y = y given the evidence e
        parents, table = self.pt[Y]
        key = ()
        for p in parents:
            key += (e[p],)

        if y is False:
            return 1 - table[key]

        return table[key]




def enumeration_ask(X, e, bn):
    QX = {}
    bn.X = X

    for xi in [True, False]:
        e = copy.deepcopy(e)
        e[X] = xi
        QX[xi] = enumerate_all(bn.variables, e, bn)
        del e[X]
    return normalize(QX)


def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0

    Y, rest = variables[0], variables[1:]

    if Y in e:
        prob = bn.probability(Y, e[Y], e)
        return prob * enumerate_all(rest, e, bn)
    else:
        sum = 0
        for yi in [True, False]:
            prob2 = bn.probability(Y, yi, e)
            e = copy.deepcopy(e)
            e[Y] = yi
            sum += prob2 * enumerate_all(rest, e, bn)
            del e[Y]

    return sum




def normalize(distribution):
    sum = 0
    for key in distribution:
        sum += distribution[key]
    for key in distribution:
        distribution[key] = distribution[key] / sum
    for key in distribution:
        distribution[key] = round(distribution[key], 3)
    return distribution


def parse_input_file1(input_file):
    nodes = []
    paths = []
    probability_table = {}
    query = []
    # Open the input file and read its contents
    with open(input_file, 'r') as f:
        contents = f.read()

    # Split the contents of the file into a list of lines
    lines = contents.split('\n')
    validList = ""
    # Iterate over the lines in the file
    for line in lines:
        if line[1:-1] == "BayesNetNodes":
            validList = "nodes"
        elif line[1:-1] == "Paths":
            validList = "paths"
        elif line[1:-1] == "ProbabilityTable":
            validList = "probability_table"
        elif line[1:-1] == "Query":
            validList = "query"
        else:
            if validList == "nodes":
                nodes.append(line)
            if validList == "paths":
                x = eval(line)
                paths.append(x)
            if validList == "probability_table":
                x = eval(line)
                probability_table[x[0]] = (x[1], x[2])
            if validList == "query":
                query = eval(line)

    return (nodes, paths, probability_table, query)



def initializeBayesNet(file):
    (nodes, paths, probability_table, query) = parse_input_file1(file)
    bn = initialize_bn(nodes, paths, probability_table, query)
    return bn


def initialize_bn(nodes, paths, probability_table, query):
    # Create a dictionary to store the probability tables for each node
    pt = {}
    # Iterate over the probability table entries and add them to the dictionary
    for entry in probability_table:
        node = entry
        parents, table = probability_table[entry]
        pt[node] = (parents, table)

    # Create a dictionary to store the children of each node
    children = {}
    for node in nodes:
        children[node] = []

    # Iterate over the paths and add them to the children dictionary
    for path in paths:
        parent, child = path
        for p in parent:
            children[p].append(child)

    # Return the initialized Bayesian network as a tuple
    return (children, pt, query)



def gib_ask(X, e, bn, N):
    """
    Since there are such small values as 0.001, I improvised a little from Metropolis-Hastings
    to go beyond my first approach.
    In my first sampling approach, I always got {True:0, False:1} because of the small values

    """

    count_dic = {True: 0, False:0} #counts dictioanry

    Z = [var for var in bn.variables if var not in e] #nonevidence variables

    x = copy.deepcopy(e) #current state

    # initialize x with random values for each variable in Z
    for hidden in Z:
        prob = bn.probability(hidden, True, x)
        x[hidden] = random.uniform(0,1) <= prob

    for j in range(N):
        for Zi in Z:
            #First Approach was only
            #x[Zi] = random.uniform(0, 1) <= bn.probability(Zi, True, x)
            proposal = random.uniform(0, 1) <= bn.probability(Zi, True, x)

            # Calculate the acceptance probability of the proposal value
            p_current = bn.probability(Zi, x[Zi], x)
            p_proposal = bn.probability(Zi, proposal, x)
            acceptance_prob = p_proposal / p_current

            # Accept the proposal value with probability equal to the acceptance probability
            if random.uniform(0, 1.5) <= acceptance_prob:
                x[Zi] = proposal
            else:
                x[Zi] = not proposal
            # Update the count vector
            count_dic[x[X]] += 1
    return normalize(count_dic)


def DoInference(method_name, problem_file_name, num_iteration):
    (children, pt, query) = initializeBayesNet(problem_file_name)
    bn = BayesNet(children, pt, query[0])
    e = query[1]
    if method_name == "ENUMERATION":
        answer = enumeration_ask(query[0], e, bn)
        return answer
    elif method_name == "GIBBS":
        answer = gib_ask(query[0],e,bn,num_iteration)
        return answer


