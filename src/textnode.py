from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text and self.text_type == other.text_type and self.url == other.url):
            return True
        else:
            return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise Exception("Wrong type")
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            splited_node = node.text.split(delimiter)
            if len(splited_node) % 2 == 0:
                raise ValueError("Wrong Markdown")
            else:
                for i in range(len(splited_node)):
                    if splited_node[i] == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(splited_node[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(splited_node[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def helper_split_image(section):
    new_node = []
    match = extract_markdown_images(section)
    if len(match) <= 0:
        return [TextNode(section, TextType.TEXT)]
    else:
        alt = match[0][0]
        url = match[0][1]
        sections = section.split(f"![{alt}]({url})", 1)
        if sections[0] != "":
            new_node.append(TextNode(sections[0], TextType.TEXT))
        new_node.append(TextNode(alt, TextType.IMAGE, url))
        if sections[1] != "":
            new_node.extend(helper_split_image(sections[1]))
    return new_node

def helper_split_link(section):
    new_node = []
    match = extract_markdown_links(section)
    if len(match) <= 0:
        return [TextNode(section, TextType.TEXT)]
    else:
        alt = match[0][0]
        url = match[0][1]
        sections = section.split(f"[{alt}]({url})", 1)
        if sections[0] != "":
            new_node.append(TextNode(sections[0], TextType.TEXT))
        new_node.append(TextNode(alt, TextType.LINK, url))
        if sections[1] != "":
            new_node.extend(helper_split_link(sections[1]))
    return new_node


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(helper_split_image(node.text))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(helper_split_link(node.text))
        else:
            new_nodes.append(node)
    return new_nodes
           
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

