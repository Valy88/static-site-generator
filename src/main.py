import sys

from textnode import TextNode, TextType
from helper_functions import copy_static_to_docs, generate_page, generate_pages_recursive

print("Hello, World!")

def main():
  basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
  copy_static_to_docs()
  generate_pages_recursive("content", "template.html", "docs", basepath)
  text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(text_node)

main()