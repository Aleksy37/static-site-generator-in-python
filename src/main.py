import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import sys


basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]
static_path = "./static"
docs_path = "./docs"
content_path = "./content"


def main():
    if os.path.exists(docs_path):
        shutil.rmtree(docs_path)
    copy_files_recursive(static_path, docs_path)
    generate_pages_recursive(dir_path_content=content_path, template_path="./template.html", dest_dir_path=docs_path, basepath=basepath)

main()


    