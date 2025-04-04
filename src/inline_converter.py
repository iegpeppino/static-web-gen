from textnode import TextNode, TextType


"""
Takes a list of old text nodes, a delimiter and text type
then returns a list of text nodes split into multiple nodes
based on syntax
"""

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:  # Checking if there's a closing delimiter
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(splits)):
            if splits[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(splits[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(splits[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
