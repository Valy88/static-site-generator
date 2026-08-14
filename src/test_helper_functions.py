import unittest
from helper_functions import split_nodes_delimiter
from textnode import TextNode, TextType

class TestHelperFunctions(unittest.TestCase):
  def test_split_nodes_delimiter(self):
    old_nodes = [
      TextNode("This is a text node", TextType.TEXT),
      TextNode("This is a bold text node", TextType.BOLD),
      TextNode("This is a link text node", TextType.ITALIC),
    ]
    delimiter = " "
    text_type = TextType.TEXT
    new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    self.assertEqual(len(new_nodes), 7)
    self.assertEqual(new_nodes[0].text, "This")
    self.assertEqual(new_nodes[1].text, "is")
    self.assertEqual(new_nodes[2].text, "a")
    self.assertEqual(new_nodes[3].text, "text")
    self.assertEqual(new_nodes[4].text, "node")

  def test_split_nodes_delimiter_bold(self):
    old_nodes = [
      TextNode("This contains a **bold** text node", TextType.TEXT),
    ]
    delimiter = "**"
    text_type = TextType.TEXT
    new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "This contains a ")
    self.assertEqual(new_nodes[1].text, "bold")
    self.assertEqual(new_nodes[2].text, " text node")

if __name__ == "__main__":
  unittest.main()