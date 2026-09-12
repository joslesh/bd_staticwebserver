import unittest
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

if __name__ == "__main__":
    unittest.main()
