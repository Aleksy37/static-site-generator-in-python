import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT or delimiter not in n.text:
            new_nodes.append(n)
            continue

        parts = n.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
        

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT :
            new_nodes.append(n)
            continue
        current = n.text
        matches = extract_markdown_images(n.text)
        for match in matches:
            sections = current.split(f"![{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            current = sections[1]
        if len(current) != 0:
            new_nodes.append(TextNode(current, TextType.TEXT))            

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT :
            new_nodes.append(n)
            continue
        current = n.text
        matches = extract_markdown_links(n.text)
        for match in matches:
            sections = current.split(f"[{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            current = sections[1]
        if len(current) != 0:
            new_nodes.append(TextNode(current, TextType.TEXT))            

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
