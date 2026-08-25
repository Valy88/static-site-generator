from textnode import TextNode, TextType
from helper_functions import copy_static_to_public, generate_page, generate_pages_recursive

print("Hello, World!")

def main():
  copy_static_to_public()
  generate_pages_recursive("content", "template.html", "public")
  # generate_page("content/index.md", "template.html", "public/index.html")
  text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(text_node)

main()