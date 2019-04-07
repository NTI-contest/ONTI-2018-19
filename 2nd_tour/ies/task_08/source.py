import random
import sys

seed = 544234
random.seed(seed)

pageCount = 500

def genMain():
    result = []
    for _ in range(10):
        target = random.randint(0,pageCount-1)
        result.append((0,target))
    return result

def gen():
    result = genMain()
    for _ in range(10,round(pageCount**1.5)):
        source = random.randint(0,pageCount-1)
        target = random.randint(0,pageCount-1)
        result.append((source,target))
    return result

def viewOnePage(openPages,pagesRanks,wikiStructure):
    #print(openPages)
    pagesRanks[openPages[0]] += 10
    currentPage = openPages[0]
    for (source,destination) in wikiStructure:
        if source == currentPage:
            if ( destination in openPages[1:] ) and ( destination != currentPage ):
                pagesRanks[destination] += 1
            else:
                openPages.append(destination)
    if len(openPages) < 50:
        if openPages == []:
            resultPages = [0]
        else:
            resultPages = openPages[1:]
    else:
        rankers = openPages[:-1]
        for p in rankers:
            pagesRanks[p] += 5
        resultPages = [ openPages[-1]]
    return resultPages, pagesRanks

def surfNTimes(n,wikiStructure):
    openPages = [0]
    pagesRanks = [ 0 for _ in range(len(wikiStructure)) ]
    for i in range(n):
        opens,ranks = viewOnePage(openPages,pagesRanks,wikiStructure)
        openPages = opens
        pagesRanks = ranks
    return ranks

def findBestPages(ranks):
    tagged = [ (ranks[ix],ix) for ix in range(len(ranks)) ]
    tagged.sort()
    tagged.reverse()
    return tagged[:10]

def test(n):
    random.seed(seed)
    wiki = gen()
    wiki.sort()
    print(n)
    ranks = surfNTimes(n,wiki)
    bests = findBestPages(ranks)
    for b in range(len(bests)):
        print(b, bests[b])

#test(pageCount)
#test(pageCount*3)
#test(pageCount*10)
#test(pageCount*15)

def generate():
    result = []
    for _ in range(20):
        g = gen()
        result.append((str(g),g))
    return result

def solve(dataset):
    wiki = eval(dataset)
    ranks = surfNTimes(5000,wiki)
    bests = findBestPages(ranks)
    rating,best = bests[0]
    return str(best)

def check(reply,clue):
    their = eval(reply)
    ranks = surfNTimes(10000,clue)
    bests = findBestPages(ranks)
    rating,_ = bests.pop()
    if ranks[their] >= rating:
        return True
    else:
        return ( ranks[their] / rating ) >= 0.99

print(solve(sys.stdin.read()))