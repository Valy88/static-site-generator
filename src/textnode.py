from enum import Enum
from typing import Set, Union

from htmlnode import LeafNode

class TextType(Enum):
  PLAIN="text"
  BOLD="bold"
  ITALIC="italic"
  CODE="code"
  LINK="link"
  IMAGE="image"

class TextNode():
  def __init__(self, text: str, text_type: TextType, url: Union[str, None] = None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other):
    if not isinstance(other, TextNode):
      return False
    return self.text == other.text and self.text_type == other.text_type and self.url == other.url

  def __repr__(self):
    return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"
  def __repr__(self):
    return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"


def text_node_to_html_node(text_node: 'TextNode') -> LeafNode:
  if not isinstance(text_node.text_type, TextType):
    raise ValueError(f"Invalid text type: {text_node.text_type}")
  if text_node.text_type == TextType.PLAIN:
    return LeafNode(tag=None, value=text_node.text)
  elif text_node.text_type == TextType.BOLD:
    return LeafNode(tag="b", value=text_node.text)
  elif text_node.text_type == TextType.ITALIC:
    return LeafNode(tag="i", value=text_node.text)
  elif text_node.text_type == TextType.CODE:
    return LeafNode(tag="code", value=text_node.text)
  elif text_node.text_type == TextType.LINK:
    if not text_node.url:
      raise ValueError("Link text node must have a URL")
    return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
  elif text_node.text_type == TextType.IMAGE:
    if not text_node.url:
      raise ValueError("Image text node must have a URL")
    return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})