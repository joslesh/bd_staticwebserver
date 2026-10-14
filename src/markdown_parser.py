from textnode import TextType, TextNode, text_node_to_html_node
from markdown_block import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
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

def markdown_to_blocks(markdown: str) -> list[str]:
    final_block_strings = []
    for block in markdown.split("\n\n"):
        if block == "":
            continue
        final_block_strings.append(block.strip())
    return final_block_strings

def block_to_block_type(block: str) -> BlockType:
    # Find the type of block type each block that is passed in is, then return the given proper block. (First idea was to use a regex for each case, but hopefully this simpler approach works better)
    first_char_of_block = block[:1]
    if len(block) < 2:
        return BlockType.PARAGRAPH
    match first_char_of_block:
        case "#":
            #Somehow check if up to the first chars are a #, then a space.
            # For now will just check the first char.
            #space_after = True
            #pound_count = 0
            #for char in block:
            #    if pound_count > 6:
            #        if char != 
            return BlockType.HEADING
        case "`":
            # This should work no matter what the given input is
            if block[0:4] == "```\n" and block[-3:] == "```":
                return BlockType.CODE
            else:
                return BlockType.PARAGRAPH
        case ">":
            line_list = block.split("\n")
            all_newline = True
            for line in line_list:
                if line[0] != ">":
                    all_newline = False
                    break
            if all_newline:
                return BlockType.QUOTE
            return BlockType.PARAGRAPH
        case "-":
            line_list = block.split("\n")
            line_starts_with_dash = True
            for line in line_list:
                if line[:2] == "- ":
                    continue
                else:
                    line_starts_with_dash = False
            if line_starts_with_dash:
                return BlockType.UNORDERED_LIST
            else:
                return BlockType.PARAGRAPH
        case "1":
            line_list = block.split("\n")
            line_count = 1
            for line in line_list:
                if line[:3] == f"{line_count}. ":
                    line_count += 1
                    continue
                else:
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
         

def markdown_to_html_node(markdown: str) -> HTMLNode:
    list_of_children = []
    # Breaks down markdown file into one parent HTML Node
    # Start by breaking the inital str into blocks:
    list_of_blocks = markdown_to_blocks(markdown)
    # Then take the list and transfer the blocks into nodes, with the proper types.
    # (helper function for creating the proper nodes and node types?)
    
    for block in list_of_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                final_text = block.strip("```").lstrip()
                list_of_children.append(ParentNode("pre", [LeafNode("code", final_text)]))
            case BlockType.PARAGRAPH:
                list_of_children.append(ParentNode("p", text_to_children(block)))

            case BlockType.UNORDERED_LIST:
                list_of_children.append(ParentNode("ul", text_unordered_list_to_children(block))) 

            case BlockType.QUOTE:
                list_of_children.append(text_quote_block_to_children(block))

            case BlockType.ORDERED_LIST:
                list_of_children.append(ParentNode("ol", text_ordered_list_to_children(block)))

            case BlockType.HEADING:
                list_of_children.append(text_header_to_children(block))

    return ParentNode("div", list_of_children)


def text_to_children(text: str) -> list[HTMLNode]:
    no_newline_text = text.replace("\n", " ")
    text_nodes = text_to_textnodes(no_newline_text)
    new_list = []
    for node in text_nodes:
        new_list.append(text_node_to_html_node(node))
    return new_list

def text_unordered_list_to_children(text: str) -> list[HTMLNode]:
    list_of_lines = text.split("\n")
    list_of_cleaned_lines = []
    for line in list_of_lines:
        new_line = line.strip("- ").strip()
        list_of_cleaned_lines.append(ParentNode("li", text_to_children(new_line)))
    return list_of_cleaned_lines

def text_ordered_list_to_children(text: str) -> list[HTMLNode]:
    list_of_lines = text.split("\n")
    list_of_cleaned_lines = []
    for line in list_of_lines:
        new_line = line[3:]
        list_of_cleaned_lines.append(ParentNode("li", text_to_children(new_line)))
    return list_of_cleaned_lines

def text_header_to_children(text: str) -> list[HTMLNode]:
    header_count = text.count("#")
    new_line = text[header_count + 1:]
    return ParentNode(f"h{header_count}", text_to_children(new_line))

def text_quote_block_to_children(text: str) -> list[HTMLNode]:
    return LeafNode("blockquote", text.replace("> ", "").strip())
