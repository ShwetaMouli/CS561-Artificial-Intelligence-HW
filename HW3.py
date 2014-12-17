__author__ = 'Shweta'
f = open("input.txt", 'r+b')
diagnosis = f.readline().rstrip()
no_of_clauses = int(f.readline().rstrip())

#code to create list of clauses
n = 1
clauses = []
while n <= no_of_clauses:
    clauses.append(f.readline().rstrip())
    n += 1

#print diagnosis, no_of_clauses, clauses

#make a list of facts and clauses
facts = []
implying_clauses = []
n = 0
while n < no_of_clauses:
    if "=>" in clauses[n]:
        implying_clauses.append(clauses[n]+";")
    else:
        facts.append(clauses[n])
    n += 1

#print facts, implying_clauses


#create a knowledge base of conclusions and requirements
n = 0
m = 0
kb = dict()
while n < len(implying_clauses):
    start = implying_clauses[n].index('>')
    end = implying_clauses[n].index(';')
    predicate = implying_clauses[n][start+1:end]
    #kb[m][0] = predicate
    no_of_pred = implying_clauses[n].count('&') + 1
    i = 0
    j = 0
    start_req = 0
    isFirst = True
    while implying_clauses[n][i] != '>':
        if implying_clauses[n][i] == '&' or implying_clauses[n][i] == '=':
            end_req = i + 1
            if isFirst == True:
                kb[predicate] = []
                kb[predicate].append(implying_clauses[n][start_req:end_req-1])
                isFirst = False
            else:
                kb[predicate].append(implying_clauses[n][start_req:end_req-1])
            start_req = end_req

        i += 1

#    print predicate, no_of_pred
    n += 1

#print kb


#make can unify list to see what x can be
can_unify = dict()
for fact in facts:
    start_fact = fact.index('(')+1
    if ',' in fact:
        startstart = fact[0:start_fact-1]
        end_fact = fact.index(',')
        can_unify[startstart] = []
        can_unify[startstart].append(fact[start_fact:end_fact])
        start_fact = end_fact
        end_fact = fact.index(')')
        can_unify[startstart].append(fact[start_fact+1:end_fact])
    else:
        end_fact = fact.index(')')
        can_unify[fact[0:start_fact-1]] = []
        can_unify[fact[0:start_fact-1]].append(fact[start_fact:end_fact])

#print can_unify
#print

for key_kb in kb.keys():
    if key_kb.find("(x") == -1:
        allX = True
        for value in kb[key_kb]:
            if value.find("(x") == -1:
                allX = False
            #print value[0:value.index("(")], can_unify.keys(), value[0:value.index("(")] in can_unify.keys()
            if value[0:value.index("(")] not in can_unify.keys():
                allX = False
        #print "ALLX", allX
        if allX == True:
            listOfSets = []
            for value in kb[key_kb]:
                if value[0:value.index("(")] in can_unify.keys():
                    #print value
                    listOfSets.append(set(can_unify[value[0:value.index("(")]]))
            #if set.intersection(*listOfSets) is not None:
                #print set.intersection(*listOfSets)
            #else:
                #print set.intersection(*listOfSets)
            if key_kb[0:key_kb.index("(")] in can_unify.keys():
                can_unify[key_kb[0:key_kb.index("(")]].append(key_kb[key_kb.index("(")+1:key_kb.index(",")])
            else:
                can_unify[key_kb[0:key_kb.index("(")]] = []
                can_unify[key_kb[0:key_kb.index("(")]].append(key_kb[key_kb.index("(")+1:key_kb.index(",")])
        #print allX, key_kb

#print can_unify

#currDiag = diagnosis
def isEntailed(currDiag, xValue = None):
    #print
    if currDiag in facts:
        return True
    elif currDiag[0:currDiag.index("(")] in can_unify.keys():

        if currDiag.find(",") != -1:
            if currDiag[currDiag.index("(")+1:currDiag.index(",")] in can_unify[currDiag[0:currDiag.index("(")]] or xValue in can_unify[currDiag[0:currDiag.index("(")]]:
               return True
            else:
              #print "return 1"
              return False
        else:
            if currDiag[currDiag.index("(")+1:currDiag.index(")")] in can_unify[currDiag[0:currDiag.index("(")]] or xValue in can_unify[currDiag[0:currDiag.index("(")]]:
               return True
            else:
               #print "return 2"
               return False
    #else:
    #print currDiag[0:currDiag.index("(")], "else"
    for key_kb in kb.keys():
        if key_kb[0:key_kb.index("(")] == currDiag[0:currDiag.index("(")] and currDiag.find(",") != -1 and key_kb.find(",") != -1:
            if key_kb[key_kb.index(",")+1:key_kb.index(")")] == currDiag[currDiag.index(",")+1:currDiag.index(")")]:
                for value in kb[key_kb]:
                    #print value, currDiag
                    if value.find("(x") != -1:
                        if currDiag[currDiag.index("(")+1:currDiag.index(",")] != "x":
                            xValue = currDiag[currDiag.index("(")+1:currDiag.index(",")]
                        #print xValue, "if", value
                        #print isEntailed(value, xValue), "31"
                        if isEntailed(value, xValue) is True:
                            #print "happen"
                            continue
                        else:
                            #print "return 31"
                            return False
                    elif value.find("(x") == -1 and currDiag.find("(x") != -1:
                        #xValue = currDiag[currDiag.index("(")+1:currDiag.index(")")]
                        #print xValue, "elif", value
                        #print isEntailed(value, xValue)
                        if isEntailed(value, xValue) is True:
                            #print "happen"
                            continue
                        else:
                            #print "return 3"
                            return False


        elif key_kb[0:key_kb.index("(")] == currDiag[0:currDiag.index("(")] and currDiag.find(",") == -1 and key_kb.find(",") == -1:
            for value in kb[key_kb]:
                #print value, currDiag, xValue, "elif"
                if value.find("(x") != -1 and currDiag.find("(x") == -1:
                    xValue = currDiag[currDiag.index("(")+1:currDiag.index(")")]
                    #print xValue, "elif"
                    #print isEntailed(value, xValue)
                    if isEntailed(value, xValue) is True:
                        #print "happen"
                        continue
                    else:
                        #print "return 321"
                        return False

                elif value.find("(x") != -1 and currDiag.find("(x") != -1:
                    #xValue = currDiag[currDiag.index("(")+1:currDiag.index(")")]
                    #print xValue, "elif", value
                    #print isEntailed(value, xValue)
                    if isEntailed(value, xValue) is True:
                        #print "happen"
                        continue
                    else:
                        #print "return 3"
                        return False
            #print "out here"
            return True
    return True




        #return False

#print isEntailed(diagnosis, 99)

if isEntailed(diagnosis) == True:
    f = open("output.txt", "w")
    f.write("TRUE")
    f.close()
else:
    f = open("output.txt", "w")
    f.write("FALSE")
    f.close()









