import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode("a", "This is a link")
        self.assertEqual(node.props_to_html(), "")

    def test_node_with_children(self):
        child_node = HTMLNode("b", "This is bold text")
        node = HTMLNode("p", "This is a paragraph", children=[child_node])
        self.assertEqual(node.children[0].props_to_html(), child_node.props_to_html())

    def test_node_with_props(self):
        node = HTMLNode("a", "This is a link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
            node = LeafNode("a", "Hello, world!", props={"href": "https://example.com"})
            self.assertEqual(node.to_html(), '<a href="https://example.com">Hello, world!</a>')

if __name__ == "__main__":
    unittest.main()