from textnode import TextNode


def main() -> None:
    Dummy_Node1 = TextNode("Text", "plain")
    print(Dummy_Node1)
    Dummy_Node2 = TextNode("More Text", "plain", "www.google.com")
    print(Dummy_Node1 == Dummy_Node2)

main()
