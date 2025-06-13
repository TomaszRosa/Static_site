from enum import Enum
from htmlnode import *
from textnode import *

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        striped = block.strip()
        if striped != "":
            new_blocks.append(striped)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"

def block_to_block_type(block):
   
   if block.startswith(("# ", "## ", "### ", "#### ", "##### ","###### ")):
        return BlockType.HEADING
   elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
   else:
        block = block.split("\n")
        quotes = [blo.startswith(">") for blo in block]
        if all(quotes):
            return BlockType.QUOTE
        unordered = [blo.startswith("- ") for blo in block]
        if all(unordered):
            return BlockType.UNORDERED
        ordered = [block[i].startswith(f"{i+1}. ") for i in range(len(block))]
        if all(ordered):
            return BlockType.ORDERED
        return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    HTML_list = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                HTML_list.append(ParentNode("p", text_to_children(block)))
            case BlockType.QUOTE:
                quotes = block.split("\n")
                html_quotes = []
                for quote in quotes:
                    if quote.startswith("> "):
                        quote = quote.lstrip("> ")
                        html_quotes.append(quote)
                html_quotes = "\n".join(html_quotes)
                html_quotes = html_quotes.replace("\n", " ")
                HTML_list.append(ParentNode("blockquote", text_to_children(html_quotes)))
            case BlockType.CODE:
                codes = block.split("\n")
                codes = "\n".join(codes[1:-1]) + "\n"
                code_block = TextNode(codes, TextType.CODE)
                HTML_list.append(ParentNode("pre", [text_node_to_html_node(code_block)]))
            case BlockType.HEADING:
                if block.startswith("# "):
                    HTML_list.append(ParentNode("h1", text_to_children(block[2:])))
                elif block.startswith("## "):
                    HTML_list.append(ParentNode("h2", text_to_children(block[3:])))
                elif block.startswith("### "):
                    HTML_list.append(ParentNode("h3", text_to_children(block[4:])))
                elif block.startswith("#### "):
                    HTML_list.append(ParentNode("h4", text_to_children(block[5:])))
                elif block.startswith("##### "):
                    HTML_list.append(ParentNode("h5", text_to_children(block[6:])))
                elif block.startswith("###### "):
                    HTML_list.append(ParentNode("h6", text_to_children(block[7:])))
            case BlockType.UNORDERED:
                un_list = block.split("\n")
                html_un = []
                for un in un_list:
                    if un.startswith("- "):
                        un = un.lstrip("- ")
                    elif un.startswith("* "):
                        un = un.lstrip("* ")
                    html_un.append(ParentNode("li", text_to_children(un)))

                HTML_list.append(ParentNode("ul", html_un))
            case BlockType.ORDERED:
                o_list = block.split("\n")
                html_o = []
                for o in o_list:
                    index = o.find(".") + 2
                    html_o.append(ParentNode("li", text_to_children(o[index:])))

                HTML_list.append(ParentNode("ol", html_o))
            case _:
                raise Exception("Wrong type")
    return ParentNode("div", HTML_list)
        