import re

def markdown_to_blocks(markdown):
    no_ws = markdown.strip()
    sentences = no_ws.split("\n\n")
    for i in range(len(sentences)):
        if sentences[i] == "":
            sentences.pop(i)
        sentences[i] = re.sub(r'\n\s+', '\n', sentences[i].strip()) # Replaces line breaks followed by whitespace with just a line break character
    print(sentences)
    return sentences