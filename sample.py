
def recursive_simple_cycles(G):
    def _unblock(thisnode):
        """Recursively unblock and remove nodes from B[thisnode]."""
        if blocked[thisnode]:
            blocked[thisnode] = False
            while B[thisnode]:
                _unblock(B[thisnode].pop())

    def circuit(thisnode, startnode, component):
        closed = False # set to True if elementary path is closed
        path.append(thisnode)
        blocked[thisnode] = True
        for nextnode in component[thisnode]: # direct successors of thisnode
            if nextnode == startnode:
                result.append(path[:])
                closed = True
            elif not blocked[nextnode]:
                if circuit(nextnode, startnode, component):
                    closed = True
        if closed:
            _unblock(thisnode)
        else:
            for nextnode in component[thisnode]:
                if thisnode not in B[nextnode]: # TODO: use set for speedup?
                    B[nextnode].append(thisnode)
        path.pop() # remove thisnode from path
        return closed

    path = [] # stack of nodes in current path
    blocked = defaultdict(bool) # vertex: blocked from search?
    B = defaultdict(list) # graph portions that yield no elementary circuit
    result = [] # list to accumulate the circuits found
    # Johnson's algorithm requires some ordering of the nodes.
    # They might not be sortable so we assign an arbitrary ordering.
    ordering=dict(zip(G,range(len(G))))
    for s in ordering:
        # Build the subgraph induced by s and following nodes in the ordering
        subgraph = G.subgraph(node for node in G
                              if ordering[node] >= ordering[s])
        # Find the strongly connected component in the subgraph
        # that contains the least node according to the ordering
        strongcomp = nx.strongly_connected_components(subgraph)
        mincomp=min(strongcomp,
                    key=lambda nodes: min(ordering[n] for n in nodes))
        component = G.subgraph(mincomp)
        if component:
            # smallest node in the component according to the ordering
            startnode = min(component,key=ordering.__getitem__)
            for node in component:
                blocked[node] = False
                B[node][:] = []
            dummy=circuit(startnode, startnode, component)
    return result

G=nx.DiGraph(nx_pydot.read_dot("cfg.dot"))
G2=nx.DiGraph(nx_pydot.read_dot("cfg_testsum.dot"))

# cycles = recursive_simple_cycles(G2)
# for n in cycles:
# 	print n
nodes = dfs_edges(G)

# for n in path:
# 	print n

for n in nodes:
	print n

# print nx.degree(G)
# print G.graph
# print G['0']
for path in nx.all_simple_paths(G, source='0', target='26'):
	 print(path)

# nx.draw(G)
# nx.draw_spectral(G,with_labels = True)
# pos=nx.spring_layout(G)
# nx.draw_networkx_nodes(G,pos,node_size=26,node_color='w',alpha=0.4)
# labels=nx.draw_networkx_labels(G,pos=nx.nx_agraph.graphviz_layout(G))
# plt.savefig("cfg3.png")
# plt.show()