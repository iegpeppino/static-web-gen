import os
import shutil

def clear_directory(path):
    """This function recursively deletes files and sub-directories
    from a given path argument"""
    # Check if desired path exists
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            # Checks if file or directory
            if os.path.isdir(item_path):        
                print(f"Deleted directory: {item_path}")
            else:
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
    # If desired path doesn't exist, it is created
    else:
        os.makedirs(path)
        print(f"Created directory: {path}")

def copy_directory(src_path, dest_path):
    """Copies files from one directory to another"""
    # If path doesn't exist it is created
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)       
    for item in os.listdir(src_path):
        src_path = os.path.join(src_path, item)
        dest_path = os.path.join(dest_path, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)
            print(f"Copied file: {src_path} -> to {dest_path}")

def move_static_to_public(static_dir="static", public_dir="public"):
    """Clears files and sub-directories from public and then copies
    the contents from static to the former folder"""
    clear_directory(public_dir)
    copy_directory(static_dir, public_dir)
    print("Completed copying process")