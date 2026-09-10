import unittest
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
        self.assertEqual(new_nodes, expected)

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
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()
