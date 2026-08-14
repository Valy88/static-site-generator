from textnode import TextNode, TextType
from typing import List

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
  new_nodes: List[TextNode] = []
  for node in old_nodes:
    if node.text_type != text_type:
      new_nodes.append(node)
      continue
    split_texts = node.text.split(delimiter)
    if len(split_texts) % 2 == 0:
      raise ValueError(f"Delimiter '{delimiter}' must be used in pairs for text type '{text_type.value}'")
    print("split texts:", split_texts)
    for split_text in split_texts:
      new_nodes.append(TextNode(split_text, text_type))
  return new_nodes