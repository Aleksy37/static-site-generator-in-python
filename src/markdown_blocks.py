from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_lsit"


def markdown_to_blocks(markdown):
    splits = markdown.split("\n\n")
    blocks = []
    for block in splits:
        block = block.strip()
        if len(block) == 0:
            continue
        blocks.append(block)
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")
    for i in range(1,7):
        prefix = "#" * i + " "
        if block.startswith(prefix):
            return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    for line in lines:
        if not line.startswith("> "):
            break
    else:
        return BlockType.QUOTE
    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.ULIST
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            break
    else:
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node)) 
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            header_count = block.count("#", 0, 7)
            content = block[header_count + 1:]
            header_level = f"h{header_count}"
            children  = text_to_children(content)
            html_nodes.append(ParentNode(header_level, children)) 
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            children = []
            for line in lines:
                content = line.strip().lstrip("> ")
                children.extend(text_to_children(content))
            html_nodes.append(ParentNode("blockquote", children)) 
        elif block_type == BlockType.CODE:
            content = block[4:-4]  
            text_node = TextNode(content, TextType.TEXT)
            leaf = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [leaf])
            html_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.ULIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                children = []
                content = line.strip().lstrip("- ")
                children.extend(text_to_children(content))
                list_items.append(ParentNode("li", children))
            html_nodes.append(ParentNode("ul", list_items))
        elif block_type == BlockType.OLIST:
            lines = block.split("\n")
            list_items = []
            for i, line in enumerate(lines):
                children = []
                content = line[len(str(i + 1)) + 2:]
                children.extend(text_to_children(content))
                list_items.append(ParentNode("li", children))
            html_nodes.append(ParentNode("ol", list_items))
        elif block_type == BlockType.PARAGRAPH:
            content = block.replace("\n", " ")
            children = text_to_children(content)
            html_nodes.append(ParentNode("p", children))
        
    return ParentNode("div", html_nodes)