import unittest

from graphList import GraphList


class TestNoDirigido(unittest.TestCase):
    def setUp(self):
        self.g = GraphList()
        self.g.add_edge("A", "B")
        self.g.add_edge("A", "C")
        self.g.add_edge("B", "C")

    def test_add_vertex(self):
        self.g.add_vertex("D")
        self.assertIn("D", self.g.vertices())
        self.assertEqual(self.g.degree("D"), 0)

    def test_add_edge_simetrica(self):
        self.assertTrue(self.g.has_edge("A", "B"))
        self.assertTrue(self.g.has_edge("B", "A"))

    def test_degree(self):
        self.assertEqual(self.g.degree("A"), 2)

    def test_autolazo(self):
        self.g.add_edge("A", "A")
        self.assertEqual(self.g.degree("A"), 4)

    def test_remove_edge(self):
        self.g.remove_edge("A", "B")
        self.assertFalse(self.g.has_edge("A", "B"))
        self.assertFalse(self.g.has_edge("B", "A"))

    def test_remove_edge_inexistente(self):
        with self.assertRaises(KeyError):
            self.g.remove_edge("A", "Z")

    def test_remove_vertex(self):
        self.g.remove_vertex("A")
        self.assertNotIn("A", self.g.vertices())
        self.assertEqual(self.g.neighbors("B"), ["C"])

    def test_vertice_inexistente(self):
        with self.assertRaises(KeyError):
            self.g.degree("Z")
        with self.assertRaises(KeyError):
            self.g.remove_vertex("Z")

    def test_edges_sin_repetir(self):
        self.assertEqual(len(self.g.edges()), 3)


class TestDirigido(unittest.TestCase):
    def setUp(self):
        self.g = GraphList(directed=True)
        self.g.add_edge(1, 2)
        self.g.add_edge(1, 3)
        self.g.add_edge(3, 1)
        self.g.add_edge(2, 3)

    def test_no_simetrica(self):
        self.assertTrue(self.g.has_edge(1, 2))
        self.assertFalse(self.g.has_edge(2, 1))

    def test_grados(self):
        self.assertEqual(self.g.out_degree(1), 2)
        self.assertEqual(self.g.in_degree(1), 1)
        self.assertEqual(self.g.degree(1), 3)

    def test_remove_edge(self):
        self.g.remove_edge(1, 3)
        self.assertFalse(self.g.has_edge(1, 3))
        self.assertTrue(self.g.has_edge(3, 1))

    def test_remove_vertex(self):
        self.g.remove_vertex(1)
        self.assertEqual(self.g.edges(), [(2, 3)])
        self.assertEqual(self.g.in_degree(2), 0)

    def test_edges(self):
        self.assertEqual(len(self.g.edges()), 4)


if __name__ == "__main__":
    unittest.main()