from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            split_text = node.text.split(delimiter)
            if len(split_text) == 1:
                new_nodes.append(node)
            elif len(split_text) % 2 == 0:
                raise Exception("Did not find matching delimiter")
            else:
                for i in range(0, len(split_text)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_text[i], node.text_type))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)
    
def extract_markdown_links(test: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*)\(([^)]+)\)"
    return re.finaladd(pattern, text)

