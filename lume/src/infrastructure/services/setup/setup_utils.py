import os
import shutil
import zipfile


def unzip_file(dst: str, url: str):
    file_name = url.split("/")[-1]
    path_zipfile = os.path.join(dst, file_name)
    zip_ref = zipfile.ZipFile(path_zipfile, "r")
    zip_ref.extractall(dst)
    zip_ref.close()
    os.remove(path_zipfile)

    if contain_one_folder(dst):
        content = os.listdir(dst)
        name_path = content[0]
        move_content(os.path.join(dst, name_path), dst)
        shutil.rmtree(os.path.join(dst, name_path))


def contain_one_folder(path):
    content = os.listdir(path)
    if len(content) == 1 and os.path.isdir(os.path.join(path, content[0])):
        return True
    return False


def move_content(unzip_directory_path, dst):
    unzip_directory_path_content = os.listdir(unzip_directory_path)
    for item_name in unzip_directory_path_content:
        shutil.move(os.path.join(unzip_directory_path, item_name), dst)
