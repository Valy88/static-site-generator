import unittest
from helper_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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
    text_type = TextType.BOLD
    new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "This contains a ")
    self.assertEqual(new_nodes[1].text, "bold")
    self.assertEqual(new_nodes[2].text, " text node")

  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a link [example url](https://example.com)"
    )
    self.assertListEqual([("example url", "https://example.com")], matches)

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )

  def test_split_Link(self):
    node = TextNode(
        "This is text with a link [first link](https://example.com) and another link [second link](https://google.com)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("first link", TextType.LINK, "https://example.com"),
            TextNode(" and another link ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://google.com"),
        ],
        new_nodes,
    )

  def test_text_to_textnodes(self):
    new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    self.assertEqual(
        [
          TextNode("This is ", TextType.TEXT),
          TextNode("text", TextType.BOLD),
          TextNode(" with an ", TextType.TEXT),
          TextNode("italic", TextType.ITALIC),
          TextNode(" word and a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" and an ", TextType.TEXT),
          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
          TextNode(" and a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
      new_nodes
    )

if __name__ == "__main__":
  unittest.main()