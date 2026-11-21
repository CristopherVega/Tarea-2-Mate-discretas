class GraphList:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = set()

    def remove_vertex(self, v):
        if v not in self.adj:
            raise KeyError(f"El vertice {v} no existe")
        del self.adj[v]
        for u in self.adj:
            self.adj[u].discard(v)

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].add(v)
        if not self.directed:
            self.adj[v].add(u)

    def remove_edge(self, u, v):
        if not self.has_edge(u, v):
            raise KeyError(f"La arista ({u}, {v}) no existe")
        self.adj[u].remove(v)
        if not self.directed:
            self.adj[v].discard(u)

    def has_edge(self, u, v):
        return u in self.adj and v in self.adj[u]

    def out_degree(self, v):
        if v not in self.adj:
            raise KeyError(f"El vertice {v} no existe")
        return len(self.adj[v])

    def in_degree(self, v):
        if v not in self.adj:
            raise KeyError(f"El vertice {v} no existe")
        return sum(1 for u in self.adj if v in self.adj[u])

    def degree(self, v):
        if v not in self.adj:
            raise KeyError(f"El vertice {v} no existe")
        if self.directed:
            return self.in_degree(v) + self.out_degree(v)
        if v in self.adj[v]:
            return len(self.adj[v]) + 1
        return len(self.adj[v])

    def vertices(self):
        return list(self.adj)

    def neighbors(self, v):
        if v not in self.adj:
            raise KeyError(f"El vertice {v} no existe")
        return list(self.adj[v])

    def edges(self):
        result = []
        visited = set()
        for u in self.adj:
            for v in self.adj[u]:
                if self.directed or v not in visited:
                    result.append((u, v))
            visited.add(u)
        return result