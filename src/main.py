from textnode import TextNode, TextType
from helper_functions import copy_static_to_public, generate_page

print("Hello, World!")

def main():
  copy_static_to_public()
  generate_page("content/index.md", "template.html", "public/index.html")
  text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(text_node)

main()