import json
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from graph_matrix import GraphMatrix


def servicios():
    g = GraphMatrix()
    for v in ["Auth", "API", "BD", "Notif"]:
        g.add_vertex(v)
    g.add_edge("Auth", "API")
    g.add_edge("API", "BD")
    g.add_edge("API", "Notif")
    return g


def test_grafo_vacio():
    g = GraphMatrix()
    assert len(g) == 0 and g.edges() == []
    assert json.loads(g.to_json())["vertices"] == []


def test_vertice_aislado():
    g = GraphMatrix()
    g.add_vertex("X")
    assert g.degree("X") == 0


def test_grados():
    g = servicios()
    assert g.degree("API") == 3
    assert g.degree("Auth") == 1


def test_arista_duplicada_no_se_repite():
    g = servicios()
    g.add_edge("Auth", "API", weight=5)
    assert len(g.edges()) == 3
    assert ("Auth", "API", 5) in g.edges()


def test_eliminar_vertice_con_aristas():
    g = servicios()
    g.remove_vertex("API")
    assert g.edges() == []
    assert g.vertices() == ["Auth", "BD", "Notif"]
    assert g.degree("BD") == 0


def test_vertice_inexistente():
    with pytest.raises(KeyError):
        GraphMatrix().add_edge("A", "B")


def test_dirigido():
    g = GraphMatrix(directed=True)
    g.add_vertex("A"); g.add_vertex("B")
    g.add_edge("A", "B")
    assert g.out_degree("A") == 1 and g.in_degree("B") == 1
    assert not g.has_edge("B", "A")


def test_bucle_suma_dos():
    g = GraphMatrix()
    g.add_vertex("A")
    g.add_edge("A", "A")
    assert g.degree("A") == 2


def test_to_networkx():
    nx = pytest.importorskip("networkx")
    g = servicios().to_networkx()
    assert g.number_of_nodes() == 4 and g.number_of_edges() == 3