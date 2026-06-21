import os
import shutil


def copy_files(src: str, dst: str) -> None:
    if not os.path.exists(dst):
        os.mkdir(dst)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)

        if os.path.isfile(src_path):
            print(f"copying {src_path} to {dst_path}")
            _ = shutil.copy(src_path, dst_path)
        else:
            copy_files(src_path, dst_path)
