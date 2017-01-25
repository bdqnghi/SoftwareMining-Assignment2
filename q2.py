import networkx as nx
import matplotlib.pyplot as plt
import networkx.drawing.nx_pydot as nx_pydot
from collections import defaultdict
import re

def extract_assign_expression(label):
	# m = re.search("==",label)
	m = re.search('if(.+?)goto', label)
	if m:
		return m.group(1)
	return None

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

def find_branching_node(cycle):
	for n in cycle:
		label = G2.node[n]['label']
		if "if" in label:
			return n
	return None

def find_assignment_node(cycle):
	node = list()
	for n in cycle:
		label = G2.node[n]['label']
		if "=" in label:
			node.append(n)
	return node

def extract_branching_condition(node):
	label = G2.node[node]['label']
	label = label.strip()
	m = re.findall(r'\b\d+\b', label)
	if m:
		return m[0]
	return None

def path_constrain(cycle):
	branching_node = find_branching_node(cycle)
	assignment_nodes = find_assignment_node(cycle)
	print assignment_nodes
	condition = extract_branching_condition(branching_node)
	for i in range(int(condition)):
		print i 


G2=nx.DiGraph(nx_pydot.read_dot("cfg_testsum.dot"))

cycles = recursive_simple_cycles(G2)
cycle = cycles[0]

# print find_branching_node(cycle)
# for n in cycle:
# 	print G2.node[n]

path_constrain(cycle)