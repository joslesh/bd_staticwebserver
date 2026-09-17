import unittest
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from textnode import TextNode, TextType

class TestMarkdownParser(unittest.TestCase):
    def test_onecodenode(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_onenormalnode(self):
        node = TextNode("This is a normal node", TextType.PLAIN)
        expected = [node]
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_twonormalnodes(self):
        node = TextNode("This is a normal node", TextType.PLAIN)
        node2 = TextNode("This is also a normal node", TextType.PLAIN)
        og_nodes = [node, node2]
        new_nodes = split_nodes_delimiter(og_nodes, ",", TextType.CODE)
        expected = [node, node2]
        self.assertListEqual(new_nodes, expected)

    def text_twonodenodes(self):
        node = TextNode("This is a `code` node", TextType.PLAIN)
        node2 = TextNode("This is also a `code` node", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node, node2], "`", TypeType.CODE)
        expected = [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" node", TextType.PLAIN),
                TextNode("This is also a ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" node", TextType.PLAIN)]
        self.assertListEqual(new_nodes, expected)

    def test_two_codes_in_one_node(self):
        node = TextNode("This is `code` node and another `code 2`", TextType.PLAIN)
        expected = [
                TextNode("This is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" node and another ", TextType.PLAIN),
                TextNode("code 2", TextType.CODE),
                ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(expected, new_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
         matches = extract_markdown_links("This is text with a [link](google.com)")
         self.assertListEqual([("link", "google.com")], matches)

    def test_extract_markdown_images_duplicate(self):
        matches = extract_markdown_links("This is text with a ![image](www.image.com) and the same image ![image](www.image.com)")
        self.assertListEqual([("image", "www.image.com"), ("image", "www.image.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),],
            new_nodes,
        )
        
    def test_split_images_no_images(self):
        nodes = [
                TextNode("Plain text", TextType.PLAIN),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Italic text", TextType.ITALIC),
                TextNode("Code block", TextType.CODE)
                ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_links(self):
        node = TextNode(
                "This is text with an [link](https://www.google.com)",
                TextType.PLAIN,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://www.google.com")],
                new_nodes,
            )

    def test_split_links_no_links(self):
        nodes = [
                TextNode("Plain text", TextType.PLAIN),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Italic text", TextType.ITALIC),
                TextNode("Code block", TextType.CODE)
                ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_text_to_textnodes_given(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(new_nodes, expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_block_to_blocktype(self):
        block = "# Heading!"
        block2 = "## Heading!"
        block3 = "###### Heading!"
        block4 = "# H"
        blocktypes = [
                block_to_block_type(block),
                block_to_block_type(block2),
                block_to_block_type(block3),
                block_to_block_type(block4)
                ]
        expected = [BlockType.HEADING, BlockType.HEADING, BlockType.HEADING, BlockType.HEADING]
        self.assertListEqual(expected, blocktypes)

    def test_code_block_to_blocktype(self):
        block = "```\n This is a code block! ```"
        not_code_block = "`` just text ``"
        not_code_block2 = "``` just text ```"
        blocktypes = [
                block_to_block_type(block),
                block_to_block_type(not_code_block),
                block_to_block_type(not_code_block2)
                ]
        expected = [BlockType.CODE, BlockType.PARAGRAPH, BlockType.PARAGRAPH]
        self.assertListEqual(blocktypes, expected)

    def test_quote_block_to_blocktype(self):
        block = "> This is a quote!"
        block2 = ">This is also a quote!"
        block3 = "This is not a quote"
        block4 = ">This is a\n> double line quote"
        blocktypes = [
                block_to_block_type(block),
                block_to_block_type(block2),
                block_to_block_type(block3),
                block_to_block_type(block4)
                ]
        expected = [BlockType.QUOTE, BlockType.QUOTE, BlockType.PARAGRAPH, BlockType.QUOTE]
        self.assertListEqual(blocktypes, expected)

    def test_unordered_list_block_to_blocktype(self):
        block = "- This is a list"
        block2 = "-This is not a list"
        block3 = "- This is a\n- multiple line list"
        block4 = "- This is \n-almost an unordered list"
        blocktypes = [
                block_to_block_type(block),
                block_to_block_type(block2),
                block_to_block_type(block3),
                block_to_block_type(block4)
                ]
        expected = [BlockType.UNORDERED_LIST, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST, BlockType.PARAGRAPH]
        self.assertListEqual(blocktypes, expected)

    def test_ordered_list_block_to_blocktype(self):
        block = "1. This is a short list"
        block2 = "2. This is not a list"
        block3 = "1. This is a\n2. list with\n3. three elements"
        block4 = "1. This is not a\n2 list"
        block5 = "1.This is not a list"
        blocktypes = [
                block_to_block_type(block),
                block_to_block_type(block2),
                block_to_block_type(block3),
                block_to_block_type(block4),
                block_to_block_type(block5)
                ]
        expected = [BlockType.ORDERED_LIST, BlockType.PARAGRAPH, BlockType.ORDERED_LIST, BlockType.PARAGRAPH, BlockType.PARAGRAPH]
        self.assertListEqual(blocktypes, expected)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
