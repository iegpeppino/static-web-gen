import os
import shutil
from .block_converter import markdown_to_html_node, extract_title
from pathlib import Path

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md:
        markdown_file = md.read()
        md.close()
    with open(template_path, "r") as tmp:
        template = tmp.read()
        tmp.close()
    title = extract_title(markdown_file)
    print(title)
    converted_md = markdown_to_html_node(markdown_file) # Markdown converted to html_node
    print(converted_md)
    html_string = converted_md.to_html()                # html node converted to string
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) # Making sure the destiny directory exists
    print(template)
    with open(dest_path, "w") as html_file:
        html_file.write(template)
        html_file.close()
    return print("HTML file was created!")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(src_path, template_path, dest_path)
        else:
            generate_pages_recursive(src_path, template_path, dest_path)

def main():
    move_static_to_public("static/", "public/")
    generate_pages_recursive("./content", "template.html", "./public")
    

if __name__ == "__main__":
    main()
