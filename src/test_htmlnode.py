import unittest
from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()