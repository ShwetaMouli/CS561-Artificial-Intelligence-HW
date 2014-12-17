__author__ = 'Shweta'
# read input file
f = open("input.txt", 'r+b')
search_method = int(f.readline().rstrip('\n'))
start_name = f.readline().rstrip('\n')
end_name = f.readline().rstrip('\n')
number_of_people = int(f.readline().rstrip('\n'))

#code to create list of names of students
n = 1
names = []
while n <= int(number_of_people):
    names.append(f.readline().rstrip('\n'))
    n += 1

#code to store the array
n = 1
graph_matrix = []
while n <= int(number_of_people):
    line = f.readline().rstrip('\n')
    graph_matrix.append([int(x) for x in line.split(' ')])
    n += 1

if int(number_of_people) <= 0:
    exit(0)
elif int(number_of_people) == 1:
    print "Single person, invalid."
    exit(0)


#print graph_matrix[2][2]
#code to implement bfs
def bfs(graph, start, end, names_bfs):
    start_no = names_bfs.index(start)
    depth = 0
    bfs_index = 1
    bfs_queue = list()
    closed = list()
    bfs_queue.append([bfs_index, start, depth, 0, 0, 0])
    names_visited = [0] * len(names_bfs)
    names_visited[start_no] = 1
    curr_name = start
    bfs_path = list()
    bfs_log = list()

    #deciding which node to pop, alphabetically
    while len(bfs_queue) != 0:
        #print
        #print bfs_queue

        poppable_nodes = list()
        min_cost = bfs_queue[0][2]
        i = 0
        #print "mincost is", min_cost

        while i < len(bfs_queue) and bfs_queue[i][2] == min_cost:
            #print bfs_queue[i]
            poppable_nodes.append(bfs_queue[i])
            i += 1

        pop_index = 0
        i = 0

        #print "poppable nodes are", poppable_nodes
        while i < len(poppable_nodes):
            if poppable_nodes[i][1] < poppable_nodes[pop_index][1]:
                pop_index = i
            i += 1

        #print "popped is", bfs_queue[pop_index], "end is", end
        popped = bfs_queue.pop(pop_index)
        curr_name = popped[1]
        closed.append(popped)
        bfs_log.append(popped[1])
        #print bfs_log
        path_cost = 0
        if popped[1] == end:
            path_cost = popped[5]
            bfs_path.append(popped[1])
            i = 0
            closed_indices = list()
            while i < len(closed):
                closed_indices.append(closed[i][0])
                i += 1
            #print
            #print popped, closed_indices, popped[3]
            #print closed_indices.index(popped[4]), closed
            next_node = closed[closed_indices.index(popped[4])]
            bfs_path.append(next_node[1])
            while popped[2] != 1:
                #print "next node", next_node, "closed index", closed_indices.index(next_node[4]), "closed of closed index", closed[closed_indices.index(next_node[4])]
                if next_node[4] != 0:
                    next_node = closed[closed_indices.index(next_node[4])]
                bfs_path.append(next_node[1])
                popped[2] -= 1
                #print "depth", popped[2]
            bfs_path.reverse()
            return bfs_log, bfs_path, path_cost


        #exploring the graph
        up_next = list()
        i = 0
        while i < len(names_bfs):
            #print "sup", graph[names_bfs.index(curr_name)][i], names_bfs[i]
            bool_flag = names_bfs[i] in bfs_log or names_bfs[i] in bfs_queue
            #print bool_flag, bfs_log
            if graph[names_bfs.index(curr_name)][i] != 0:
                if bool_flag is False:
                    up_next.append(names_bfs[i])
                    #print names_bfs[i], "hi2"
            i += 1
        up_next.sort()
        depth += 1
        #print up_next
        for person in up_next:
            bfs_index += 1
            new_node = [bfs_index, person, popped[2]+1, names_bfs.index(curr_name), popped[0], popped[5]+graph_matrix[names_bfs.index(person)][names_bfs.index(popped[1])]]
            #print new_node
            add_flag = True
            for node in bfs_queue:
                if node[1] == new_node[1]:
                    add_flag = False
                    bfs_index -= 1
            if add_flag == True:
                bfs_queue.append(new_node)


        #print "finished: ", closed


#performing DFS on graph
def dfs(graph, start, end, names_dfs):
    start_no = names_dfs.index(start)
    depth = 0
    dfs_index = 1
    dfs_queue = list()
    closed = list()
    dfs_queue.append([dfs_index, start, depth, 0, 0])
    curr_name = start
    dfs_path = list()
    dfs_log = list()
    closed = list()
    popped = list()

    while len(dfs_queue) != 0:
        #print
        #print
        #print "NExt one"
        #what is visitable from the current node popped

        if len(dfs_queue) == 1:
            popped = dfs_queue.pop()
        else:
            #print popped
            #print "closed", closed
            parent_node = popped
            min_parent = popped[0]
            poppable_nodes = list()
            i = 0
            while i < len(dfs_queue):
                if dfs_queue[i][3] == min_parent:
                    poppable_nodes.append(dfs_queue[i])
                i += 1
            while len(poppable_nodes) == 0:
                i = 0
                while i < len(dfs_queue):
                    #print "loop1", min_parent
                    if min_parent == dfs_queue[i][0]:
                        min_parent = dfs_queue[i][3]
                    i += 1

                i = 0
                while i < len(closed):
                    #print "loop2", min_parent
                    if min_parent == closed[i][0]:
                        min_parent = closed[i][3]
                    i += 1

                i = 0
                while i < len(dfs_queue):
                    #print "loop3", min_parent
                    if dfs_queue[i][3] == min_parent:
                        poppable_nodes.append(dfs_queue[i])
                    i += 1

            pop_index = 0
            i = 0

            #print "poppable nodes are", poppable_nodes
            while i < len(poppable_nodes):
                if poppable_nodes[i][1] < poppable_nodes[pop_index][1]:
                    pop_index = i
                i += 1


            #print "pop index is", pop_index
            popped = dfs_queue.pop(dfs_queue.index(poppable_nodes[pop_index]))

        #print "Actually popped", popped
        curr_name = popped[1]
        closed.append(popped)
        dfs_log.append([popped[1], popped[2]])
        #print bfs_log

        path_cost = 0
        if popped[1] == end:
            dfs_log1 = list()
            i = 0
            while i < len(dfs_log):
                dfs_log1.append(dfs_log[i][0])
                i += 1
            path_cost = popped[4]
            dfs_path.append(popped[1])
            i = 0
            closed_indices = list()
            while i < len(closed):
                closed_indices.append(closed[i][0])
                i += 1
            #print
            #print popped, closed_indices, popped[3]
            #print closed_indices.index(popped[3]), closed
            next_node = closed[closed_indices.index(popped[3])]
            dfs_path.append(next_node[1])
            while popped[2] != 1:
                #print "next node", next_node, "closed index", closed_indices.index(next_node[3]), "closed of closed index", closed[closed_indices.index(next_node[3])]

                if next_node[3] != 0:
                    next_node = closed[closed_indices.index(next_node[3])]
                dfs_path.append(next_node[1])
                popped[2] -= 1
                #print "depth", popped[2]
            dfs_path.reverse()
            return dfs_log1, dfs_path, path_cost

        #exploring the graph
        up_next = list()
        i = 0

        while i < len(names_dfs):
            #print
            #print "sup", graph[names_bfs.index(curr_name)][i], names_bfs[i]
            bool_flag = True
            dfs_names = list()
            for entry in dfs_log:
                dfs_names.append(entry[0])
            #print dfs_log, bool_flag
            #if bool_flag is True:
            if names_dfs[i] in dfs_names:
                if dfs_log[dfs_names.index(names_dfs[i])][1] < (popped[2] + 1):
                    bool_flag = False
            #print "Is it in log", bool_flag, dfs_log
            for entry in dfs_queue:
                if entry[1] == names[i]:
                    if entry[2] < (popped[2] + 1):
                        bool_flag = False
            #print "is it in queue", bool_flag, dfs_log
            if graph[names_dfs.index(curr_name)][i] != 0:
                if bool_flag is True:
                    up_next.append(names_dfs[i])
                    #print names_bfs[i], "hi2"
            i += 1

        depth += 1
        #print "up next", up_next
        for person in up_next:
            dfs_index += 1
            new_node = [dfs_index, person, popped[2]+1, popped[0], popped[4]+graph_matrix[names_dfs.index(person)][names_dfs.index(popped[1])]]
            #print new_node
            add_flag = True
            for node in dfs_queue:
                if node[1] == new_node[1] and node[2] < new_node[2]:
                    add_flag = False
                    dfs_index -= 1
            if add_flag == True:
                dfs_queue.append(new_node)

        #print dfs_queue




#implementing UCS
def ucs(graph, start, end, names_ucs):
    start_no = names_ucs.index(start)
    depth = 0
    ucs_index = 1
    ucs_queue = list()
    closed = list()
    ucs_queue.append([ucs_index, start, depth, 0, 0, 0])
    names_visited = [0] * len(names_ucs)
    names_visited[start_no] = 1
    curr_name = start
    ucs_path = list()
    ucs_log = list()

    #deciding which node to pop, alphabetically
    while len(ucs_queue) != 0:
        #print
        poppable_nodes = list()
        min_cost = 0
        #min_cost = dfs_queue[0][2]
        #min_parent = dfs_queue[0][4]
        min_parent = 1
        #print closed
        if len(closed) >= 1:
            min_parent = closed[len(closed)-1][0]
            min_cost = closed[len(closed)-1][2]
        i = 0
        #print "minparent is", min_parent, "mincost", min_cost
        #print ucs_queue
        while i < len(ucs_queue):
            #print ucs_queue[i]
            if ucs_queue[i][5] == min_cost:
                poppable_nodes.append(ucs_queue[i])
            i += 1
        #print poppable_nodes
        pop_index = 0
        i = 0

        #print "poppable nodes are", poppable_nodes
        while i < len(poppable_nodes):
            if poppable_nodes[i][1] < poppable_nodes[pop_index][1]:
                pop_index = i
            i += 1
        if len(poppable_nodes) > 0:
            #print poppable_nodes[pop_index]
            #print "popped is", ucs_queue[ucs_queue.index(poppable_nodes[pop_index])], "end is", end
            popped = ucs_queue.pop(ucs_queue.index(poppable_nodes[pop_index]))
        else:
            popped = ucs_queue.pop(pop_index)

        curr_name = popped[1]
        closed.append(popped)
        ucs_log.append(popped[1])
        #print bfs_log
        path_cost = 0
        if popped[1] == end:
            path_cost = popped[5]
            ucs_path.append(popped[1])
            i = 0
            closed_indices = list()
            while i < len(closed):
                closed_indices.append(closed[i][0])
                i += 1
            #print
            #print popped, closed_indices, popped[3]
            #print closed_indices.index(popped[4]), closed
            next_node = closed[closed_indices.index(popped[4])]
            ucs_path.append(next_node[1])
            while popped[2] != 1:
                #print "next node", next_node, "closed index", closed_indices.index(next_node[4]), "closed of closed index", closed[closed_indices.index(next_node[4])]
                if next_node[4] != 0:
                    next_node = closed[closed_indices.index(next_node[4])]
                ucs_path.append(next_node[1])
                popped[2] -= 1
                #print "depth", popped[2]
            ucs_path.reverse()
            return ucs_log, ucs_path, path_cost

        #exploring the graph
        up_next = list()
        i = 0
        while i < len(names_ucs):
            #print "sup", graph[names_bfs.index(curr_name)][i], names_bfs[i]
            bool_flag = names_ucs[i] in ucs_log or names_ucs[i] in ucs_queue
            #print bool_flag, bfs_log
            if graph[names_ucs.index(curr_name)][i] != 0:
                if bool_flag is False:
                    up_next.append(names_ucs[i])
                    #print names_bfs[i], "hi2"
            i += 1
        up_next.sort()
        depth += 1
        #print up_next
        for person in up_next:
            ucs_index += 1
            new_node = [ucs_index, person, popped[2]+1, names_ucs.index(curr_name), popped[0], popped[5]+graph_matrix[names_ucs.index(person)][names_ucs.index(popped[1])]]
            #print new_node
            add_flag = True
            for node in ucs_queue:
                if node[1] == new_node[1]:
                    add_flag = False
                    ucs_index -= 1
            if add_flag == True:
                ucs_queue.append(new_node)

        temp = list()
        i = 0
        j = 1
        while i < len(ucs_queue):
            while j < len(ucs_queue):
                if ucs_queue[i][1] > ucs_queue[j][1]:
                    temp = ucs_queue[i]
                    ucs_queue[i] = ucs_queue[j]
                    ucs_queue[j] = temp
                j += 1
            i += 1

        #print "finished: ", closed


#output work
if search_method == 1:
    ans_tuple = bfs(graph_matrix, start_name, end_name, names)

if search_method == 2:
    ans_tuple = dfs(graph_matrix, start_name, end_name, names)

if search_method == 3:
    ans_tuple = ucs(graph_matrix, start_name, end_name, names)

if ans_tuple != None:
#if ans_tuple[0] != None and ans_tuple[1] != None and ans_tuple[2] != None:
    log = ans_tuple[0]
    path = ans_tuple[1]
    dist = ans_tuple[2]
    f = open("output.txt", "w")
    log_string = ""
    path_string = ""
    for word in log:
        log_string += str(word).rstrip('^M') + "-"
    log_string = log_string[:-1]
    for word in path:
        path_string += str(word).rstrip('^M') + "-"
    path_string = path_string[:-1]
    f.write(log_string.replace('\r', '') + "\n" + path_string.replace('\r','') + "\n" + str(dist))
    f.close()
    #print log_string, path_string, dist
else:
    f = open("output.txt", "w")
    f.write("NoPathAvailable")
    f.close()











