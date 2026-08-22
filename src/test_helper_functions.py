import unittest
from helper_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title
from textnode import TextNode, TextType

class TestHelperFunctions(unittest.TestCase):
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

  def test_split_nodes_delimiter_multiple(self):
    old_nodes = [
      TextNode("This is a **bold** text node and this is an _italic_ text node", TextType.TEXT),
    ]
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    self.assertEqual(
        [
          TextNode("This is a ", TextType.TEXT),
          TextNode("bold", TextType.BOLD),
          TextNode(" text node and this is an ", TextType.TEXT),
          TextNode("italic", TextType.ITALIC),
          TextNode(" text node", TextType.TEXT),
      ],
      new_nodes
    )

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

  def test_markdown_to_blocks(self):
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_block_to_block_type_ol(self):
    md = """
    1. First line
    2. Second line
    3. Third line
    """
    md_blocks = markdown_to_blocks(md)
    block_type = block_to_block_type(md_blocks[0])
    self.assertAlmostEqual(block_type, BlockType.OLIST)

  def test_paragraphs(self):
    md = """
      This is **bolded** paragraph
      text in a p
      tag here

      This is another paragraph with _italic_ text and `code` here

    """

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


  def test_codeblock(self):
    md = """
      ```
      This is text that _should_ remain
      the **same** even with inline stuff
      ```
    """

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

  def test_extract_title_heading(self):
    md = """
      This is some random text
      # This is the title from the heading
      ## This is a second heading which should not register
      Another paragraph of random text
    """

    title = extract_title(md)
    self.assertEqual(
      title,
      "This is the title from the heading"
    )

  def test_extract_title_exception(self):
    md = """
      This is some random text
      Another paragraph of random text

      No h1 heading present in this one

      ### Some h3 heading just for kicks
    """

    with self.assertRaises(Exception) as context:
      extract_title(md)

    self.assertEqual(
      str(context.exception),
      "There is not h1 header to extract title from"
    )

if __name__ == "__main__":
  unittest.main()