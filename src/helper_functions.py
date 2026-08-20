from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from typing import List

from enum import Enum

import re

class BlockType(Enum):
  PARAGRAPH="paragraph"
  HEADING="heading"
  CODE="code"
  QUOTE="quote"
  ULIST="unordered_list"
  OLIST="ordered_list"

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
  new_nodes: List[TextNode] = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    split_texts = node.text.split(delimiter)
    if len(split_texts) % 2 == 0:
      raise ValueError(f"Delimiter '{delimiter}' must be used in pairs for text type '{text_type.value}'")
    for i, split_text in enumerate(split_texts):
      if len(split_text) == 0:
        continue
      current_text_type = text_type if i % 2 == 1 else TextType.TEXT
      new_nodes.append(TextNode(split_text, current_text_type))
  return new_nodes

def extract_markdown_images(text: str) -> List[tuple]:
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> List[tuple]:
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_text_by_url_items(extracted_url_items, node, item_type = TextType.IMAGE):
  split_text = []
  for extracted_url_item in extracted_url_items:
    url_item_text = extracted_url_item[0]
    url_item_link = extracted_url_item[1]
    url_item = f"[{url_item_text}]({url_item_link})"
    if item_type == TextType.IMAGE:
      url_item = '!' + url_item
    if len(split_text) == 0:
      split_text = node.text.split(url_item, 1)
      split_text.insert(1, [url_item_text, url_item_link])
      continue
    split_text[-1:] = split_text[-1].split(url_item, 1)
    split_text.insert(len(split_text) - 1, [url_item_text, url_item_link])
  return split_text

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
  new_nodes: List[TextNode] = []
  for node in old_nodes:
    extracted_images = extract_markdown_images(node.text)
    if len(extracted_images) == 0:
      new_nodes.append(node)
      continue
    split_text = split_text_by_url_items(extracted_images, node, TextType.IMAGE)
    for split_item in split_text:
      if len(split_item) == 0:
        continue
      if isinstance(split_item, list):
        new_nodes.append(TextNode(split_item[0], TextType.IMAGE, split_item[1]))
      else:
        new_nodes.append(TextNode(split_item, TextType.TEXT))
  return new_nodes

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
  new_nodes: List[TextNode] = []
  for node in old_nodes:
    extracted_links = extract_markdown_links(node.text)
    if len(extracted_links) == 0:
      new_nodes.append(node)
      continue
    split_text = split_text_by_url_items(extracted_links, node, TextType.LINK)
    for split_item in split_text:
      if len(split_item) == 0:
        continue
      if isinstance(split_item, list):
        new_nodes.append(TextNode(split_item[0], TextType.LINK, split_item[1]))
      else:
        new_nodes.append(TextNode(split_item, TextType.TEXT))
  return new_nodes

def text_to_textnodes(text: str) -> List[TextNode]:
  text_nodes = [TextNode(text, TextType.TEXT)]
  text_nodes = split_nodes_delimiter(text_nodes, '**', TextType.BOLD)
  text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
  text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
  text_nodes = split_nodes_link(text_nodes)
  return split_nodes_image(text_nodes)

def markdown_to_blocks(markdown: str) -> List[str]:
  blocks = []
  for block in markdown.split('\n\n'):
    cleaned_lines = [line.strip() for line in block.splitlines()]
    cleaned_block = '\n'.join(line for line in cleaned_lines if len(line) > 0)
    if len(cleaned_block) > 0:
      blocks.append(cleaned_block)
  return blocks

def block_to_block_type (markdown: str) -> BlockType:
  if re.fullmatch(r"^#{1,6} .+$", markdown) != None:
    return BlockType.HEADING
  if re.fullmatch(r"^```\n(.+\n)+```$", markdown) != None:
    return BlockType.CODE
  if re.fullmatch(r"^>\s?.+$", markdown) != None:
    return BlockType.QUOTE
  if re.fullmatch(r"^(?:-\s.+(?:\n|$))+", markdown) != None:
    return BlockType.ULIST
  lines = markdown.splitlines()
  valid = all(
    re.match(rf"^{i}\. .+$", line)
    for i, line in enumerate(lines, 1)
  )
  if valid:
    return BlockType.OLIST
  return BlockType.PARAGRAPH

def block_type_to_tag(markdown_block: str, block_type: BlockType) -> str:
  if block_type == BlockType.HEADING:
    return f"h{markdown_block.split()[0].count('#')}"
  if block_type == BlockType.CODE:
    return "code"
  if block_type == BlockType.QUOTE:
    return "blockquote"
  if block_type == BlockType.ULIST:
    return "ul"
  if block_type == BlockType.OLIST:
    return "ol"
  return "p"

def text_to_children(text: str) -> List[LeafNode]:
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    children.append(text_node_to_html_node(text_node))
  return children

def markdown_to_html_node(markdown: str):
  markdown_blocks = markdown_to_blocks(markdown)
  html_nodes = []
  for markdown_block in markdown_blocks:
    block_type = block_to_block_type(markdown_block)
    if (block_type == BlockType.CODE):
      code_lines = markdown_block.splitlines()
      code_text = "\n".join(code_lines[1:-1]) + "\n"
      code_text_node = TextNode(code_text, TextType.CODE)
      code_html_node = text_node_to_html_node(code_text_node)
      html_node = ParentNode("pre", [code_html_node])
    else:
      markdown_block = markdown_block.replace("\n", " ")
      tag = block_type_to_tag(markdown_block, block_type)
      children = text_to_children(markdown_block)
      html_node = ParentNode(tag, children)
    html_nodes.append(html_node)
  return ParentNode("div", html_nodes)