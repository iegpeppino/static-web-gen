import os
import shutil

def clear_directory(path):
    """This function recursively deletes files and sub-directories
    from a given path argument"""
    # Check if desired path exists
    if os.path.exists(path):
       shutil.rmtree(path)
    return print("Directory deleted")

def copy_directory(src_path, dest_path):
    """Copies files from one directory to another"""
    # If path doesn't exist it is created
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)       

    for item in os.listdir(src_path):
        from_path = os.path.join(src_path, item)
        to_path = os.path.join(dest_path, item)

        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
            print(f"Copied file: {from_path} -> to {to_path}")
        else:
            copy_directory(from_path, to_path)
            

def move_static_to_public(static_dir="./static", public_dir="./docs"):
    """Clears files and sub-directories from public and then copies
    the contents from static to the former folder"""
    clear_directory(public_dir)
    copy_directory(static_dir, public_dir)
    print("Completed copying process")