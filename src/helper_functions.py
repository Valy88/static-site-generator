from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from typing import List

from enum import Enum

import re
import os
import shutil

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
  if re.fullmatch(r"^>\s?.+(?:\n>\s?.+)*$", markdown):
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

def markdown_to_html_node(markdown: str):
  markdown_blocks = markdown_to_blocks(markdown)
  html_nodes = []
  for markdown_block in markdown_blocks:
    html_node = block_to_html_node(markdown_block)
    html_nodes.append(html_node)
  return ParentNode("div", html_nodes)

def block_to_html_node(block: str) -> ParentNode:
  block_type = block_to_block_type(block)
  if block_type == BlockType.PARAGRAPH:
    return paragraph_to_html_node(block)
  if block_type == BlockType.HEADING:
    return heading_to_html_node(block)
  if block_type == BlockType.CODE:
    return code_to_html_node(block)
  if block_type == BlockType.OLIST:
    return olist_to_html_node(block)
  if block_type == BlockType.ULIST:
    return ulist_to_html_node(block)
  if block_type == BlockType.QUOTE:
    return quote_to_html_node(block)
  raise ValueError("invalid block type")

def text_to_children(text: str) -> List[LeafNode]:
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    children.append(text_node_to_html_node(text_node))
  return children

def paragraph_to_html_node(block: str) -> ParentNode:
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
  level = 0
  for char in block:
    if char == "#":
      level += 1
    else:
      break
  if level + 1 >= len(block):
    raise ValueError(f"invalid heading level: {level}")
  text = block[level + 1 :]
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("invalid code block")
  text = block[4:-3]
  raw_text_node = TextNode(text, TextType.TEXT)
  child = text_node_to_html_node(raw_text_node)
  code = ParentNode("code", [child])
  return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
  items = block.split("\n")
  html_items = []
  for item in items:
    parts = item.split(". ", 1)
    text = parts[1]
    children = text_to_children(text)
    html_items.append(ParentNode("li", children))
  return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[2:]
    children = text_to_children(text)
    html_items.append(ParentNode("li", children))
  return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode("blockquote", children)

def empty_public(public_dir: str) -> None:
  for item in os.listdir(public_dir):
    item_path = os.path.join(public_dir, item)
    if not os.path.exists(item_path):
      continue
    if os.path.isfile(item_path):
      os.unlink(item_path)
    elif (os.path.isdir(item_path)):
      shutil.rmtree(item_path)

def copy_static_to_public() -> None:
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  public_dir = os.path.join(base_dir, "public")
  static_dir = os.path.join(base_dir, "static")
  empty_public(public_dir)
  def copy_static(static_items_list):
    if not static_items_list:
      return
    static_item = static_items_list[0]
    static_item_path = os.path.join(static_dir, static_item)
    if os.path.exists(static_item_path):
      if os.path.isfile(static_item_path):
        head, tail = os.path.split(static_item)
        copy_path = shutil.copy(static_item_path, os.path.join(public_dir, head))
        print(f"copied {static_item_path} into {copy_path}")
      else:
        dir_path = os.path.join(public_dir, static_item)
        os.mkdir(dir_path)
        print(f"created dir {dir_path}")
        dir_contents = os.listdir(static_item_path)
        dir_file_paths = []
        for dir_content in dir_contents:
          dir_file_paths.append(os.path.join(static_item, dir_content))
        copy_static(dir_file_paths)
    copy_static(static_items_list[1:])

  return copy_static(os.listdir(static_dir))

def extract_title(markdown: str) -> str:
  markdown_blocks = markdown_to_blocks(markdown)
  title = ""
  for markdown_block in markdown_blocks:
    markdown_block_lines = markdown_block.split("\n")
    for markdown_block_line in markdown_block_lines:
      markdown_parts = markdown_block_line.split(" ", 1)
      if markdown_parts[0] == "#":
        title = markdown_parts[1]
        break
    if title:
      break
  if not title:
    raise Exception("There is not h1 header to extract title from")
  return title

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  try:
    with open(from_path, "r", encoding="utf-8") as markdown_file:
      markdown = markdown_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
      template = template_file.read()

    markdown_html = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)

    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", markdown_html)

    destination_dir = os.path.dirname(dest_path)
    if destination_dir:
      os.makedirs(destination_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as dest_file:
      dest_file.write(template)

  except Exception as e:
    print(f"Error: {e}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
  content_dir_paths = os.listdir(dir_path_content)
  for content_dir_path in content_dir_paths:
    item_path = os.path.join(dir_path_content, content_dir_path)
    if os.path.isfile(item_path):
      (root, ext) = os.path.splitext(content_dir_path)
      html_file_path = f"{root}.html"
      dest_item_path = os.path.join(dest_dir_path, html_file_path)
      generate_page(item_path, template_path, dest_item_path)
    else:
      dest_dir = os.path.join(dest_dir_path, content_dir_path)
      generate_pages_recursive(item_path, template_path, dest_dir)