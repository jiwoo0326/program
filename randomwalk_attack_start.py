def attack_agent(agent):
        # 「始点法」

    # Count the number of past visits.
    counter = collections.Counter(agent.path)
    g = agent.graph
    u = agent.current
    # Try to rewire to frequently-visisted vertex.
    # for v, count in counter.most_common():
    
    p = sorted(set(agent.path), key=agent.path.index)
    
    for v in p:
        # u: current vertex
        # v: one of frequently-visisted vertices
        if g.has_edge(u, v):
            continue
        # Try to find link (u, w) which can be safely deleted without isolating
        # the graph into multiple components.
        neighbors = list(g.neighbors(u))
        random.shuffle(neighbors)
        for w in neighbors:
            h = g.copy_graph()
            h.delete_edge(u, w)
            # The graph still remains connected after link deletion?
            if h.is_connected():
                # Rewrire the link to the (possible) central vertex.
                g.delete_edge(u, w)
                g.add_edge(u, v)
                return True
    return False
