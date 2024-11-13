def attack_agent(agent):
  # 「クラスタ法」
    # Count the number of past visits.
    g = agent.graph
    u = agent.current
    path = set(agent.path)
    nx_graph = nx.Graph()
    # Iterate over the vertices of the Graph-tool graph and add them to the NetworkX graph
    for v in path:
        nx_graph.add_node(int(v))

    # Iterate over the edges of the Graph-tool graph and add them to the NetworkX graph
    path_edge = set()
    for i in range(len(agent.path)-1):
        s_t = (agent.path[i], agent.path[i+1])
        t_s = (agent.path[i+1], agent.path[i])
        if s_t in path_edge or t_s in path_edge:
            continue
        else:
            path_edge.add(s_t)

    for e in path_edge:
        source = e[0]
        target = e[1]
        nx_graph.add_edge(source, target)

    # Compute the best partition using the Louvain algorithm
    partition = community.best_partition(nx_graph)
    hk_count = [0] * len(set(partition.values()))
    hk = set(agent.path)
    for node, cluster_id in partition.items():
        hk_count[cluster_id] += 1
    max_cluster_id = hk_count.index(max(hk_count))
    max_cluster = [key for key, value in partition.items() if value==max_cluster_id]
    for i in range(len(max_cluster)):
        target = random.choice(max_cluster)
        if g.has_edge(u, target):
            continue
        neighbors = list(g.neighbors(u))
        random.shuffle(neighbors)
        for w in neighbors:
            h = g.copy_graph()
            h.delete_edge(u, w)
            # The graph still remains connected after link deletion?
            if h.is_connected():
                # Rewrire the link to the (possible) central vertex.
                g.delete_edge(u, w)
                g.add_edge(u, target)
                return True    
        return False