import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_has_url(self):
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        self.assertEqual(node.url, "https://example.com")

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()