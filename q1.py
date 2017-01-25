import networkx as nx
import matplotlib.pyplot as plt
import networkx.drawing.nx_pydot as nx_pydot
from collections import defaultdict
import re
# G = nx.Graph()

def extract_if_expression(label):
	# m = re.search("==",label)
	m = re.search('if(.+?)goto', label)
	if m:
		return m.group(1)
	return None

def dfs_edges(G, source=None):	
	path = list()
	if source is None:
		nodes = G
	else:
		nodes = [source]
	visited=set()
	for start in nodes:
		if start in visited:
			continue
		visited.add(start)
		stack = [(start,iter(G[start]))]
	
		while stack:
			parent,children = stack[-1]
			try:
				child = next(children)
				label = G.node[child]['label']
				if "if" in label:
					
					# print extract_expression(label)
					exp = extract_if_expression(label)
					exp = exp.strip()
					path.append(exp)			
				if child not in visited:
					visited.add(child)
					stack.append((child,iter(G[child])))
			except StopIteration:
				stack.pop()
	return path



def reverse_operators(exp):
	if "==" in exp:
		return exp.replace("==","!=")
	else:
		return exp.replace("!=","==")
	

G=nx.DiGraph(nx_pydot.read_dot("cfg.dot"))



paths = dfs_edges(G)

print paths
# for n in path:
# 	print n
new_paths = list()
for n in paths:
	temp = reverse_operators(n)
	new_paths.append(temp);

print new_paths
all_path = list();
for p in paths:
	for np in new_paths:
		print p + " && " + np




# print nx.degree(G)
# print G.graph
# print G['0']
# for path in nx.all_simple_paths(G, source='0', target='26'):
# 	 print(path)

# nx.draw(G)
# nx.draw_spectral(G,with_labels = True)
# pos=nx.spring_layout(G)
# nx.draw_networkx_nodes(G,pos,node_size=26,node_color='w',alpha=0.4)
# labels=nx.draw_networkx_labels(G,pos=nx.nx_agraph.graphviz_layout(G))
# plt.savefig("cfg3.png")
# plt.show()