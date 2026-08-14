from textnode import TextNode, TextType
from typing import List

import re

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

def text_to_textnodes(text):
  text_nodes = [TextNode(text, TextType.TEXT)]
  text_nodes = split_nodes_delimiter(text_nodes, '**', TextType.BOLD)
  text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
  text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
  text_nodes = split_nodes_link(text_nodes)
  return split_nodes_image(text_nodes)