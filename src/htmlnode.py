from typing import Union, List, Dict

class HTMLNode():
  def __init__(self, tag: Union[str, None] = None, value: Union[str, None] = None, children: Union[List['HTMLNode'], None] = None, props: Union[Dict[str, str], None] = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("Child classes will override this method to render themselves as HTML")

  def props_to_html(self):
    if not self.props:
      return ""
    html_props = ""
    for key, value in self.props.items():
      html_props += f' {key}="{value}"'
    return html_props

  def __repr__(self):
    return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
  def __init__(self, tag: Union[str, None], value: Union[str, None], props: Union[Dict[str, str], None] = None):
    super().__init__(tag=tag, value=value, props=props)

  def to_html(self):
    if self.value is None:
      raise ValueError("LeafNode must have a value to render as HTML")
    if self.tag is None:
      return self.value
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

  def __repr__(self):
    return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
  def __init__(self, tag: Union[str, None], children: Union[List['HTMLNode'], None], props: Union[Dict[str, str], None] = None):
    super().__init__(tag=tag, children= children, props=props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("ParentNode must have a tag to render as HTML")
    if self.children is None:
      raise ValueError("ParentNode must have children to render as HTML")
    html_tags = f"<{self.tag}{self.props_to_html()}>"
    for child in self.children:
      html_tags += child.to_html()
    html_tags += f"</{self.tag}>"
    return html_tags
