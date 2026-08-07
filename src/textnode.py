from enum import Enum
from typing import Union

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