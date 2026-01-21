import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive




static_path = "./static"
public_path = "./public"
content_path = "./content"


def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    copy_files_recursive(static_path, public_path)
    generate_pages_recursive(dir_path_content=content_path, template_path="./template.html", dest_dir_path=public_path)

main()


    