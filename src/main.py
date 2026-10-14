from textnode import TextNode
import os
import shutil


def main() -> None:
    delete_and_copy("test/test_source", "test/test_dest")

def delete_and_copy(source: str, destination: str) -> None:
    # Set each of the pathsh for the source and destination files
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
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

    

main()
