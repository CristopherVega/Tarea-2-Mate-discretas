from graphList import GraphList
from graph_matrix import GraphMatrix

for Clase in (GraphList, GraphMatrix):
    g = Clase()
    for v in ["Auth", "API", "BD", "Notif"]:
        g.add_vertex(v)
    g.add_edge("Auth", "API")
    g.add_edge("API", "BD")
    g.add_edge("API", "Notif")

    print(Clase.__name__)
    print("  Vértices:", g.vertices())
    print("  Aristas:", g.edges())
    print("  Grado API:", g.degree("API"))