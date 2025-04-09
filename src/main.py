import os
import shutil

def clear_directory(path):
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):        # Checks whether it's a directory
                shutil.rmtree(item_path)        # or a file
                print(f"Deleted directory: {item_path}")
            else:
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
    else:
        os.makedirs(path)
        print(f"Created directory: {path}")

def copy_directory(src, dest):
    if not os.path.exists(dest): # If the desired destiny path 
        os.makedirs(dest)       # doesn't exist, it is created
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)
            print(f"Copied file: {src_path} -> to {dest_path}")

def move_static_to_public(static_dir="static", public_dir="public"):
    clear_directory(public_dir)
    copy_directory(static_dir, public_dir)
    print("Completed copying process")

def main():
   return move_static_to_public("../static", "../public")


if __name__ == "__main__":
    move_static_to_public()
