from copy import copy, deepcopy
import random
import sys

random.seed(99)

# Генерирует дерево как набор рёбер
def genTree(size):
    tree = []
    for i in range(1,size):
        to = random.randint(1,i)
        tree.append((to,i+1))
    return tree

# Каждому ребру задаёт коэффициент потерь
def addLosses(graph):
    new = []
    for (a,b) in graph:
        weight = random.uniform(0.01,0.02)
        new.append((a,b,weight))
    return new

# Делает граф с потерями
def makeGraph(base):
    return addLosses(genTree(base))

# Генерирует набор нод с потреблением/генерацией
def makeNodes(size):
    nodes = []
    sum = 0
    for i in range (size):
        x = random.uniform(-1,1)
        sum += x
        nodes.append((i+1,x))
    sum /= size
    zeroed = []
    for (n,x) in nodes:
        zeroed.append((n,x-sum))
    return zeroed

# Генерирует пару (ноды, рёбра с потерями)
def makeTask(base):
    nodes = makeNodes(base)
    graph = makeGraph(base)
    return (nodes,graph)

# Делает из нод и рёбер с потерями полную таблицу связности
def makeTable(nodes,graph):
    links = [[ None for i in range(len(nodes))] for j in range(len(nodes))]
    for (a,b,c) in graph:
        links[a-1][b-1] = c
        links[b-1][a-1] = c
    return links

# Возвращает None, если не лист, иначе возвращает родителя
def isLeaf(node,table,root):
    edges = 0
    uplink = None
    for i in range(len(table)):
        if table[i][node-1] == None or node == root:
            pass
        else:
            edges += 1
            uplink = i+1
    if edges == 1:
        return uplink
    else:
        return None

# Съедает дерево
def runTree(nodes_,table_,root):
    table = deepcopy(table_)
    nodes = deepcopy(nodes_)
    allLosses = 0
    for _ in range(len(table)):
        for i in range(len(table)):
            uplink = isLeaf(i+1,table,root)
            if uplink == None:
                pass
            else:
                (a,b) = nodes[uplink-1]
                (c,d) = nodes[i]
                losses = min(abs(d),d**2 * table[i][uplink-1])
                #if losses == abs(d):
                    #print("Alarm:",d)
                arrived = d / abs(d) * ( abs(d) - losses )
                allLosses += losses
                nodes[uplink-1] = (a,b+arrived)
                table[i][uplink-1] = None
                table[uplink-1][i] = None
    return allLosses

def solution(nodes,edges):
    #(loss,nodes,edges,mapp) = shrink(nodes_,edges_)
    #loss = 0
    #nodes = deepcopy(nodes_)
    #edges = deepcopy(edges_)
    table = makeTable(nodes,edges)
    roots = [ i+1 for i in range(len(table)) ]
    best = float("inf")
    guess = None
    for r in roots:
        que = runTree(nodes,table,r)
        if que < best:
            best = que
            guess = r
    #return(unMapEdges(mapp,guess),best+loss)
    return(guess,best)

def test():
    (a,b) = makeTask(20)
    print(a)
    print("~~~~~~~~~~~")
    print(b)
    print("~~~~~~~~~~~")
    print(solution(a,b))
#test()

def format_task(task):
    (nodes, edges) = task
    return "{}\n{}\n{}\n{}\n".format(
        len(nodes),
        "\n".join("{} {}".format(*n) for n in nodes),
        len(edges),
        "\n".join("{} {} {}".format(*n) for n in edges),
    )

def generate():
    num_tests = 10
    tests = []
    for test in range(num_tests):
        task = makeTask(20)
        test_case = format_task(task)
        tests.append((test_case,task))
    return tests

def solve(dataset):
    ls = dataset.splitlines()
    nnodes = int(ls[0])
    nodes = [(int(x), float(y)) for (x, y) in (l.split() for l in ls[1:nnodes+1])]
    nedges = int(ls[nnodes+1])
    edges = [(int(x), int(y), float(z)) for (x, y, z) in 
        (l.split() for l in ls[nnodes+2:nnodes+nedges+2])]
    
    (root,score) = solution(nodes,edges)
    return str(root)

def check(reply, clue):
    (nodes,edges) = clue
    table = makeTable(nodes,edges)
    (my_root,my_score) = solution(nodes,edges)
    root = eval(reply)
    return runTree(nodes,table,root) + 0.01 > my_score

def sanity(fn):
    tests = generate()
    flag = False
    for (t, c) in tests:
        y = fn(t)
        if not check(y, c):
            m = solve(t)
            print("BAD TRY>>>\n{}\n>>>\nYOUR: {}\nMINE: {}".format(t, y, m))
            flag = True
    if flag:
        print("TEST FAILED :(")
    else:
        print("ALL RIGHT :D")


print(solve(sys.stdin.read()))