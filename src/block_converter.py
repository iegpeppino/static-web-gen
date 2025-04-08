import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

"""
Splits markdown text to blocks
disregarding any empty lines
"""
def markdown_to_blocks(markdown):
    no_ws = markdown.strip()
    sentences = no_ws.split("\n\n")
    for i in range(len(sentences)):
        if sentences[i] == "":
            sentences.pop(i)
        sentences[i] = re.sub(r'\n\s+', '\n', sentences[i].strip()) # Replaces line breaks followed by whitespace with just a line break character
    return sentences

"""
Using regex to find if the blocks start
with a markdown element and return their
respective BlockType.
If if doesn't match any of the cases it
is identified as a Paragraph type of block
"""
def block_to_block(block):
    lines = block.split("\n")
    if re.search('^#{1,6}\s', block):
        return BlockType.HEADING
    if re.search('^```[\s\S]*```$', block):
        return BlockType.CODE
    if re.search('^>{1}', block):
        for line in lines:
            if not re.search("^>", line):
                return BlockType.PARAGRAPH
        return  BlockType.QUOTE
    if re.search('^-\s', block):
        for line in lines:
            if not re.search('^-\s', line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if re.search('^1\.\s', block):
        for line in lines:
            if not re.search('^\d+\.\s', line):
                return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH