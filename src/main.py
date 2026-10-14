from textnode import TextNode
from markdown_parser import markdown_to_html_node
import os
import shutil
import sys



def main() -> None:
    print(sys.argv)
    base_path = sys.argv[1]
    if base_path == "":
        base_path = "/"
    delete_and_copy("static", "docs")
    generate_page_recursive("content", "template.html", "docs", base_path)

def delete_and_copy(source: str, destination: str) -> None:
    # Set each of the pathsh for the source and destination files
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    print(source_path)
    destination_path = os.path.join(cwd, destination)
    if not os.path.exists(source_path) and not os.path.exists(destination_path):
        raise Exception("One of the paths does not exist")
    # Remove the destination directory, in order to rebuild it with the new source directory files.
    shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    # List each of the files in the given source directory
    directories_in_source = os.listdir(source_path)
    for entry in directories_in_source:
        entry_path = os.path.join(source_path, entry)
        if os.path.isdir(entry_path):
            os.mkdir(os.path.join(destination_path, entry))
            delete_and_copy(entry_path, os.path.join(destination, entry))
        else:
            shutil.copy(entry_path, destination_path)

def extract_title(markdown_file: str) -> str:
    heading_line = ""
    with open(markdown_file, "r") as md_file:
        for line in md_file:
            if line[:2] == "# ":
                heading_line = line[2:].strip()

    if heading_line == "":
        raise Exception("No h1 header included")
    else:
        return heading_line

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}", "\n----------")
    cwd = os.getcwd()
    source_path = os.path.join(cwd, from_path)
    destination_path = os.path.join(cwd, dest_path)
    markdown, template = "", ""
    with open(source_path, "r") as md_file:
        markdown = md_file.read()
    with open(template_path, "r") as temp_file:
        template = temp_file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(source_path)
    new_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    newer_template = new_template.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    with open(destination_path, "w") as html_file:
        html_file.write(newer_template)

def generate_page_recursive(dir_path_constant: str, template_path: str, dest_dir_path: str, base_path: str) -> None:
    files_in_dir_path = os.listdir(dir_path_constant)
    for file in files_in_dir_path:
        new_dir = os.path.join(dir_path_constant, file)
        new_dest_dir_path = os.path.join(dest_dir_path, file)
        if os.path.isdir(new_dir):
            os.mkdir(new_dest_dir_path)
            generate_page_recursive(new_dir, template_path, new_dest_dir_path, base_path)
        else:
            generate_page(new_dir, template_path, new_dest_dir_path.replace("md", "html"), base_path)


main()
