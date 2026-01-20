import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page




static_path = "./static"
public_path = "./public"

def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    copy_files_recursive(static_path, public_path)
    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")

main()


    