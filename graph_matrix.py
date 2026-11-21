import json


class GraphMatrix:
    """Grafo con matriz de adyacencia. None = sin arista; otro valor = peso."""

    def __init__(self, directed=False):
        self.directed = directed
        self._names = []   # índice -> nombre del vértice
        self._index = {}   # nombre -> índice
        self._m = []       # matriz V x V

    # ---------- vértices ----------
    def add_vertex(self, v):
        if v in self._index:
            return False
        self._index[v] = len(self._names)
        self._names.append(v)
        for row in self._m:
            row.append(None)
        self._m.append([None] * len(self._names))
        return True

    def remove_vertex(self, v):
        i = self._require(v)
        del self._m[i]
        for row in self._m:
            del row[i]
        del self._names[i]
        self._index = {name: k for k, name in enumerate(self._names)}

    def vertices(self):
        return list(self._names)

    # ---------- aristas ----------
    def add_edge(self, u, v, weight=1):
        i, j = self._require(u), self._require(v)
        self._m[i][j] = weight          # si ya existe, actualiza el peso
        if not self.directed:
            self._m[j][i] = weight

    def remove_edge(self, u, v):
        i, j = self._require(u), self._require(v)
        self._m[i][j] = None
        if not self.directed:
            self._m[j][i] = None

    def has_edge(self, u, v):
        i, j = self._require(u), self._require(v)
        return self._m[i][j] is not None

    def edges(self):
        result = []
        n = len(self._names)
        for i in range(n):
            start = 0 if self.directed else i
            for j in range(start, n):
                w = self._m[i][j]
                if w is not None:
                    result.append((self._names[i], self._names[j], w))
        return result

    # ---------- grados ----------
    def out_degree(self, v):
        i = self._require(v)
        return sum(1 for w in self._m[i] if w is not None)

    def in_degree(self, v):
        j = self._require(v)
        return sum(1 for row in self._m if row[j] is not None)

    def degree(self, v):
        if self.directed:
            return self.in_degree(v) + self.out_degree(v)
        i = self._require(v)
        d = self.out_degree(v)
        if self._m[i][i] is not None:   # un bucle suma 2 en no dirigidos
            d += 1
        return d

    # ---------- exportación ----------
    def to_dict(self):
        return {
            "directed": self.directed,
            "vertices": self.vertices(),
            "edges": [{"source": u, "target": v, "weight": w}
                      for u, v, w in self.edges()],
        }

    def to_json(self, path=None, indent=2):
        text = json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        return text

    def to_networkx(self):
        import networkx as nx
        g = nx.DiGraph() if self.directed else nx.Graph()
        g.add_nodes_from(self.vertices())
        for u, v, w in self.edges():
            g.add_edge(u, v, weight=w)
        return g

    # ---------- auxiliares ----------
    def _require(self, v):
        if v not in self._index:
            raise KeyError(f"El vértice '{v}' no existe")
        return self._index[v]

    def __len__(self):
        return len(self._names)