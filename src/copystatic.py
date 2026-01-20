import os, shutil

def copy_files_recursive(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in os.listdir(src):
        item_src = os.path.join(src, item)
        item_dst = os.path.join(dst, item)
        if os.path.isfile(item_src):
           shutil.copy(item_src, item_dst)
        if os.path.isdir(item_src):
            copy_files_recursive(item_src, item_dst)