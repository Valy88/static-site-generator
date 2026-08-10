from typing import Union, List, Dict

class HTMLNode():
  def __init__(self, tag: str, value: str = None, children: Union[List['HTMLNode'], None] = None, props: Union[Dict[str, str], None] = None):
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