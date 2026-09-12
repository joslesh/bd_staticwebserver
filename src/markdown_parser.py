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
                        if split_text[i] == "":
                            continue
                        new_nodes.append(TextNode(split_text[i], node.text_type))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)
    
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r'\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    # Take in each node, use the extract function
    # Split on each combined image/link text, using the combined text as a delimitter in the old function.
    new_nodes = []
    for node in old_nodes:
        process_list = [node.text]
        images_tuple_list = extract_markdown_images(node.text)
        if images_tuple_list == []:
            new_nodes.append(node)
            continue
        while images_tuple_list:
            delimiter_text = f"![{images_tuple_list[0][0]}]({images_tuple_list[0][1]})"
            process_list = process_list[0].split(delimiter_text, 1)
            if process_list[1] == "":
                process_list = process_list[:1]
            new_nodes.append(TextNode(process_list.pop(0), TextType.PLAIN))
            image_desc, image_text = images_tuple_list.pop(0)
            new_nodes.append(TextNode(image_desc, TextType.IMAGE, image_text))
        if process_list:
            new_nodes.append(TextNode(process_list[0], TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        process_list = [node.text]
        links_tuple_list = extract_markdown_links(node.text)
        if links_tuple_list == []:
            new_nodes.append(node)
            continue
        while links_tuple_list:
            delimiter_text = f"[{links_tuple_list[0][0]}]({links_tuple_list[0][1]})"
            process_list = process_list[0].split(delimiter_text, 1)
            if process_list[1] == "":
                process_list = process_list[:1]
            new_nodes.append(TextNode(process_list.pop(0), TextType.PLAIN))
            link_desc, link_text = links_tuple_list.pop(0)
            new_nodes.append(TextNode(link_desc, TextType.LINK, link_text))
        if process_list:
            new_nodes.append(TextNode(process_list[0], TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
